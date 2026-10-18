"""``cad-helper`` command line.

cad-helper new <name> --width 20000 --length 30000   scaffold projects/<name>/build.py
cad-helper build <name|path>                         build DXF + preview.png, run checks
cad-helper render <file.dxf> -o out.png              PNG preview of any DXF
cad-helper check <file.dxf> [--bounds x0,y0,x1,y1]   checks on any DXF
cad-helper tiles grid --width 3000 --length 8000 --tile 600x300 --offset
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
import time
from collections import Counter
from pathlib import Path

import ezdxf

from cad_helper.checks import check_document
from cad_helper.core import save
from cad_helper.render import render_png

PROJECTS_DIR = Path("projects")

BUILD_TEMPLATE = '''"""{title}.

Brief: brief.md - plan: plan.md - review: review.md
Build: uv run cad-helper build {name}
"""

from cad_helper.checks import Clearance
from cad_helper.core import create_document
from cad_helper.site import draw_compass, draw_fence, draw_plot

# ─── Configuration (mm; origin = south-west corner, X east, Y north) ────────

PLOT_W = {width}
PLOT_L = {length}

BOUNDS = (0, 0, PLOT_W, PLOT_L)  # every non-annotation entity must stay inside
CLEARANCES: list[Clearance] = []  # e.g. Clearance("HOUSE", "POND", 3000, "water away from foundations")


def build():
    doc = create_document()
    msp = doc.modelspace()

    draw_plot(msp, doc, width=PLOT_W, length=PLOT_L)
    draw_fence(msp, doc, width=PLOT_W, length=PLOT_L, gates=[
        {{"side": "south", "center": PLOT_W / 2, "opening": 1500, "label": "GATE"}},
    ])
    draw_compass(msp, doc, x=-2500, y=PLOT_L - 2000)

    return doc
'''


# ─── Project commands ────────────────────────────────────────────────────────


def _project_script(target: str) -> Path:
    p = Path(target)
    if p.is_file():
        return p
    if p.is_dir():
        return p / "build.py"
    return PROJECTS_DIR / target / "build.py"


def _load_module(script: Path):
    spec = importlib.util.spec_from_file_location(f"cad_project_{script.parent.name}", script)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot import {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cmd_new(args: argparse.Namespace) -> int:
    name = re.sub(r"[^a-z0-9_]+", "_", args.name.lower()).strip("_")
    folder = PROJECTS_DIR / name
    script = folder / "build.py"
    if script.exists():
        print(f"{script} already exists", file=sys.stderr)
        return 1
    folder.mkdir(parents=True, exist_ok=True)
    script.write_text(
        BUILD_TEMPLATE.format(
            title=name.replace("_", " ").title(),
            name=name,
            width=f"{int(args.width):_}",
            length=f"{int(args.length):_}",
        )
    )
    print(f"Created {script}")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    script = _project_script(args.project)
    if not script.exists():
        print(f"No build script at {script}", file=sys.stderr)
        return 1
    started = time.perf_counter()
    module = _load_module(script)
    doc = module.build()

    issues = check_document(
        doc,
        bounds=getattr(module, "BOUNDS", None),
        clearances=getattr(module, "CLEARANCES", ()),
        plot_scale=getattr(module, "PLOT_SCALE", 100),
    )
    out = save(doc, script.parent / f"{script.parent.name}.dxf")
    msp = doc.modelspace()
    layers = sorted({e.dxf.layer for e in msp})
    print(f"Built: {out}")
    print(f"  {len(msp)} entities on {len(layers)} layers in {time.perf_counter() - started:.1f}s")

    if not args.no_preview:
        preview = render_png(doc, script.parent / "preview.png", theme=args.theme)
        print(f"  Preview: {preview}")
    return _report(issues)


def _report(issues) -> int:
    errors = [i for i in issues if i.level == "error"]
    if not issues:
        print("Checks: all passed")
        return 0
    print(f"Checks: {len(errors)} error(s), {len(issues) - len(errors)} warning(s)")
    for issue in issues:
        print(f"  {issue}")
    return 1 if errors else 0


def cmd_render(args: argparse.Namespace) -> int:
    out = Path(args.output) if args.output else Path(args.dxf).with_suffix(".png")
    print(f"Rendered: {render_png(args.dxf, out, theme=args.theme, width_px=args.width)}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    bounds = tuple(float(v) for v in args.bounds.split(",")) if args.bounds else None
    if bounds is not None and len(bounds) != 4:
        print("--bounds needs four numbers: x0,y0,x1,y1", file=sys.stderr)
        return 2
    return _report(check_document(ezdxf.readfile(args.dxf), bounds=bounds, plot_scale=args.scale))


def cmd_layers(args: argparse.Namespace) -> int:
    """Layer table as AutoCAD's layer manager would show it, with entity counts."""
    doc = ezdxf.readfile(args.dxf)
    counts = Counter(e.dxf.layer for e in doc.modelspace())
    print(f"{'LAYER':<24} {'COLOR':>5} {'LINETYPE':<12} {'ENTITIES':>8}")
    for layer in sorted(doc.layers, key=lambda la: la.dxf.name):
        name = layer.dxf.name
        if name in ("0", "Defpoints") and not counts[name]:
            continue
        print(f"{name:<24} {layer.color:>5} {layer.dxf.linetype:<12} {counts[name]:>8}")
    return 0


