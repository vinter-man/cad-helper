"""Japanese garden elements: stone lantern, karesansui, stepping stones, tsukubai,
torii, niwaki, bamboo fence and moss.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from ezdxf.document import Drawing
from ezdxf.enums import TextEntityAlignment
from ezdxf.layouts import Modelspace

from cad_helper.core import (
    Point,
    add_circle_hatch,
    add_hatch,
    add_label,
    add_layer,
    clip_segment,
    rect_points,
    rotate_point,
    walk_polyline,
)

STONE_GREY = 8
GRAVEL_GREY = 253


# ─── Stone lantern (toro) ────────────────────────────────────────────────────


def draw_stone_lantern(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    size: float = 600,
    layer: str = "LANTERNS",
    color: int = 8,
) -> None:
    """Toro seen from above: octagonal roof, square firebox, finial and light rays."""
    add_layer(doc, layer, color=color)
    r = size / 2
    roof = [
        (
            cx + r * math.cos(math.radians(i * 45 + 22.5)),
            cy + r * math.sin(math.radians(i * 45 + 22.5)),
        )
        for i in range(8)
    ]
    msp.add_lwpolyline(roof, close=True, dxfattribs={"layer": layer})
    s = r * 0.5
    msp.add_lwpolyline(
        rect_points(cx - s, cy - s, 2 * s, 2 * s), close=True, dxfattribs={"layer": layer}
    )
    msp.add_circle((cx, cy), radius=r * 0.12, dxfattribs={"layer": layer})
    for deg in (0, 90, 180, 270):
        a = math.radians(deg)
        msp.add_line(
            (cx + r * 0.14 * math.cos(a), cy + r * 0.14 * math.sin(a)),
            (cx + r * 0.35 * math.cos(a), cy + r * 0.35 * math.sin(a)),
            dxfattribs={"layer": layer},
        )


# ─── Dry garden (karesansui) ────────────────────────────────────────────────

RIPPLE_STEP = 0.5  # each ripple ring is this much of the stone radius further out


def draw_zen_garden(
    msp: Modelspace,
    doc: Drawing,
    points: Sequence[Point],
    stones: Sequence[dict] | None = None,
    rake_spacing: float = 150,
    rake_angle: float = 0,
    layer: str = "ZEN_GARDEN",
    color: int = 8,
) -> None:
    """Raked gravel field with stones.

    Each stone is ``{"cx", "cy", "rx", "ry", "rotation", "ripples"}``; ``ripples``
    (default 3) is the number of concentric rake rings around it. Straight rake lines
    are clipped to the boundary and stop at the outermost ring, as they would in gravel.
    """
    add_layer(doc, layer, color=color)
    gravel = f"{layer}_GRAVEL"
    stone_layer = f"{layer}_STONES"
    add_layer(doc, gravel, color=GRAVEL_GREY)
    add_layer(doc, stone_layer, color=STONE_GREY)

    msp.add_lwpolyline(points, close=True, dxfattribs={"layer": layer, "const_width": 10})
    add_hatch(msp, points, layer=gravel, color=GRAVEL_GREY, pattern="AR-SAND", scale=15)

    stones = [{"rx": 400, "ry": 300, "rotation": 0, "ripples": 3, **s} for s in stones or []]
    keep_out = [
        (
            s["cx"],
            s["cy"],
            s["rx"] * (1 + RIPPLE_STEP * s["ripples"]),
            s["ry"] * (1 + RIPPLE_STEP * s["ripples"]),
            s["rotation"],
        )
        for s in stones
    ]

    for a, b in _rake_lines(points, rake_spacing, rake_angle):
        pieces = clip_segment(a, b, points)
        for ellipse in keep_out:
            pieces = [part for seg in pieces for part in _outside_ellipse(seg, ellipse)]
        for p, q in pieces:
            msp.add_line(p, q, dxfattribs={"layer": gravel})

    for s in stones:
        _draw_stone(msp, s["cx"], s["cy"], s["rx"], s["ry"], s["rotation"], stone_layer)
        for ring in range(1, s["ripples"] + 1):
            k = 1 + RIPPLE_STEP * ring
            msp.add_ellipse(
                center=(s["cx"], s["cy"]),
                major_axis=_axis(s["rx"] * k, s["rotation"]),
                ratio=s["ry"] / s["rx"],
                dxfattribs={"layer": gravel},
            )


def _axis(length: float, rotation: float) -> Point:
    a = math.radians(rotation)
    return (length * math.cos(a), length * math.sin(a))


def _rake_lines(
    boundary: Sequence[Point], spacing: float, angle: float
) -> list[tuple[Point, Point]]:
    """Parallel lines at ``angle`` covering the boundary's bounding circle."""
    xs = [p[0] for p in boundary]
    ys = [p[1] for p in boundary]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    reach = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) / 2 + spacing
    ux, uy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    n = int(reach / spacing)
    lines = []
    for i in range(-n, n + 1):
        ox, oy = cx - uy * i * spacing, cy + ux * i * spacing
        lines.append(((ox - ux * reach, oy - uy * reach), (ox + ux * reach, oy + uy * reach)))
    return lines


def _outside_ellipse(
    seg: tuple[Point, Point], ellipse: tuple[float, float, float, float, float]
) -> list[tuple[Point, Point]]:
    """The parts of a segment outside a rotated ellipse (cx, cy, rx, ry, rotation)."""
    cx, cy, rx, ry, rot = ellipse
    (x1, y1), (x2, y2) = seg
    p = rotate_point((x1, y1), (cx, cy), -rot)
    q = rotate_point((x2, y2), (cx, cy), -rot)
    px, py = (p[0] - cx) / rx, (p[1] - cy) / ry
    dx, dy = (q[0] - p[0]) / rx, (q[1] - p[1]) / ry
    a = dx * dx + dy * dy
    b = 2 * (px * dx + py * dy)
    c = px * px + py * py - 1
    disc = b * b - 4 * a * c
    if a < 1e-12 or disc <= 0:
        return [seg]
    t0 = (-b - math.sqrt(disc)) / (2 * a)
    t1 = (-b + math.sqrt(disc)) / (2 * a)
    if t0 >= 1 or t1 <= 0:
        return [seg]

    def lerp(t: float) -> Point:
        return (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t)

    pieces = []
    if t0 > 0:
        pieces.append(((x1, y1), lerp(t0)))
    if t1 < 1:
        pieces.append((lerp(t1), (x2, y2)))
    return pieces


def _draw_stone(
    msp: Modelspace, cx: float, cy: float, rx: float, ry: float, rotation: float, layer: str
) -> None:
    pts = []
    for i in range(12):
        a = math.radians(i * 30)
        k = 1.0 + 0.15 * math.sin(a * 3.7)
        pts.append(
            rotate_point((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)), (cx, cy), rotation)
        )
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer, "const_width": 15})
    add_hatch(msp, pts, layer=layer, color=STONE_GREY)


# ─── Stepping stones (tobi-ishi) ────────────────────────────────────────────


def draw_stepping_stones(
    msp: Modelspace,
    doc: Drawing,
    waypoints: Sequence[Point],
    stone_size: float = 400,
    spacing: float = 200,
    layer: str = "STEPPING_STONES",
    color: int = 8,
) -> None:
    """Irregular stones every ``stone_size + spacing`` mm, staggered left and right
    of the walking line in the classic tobi-ishi rhythm."""
    if len(waypoints) < 2:
        raise ValueError("draw_stepping_stones needs at least two waypoints")
    add_layer(doc, layer, color=color)
    stagger = stone_size * 0.3
    for i, ((px, py), (ux, uy)) in enumerate(walk_polyline(waypoints, stone_size + spacing)):
        side = 1 if i % 2 == 0 else -1
        _draw_stepping_stone(
            msp,
            px - uy * stagger * side,
            py + ux * stagger * side,
            stone_size,
            seed=i * 37,
            layer=layer,
        )


def _draw_stepping_stone(
    msp: Modelspace, cx: float, cy: float, size: float, seed: int, layer: str
) -> None:
    r = size / 2
    pts = []
    for i in range(8):
        a = math.radians(i * 45)
        k = 0.85 + 0.3 * abs(math.sin(seed + i * 1.7))  # deterministic irregularity
        pts.append((cx + r * k * math.cos(a), cy + r * k * math.sin(a)))
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer, "const_width": 8})
    add_hatch(msp, pts, layer=layer, color=GRAVEL_GREY)


# ─── Water basin (tsukubai) ─────────────────────────────────────────────────