# ─── Tile commands ───────────────────────────────────────────────────────────


def _tile(s: str) -> tuple[float, float]:
    parts = s.lower().split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(f"invalid tile size {s!r}, use WxH, e.g. 600x300")
    return float(parts[0]), float(parts[1])


def _tile_list(s: str) -> list[tuple[float, float]]:
    return [_tile(part.strip()) for part in s.split(",")]


def cmd_tiles(args: argparse.Namespace) -> int:
    from cad_helper import patterns

    common = {
        "width": args.width,
        "length": args.length,
        "gap": args.gap,
        "filled": args.filled,
        "output": args.output,
    }
    if args.pattern == "paving":
        result = patterns.create_paving(tiles=args.tiles, **common)
    elif args.pattern == "grid":
        w, h = args.tile or (600, 300)
        result = patterns.create_grid(tile_w=w, tile_h=h, offset_rows=args.offset, **common)
    elif args.pattern == "herringbone":
        w, h = args.tile or (300, 100)
        result = patterns.create_herringbone(tile_w=w, tile_h=h, **common)
    else:
        w, h = args.tile or (300, 150)
        result = patterns.create_border(tile_w=w, tile_h=h, border_rows=args.rows, **common)
    print(result.summary())
    if args.preview:
        print(f"  Preview: {render_png(result.path, result.path.with_suffix('.png'))}")
    return 0


# ─── Parser ──────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cad-helper", description="Landscape DXF drawings for AutoCAD."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("new", help="scaffold projects/<name>/build.py")
    p.add_argument("name")
    p.add_argument("--width", type=float, required=True, help="plot width west-east, mm")
    p.add_argument("--length", type=float, required=True, help="plot length south-north, mm")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("build", help="build a project: DXF, preview.png and checks")
    p.add_argument("project", help="project name under projects/, its folder, or a build.py path")
    p.add_argument("--theme", choices=["dark", "light"], default="dark")
    p.add_argument("--no-preview", action="store_true", help="skip rendering preview.png")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("render", help="render a DXF to PNG")
    p.add_argument("dxf")
    p.add_argument("-o", "--output")
    p.add_argument("--theme", choices=["dark", "light"], default="dark")
    p.add_argument("--width", type=int, default=1600, help="image width in pixels")
    p.set_defaults(func=cmd_render)

    p = sub.add_parser("check", help="run drawing checks on a DXF")
    p.add_argument("dxf")
    p.add_argument("--bounds", help="site extents x0,y0,x1,y1 in mm")
    p.add_argument("--scale", type=int, default=100, help="print scale denominator (default 100)")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("layers", help="list layers with colour and entity count")
    p.add_argument("dxf")
    p.set_defaults(func=cmd_layers)

    p = sub.add_parser("tiles", help="standalone tile layout with full/cut tile counts")
    p.add_argument("pattern", choices=["paving", "grid", "herringbone", "border"])
    p.add_argument("--width", type=float, required=True, help="area width (Y), mm")
    p.add_argument("--length", type=float, required=True, help="area length (X), mm")
    p.add_argument("--gap", type=float, default=5, help="joint width, mm (default 5)")
    p.add_argument("--tile", type=_tile, help="tile size WxH (grid, herringbone, border)")
    p.add_argument("--tiles", type=_tile_list, help="paving mix, e.g. 600x600,600x300,300x300")
    p.add_argument("--offset", action="store_true", help="grid: running bond")
    p.add_argument("--rows", type=int, default=1, help="border: number of rings")
    p.add_argument("--filled", action="store_true", help="solid-fill tiles")
    p.add_argument("--preview", action="store_true", help="also write a PNG preview")
    p.add_argument("-o", "--output", help="output DXF path")
    p.set_defaults(func=cmd_tiles)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