def draw_tsukubai(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    diameter: float = 800,
    layer: str = "TSUKUBAI",
    color: int = 140,
) -> None:
    """Stone basin with water and a bamboo spout (kakei) running east."""
    add_layer(doc, layer, color=color)
    r = diameter / 2
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})
    msp.add_circle((cx, cy), radius=r * 0.7, dxfattribs={"layer": layer})
    add_circle_hatch(msp, (cx, cy), r * 0.7, layer=layer, color=140)
    msp.add_line((cx + r, cy), (cx + r * 1.8, cy), dxfattribs={"layer": layer, "lineweight": 30})
    add_label(msp, "TSUKUBAI", (cx, cy - r - 250), height=150, layer=layer)


# ─── Torii ───────────────────────────────────────────────────────────────────


def draw_torii(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    width: float = 2000,
    depth: float = 400,
    layer: str = "TORII",
    color: int = 1,
) -> None:
    """Torii in plan: two round pillars under an overhanging lintel (kasagi)."""
    add_layer(doc, layer, color=color)
    hw = width / 2
    pillar = 200
    for side in (-1, 1):
        px = cx + side * (hw - pillar / 2)
        msp.add_circle((px, cy), radius=pillar / 2, dxfattribs={"layer": layer})
        add_circle_hatch(msp, (px, cy), pillar / 2, layer=layer, color=color)
    msp.add_lwpolyline(
        rect_points(cx - hw * 1.1, cy - depth / 2, hw * 2.2, depth),
        close=True,
        dxfattribs={"layer": layer, "const_width": 10},
    )
    add_label(msp, "TORII", (cx, cy + depth / 2 + 200), height=150, layer=layer)


# ─── Niwaki (cloud-pruned tree) ─────────────────────────────────────────────


def draw_niwaki(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    crown_diameter: float = 3000,
    num_clouds: int = 5,
    label: str = "",
    layer: str = "NIWAKI",
    color: int = 83,
) -> None:
    """Cloud-pruned tree: trunk, ``num_clouds`` foliage pads on a golden-angle spiral."""
    add_layer(doc, layer, color=color)
    r = crown_diameter / 2
    msp.add_circle((cx, cy), radius=r * 0.08, dxfattribs={"layer": layer})
    add_circle_hatch(msp, (cx, cy), r * 0.08, layer=layer, color=33)
    for i in range(num_clouds):
        a = math.radians(i * 137.5)
        dist = r * (0.3 + 0.4 * i / num_clouds)
        pad_r = r * 0.4 * (0.7 + 0.6 * abs(math.sin(i * 1.3)))
        msp.add_circle(
            (cx + dist * math.cos(a), cy + dist * math.sin(a)),
            radius=pad_r,
            dxfattribs={"layer": layer},
        )
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})
    if label:
        add_label(
            msp,
            label,
            (cx + r + 100, cy),
            height=150,
            layer=layer,
            align=TextEntityAlignment.MIDDLE_LEFT,
        )


# ─── Bamboo fence (takegaki) ────────────────────────────────────────────────


def draw_bamboo_fence(
    msp: Modelspace,
    doc: Drawing,
    start: Point,
    end: Point,
    height_symbol: float = 300,
    layer: str = "BAMBOO_FENCE",
    color: int = 33,
) -> None:
    """Fence panel drawn as a ``height_symbol``-wide strip with slats every ~200 mm."""
    add_layer(doc, layer, color=color)
    (x1, y1), (x2, y2) = start, end
    length = math.hypot(x2 - x1, y2 - y1)
    if length < 1:
        raise ValueError("bamboo fence start and end are the same point")
    nx, ny = -(y2 - y1) / length, (x2 - x1) / length
    h = height_symbol / 2
    msp.add_lwpolyline(
        [
            (x1 + nx * h, y1 + ny * h),
            (x2 + nx * h, y2 + ny * h),
            (x2 - nx * h, y2 - ny * h),
            (x1 - nx * h, y1 - ny * h),
        ],
        close=True,
        dxfattribs={"layer": layer},
    )
    n = int(length / 200)
    for i in range(1, n):
        px, py = x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n
        msp.add_line(
            (px + nx * h, py + ny * h), (px - nx * h, py - ny * h), dxfattribs={"layer": layer}
        )


# ─── Moss ────────────────────────────────────────────────────────────────────


def draw_moss_area(
    msp: Modelspace, doc: Drawing, points: Sequence[Point], layer: str = "MOSS", color: int = 83
) -> None:
    add_layer(doc, layer, color=color)
    msp.add_lwpolyline(points, close=True, dxfattribs={"layer": layer, "const_width": 5})
    add_hatch(msp, points, layer=layer, color=color, pattern="DOTS", scale=120)
