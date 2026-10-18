"""Site elements: plot boundary, house, fence with gates, north arrow, dimensions."""

from __future__ import annotations

import math
from collections.abc import Sequence

from ezdxf.document import Drawing
from ezdxf.enums import TextEntityAlignment
from ezdxf.layouts import Modelspace

from cad_helper.core import Point, add_hatch, add_label, add_layer, rect_points

SIDES = ("south", "east", "north", "west")


# ─── Plot boundary ───────────────────────────────────────────────────────────


def draw_plot(msp: Modelspace, doc: Drawing, width: float, length: float) -> None:
    """Plot boundary with overall dimensions. ``width`` runs east (X), ``length`` north (Y)."""
    add_layer(doc, "PLOT_BOUNDARY", color=7)
    msp.add_lwpolyline(
        rect_points(0, 0, width, length),
        close=True,
        dxfattribs={"layer": "PLOT_BOUNDARY", "const_width": 40},
    )
    draw_distance(msp, doc, (0, 0), (width, 0), offset=-1200)
    draw_distance(msp, doc, (0, length), (0, 0), offset=-1200)


# ─── House ───────────────────────────────────────────────────────────────────


def draw_house(
    msp: Modelspace,
    doc: Drawing,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str = "HOUSE",
    entrance_side: str = "south",
    entrance_width: float = 1200,
    entrance_center: float | None = None,
) -> None:
    """House footprint with a door swing on ``entrance_side``. (x, y) is the south-west corner.

    ``entrance_center`` places the door along that side, measured from its west
    (south/north sides) or south (east/west sides) end; default is mid-side.
    """
    if entrance_side not in SIDES:
        raise ValueError(f"entrance_side must be one of {SIDES}, got {entrance_side!r}")
    add_layer(doc, "HOUSE", color=30)
    add_layer(doc, "HOUSE_FILL", color=8)

    outline = rect_points(x, y, w, h)
    msp.add_lwpolyline(outline, close=True, dxfattribs={"layer": "HOUSE", "const_width": 30})
    add_hatch(msp, outline, layer="HOUSE_FILL", color=8, pattern="ANSI31", scale=50)

    add_label(msp, label, (x + w / 2, y + h / 2 + 200), height=300, layer="HOUSE")
    add_label(
        msp,
        f"{w / 1000:g} x {h / 1000:g} m",
        (x + w / 2, y + h / 2 - 250),
        height=200,
        layer="HOUSE",
    )
    _draw_entrance(msp, x, y, w, h, entrance_side, entrance_width, entrance_center)


def _draw_entrance(
    msp: Modelspace,
    x: float,
    y: float,
    w: float,
    h: float,
    side: str,
    width: float,
    center: float | None,
) -> None:
    """Door leaf hinged at one jamb, swinging outward, with its quarter-circle swing."""
    attribs = {"layer": "HOUSE"}
    half = width / 2
    # hinge point, closed-leaf end, open-leaf end, arc start/end angles
    along = center if center is not None else (w if side in ("south", "north") else h) / 2
    if side == "south":
        cx = x + along
        hinge, closed, opened, arc = (
            (cx - half, y),
            (cx + half, y),
            (cx - half, y - width),
            (270, 360),
        )
    elif side == "north":
        cx = x + along
        hinge, closed, opened, arc = (
            (cx + half, y + h),
            (cx - half, y + h),
            (cx + half, y + h + width),
            (90, 180),
        )
    elif side == "east":
        cy = y + along
        hinge, closed, opened, arc = (
            (x + w, cy - half),
            (x + w, cy + half),
            (x + w + width, cy - half),
            (0, 90),
        )
    else:
        cy = y + along
        hinge, closed, opened, arc = (
            (x, cy + half),
            (x, cy - half),
            (x - width, cy + half),
            (180, 270),
        )
    msp.add_line(hinge, opened, dxfattribs=attribs)
    msp.add_arc(
        center=hinge, radius=width, start_angle=arc[0], end_angle=arc[1], dxfattribs=attribs
    )
    msp.add_circle(closed, radius=40, dxfattribs=attribs)  # strike jamb


# ─── Walls and steps ─────────────────────────────────────────────────────────


def draw_wall(
    msp: Modelspace,
    doc: Drawing,
    start: Point,
    end: Point,
    thickness: float = 200,
    label: str = "",
    layer: str = "WALLS",
    color: int = 8,
) -> None:
    """Solid wall (concrete, masonry) of ``thickness`` centred on the line start-end."""
    add_layer(doc, layer, color=color)
    (x1, y1), (x2, y2) = start, end
    length = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / length * thickness / 2, (x2 - x1) / length * thickness / 2
    outline = [(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)]
    msp.add_lwpolyline(outline, close=True, dxfattribs={"layer": layer})
    add_hatch(msp, outline, layer=layer, pattern="AR-CONC", scale=10)
    if label:
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        if not -90 < angle <= 90:
            angle -= 180  # keep text upright
        mid = ((x1 + x2) / 2 + nx * 3, (y1 + y2) / 2 + ny * 3)
        add_label(msp, label, mid, height=150, layer=layer, rotation=angle)


def draw_steps(
    msp: Modelspace,
    doc: Drawing,
    x: float,
    y: float,
    w: float,
    tread: float = 300,
    count: int = 2,
    label: str = "",
    layer: str = "STEPS",
    color: int = 33,
) -> None:
    """Flight of ``count`` steps rising northwards; (x, y) is the south-west corner of the lowest."""
    add_layer(doc, layer, color=color)
    for i in range(count):
        msp.add_lwpolyline(
            rect_points(x, y + i * tread, w, tread), close=True, dxfattribs={"layer": layer}
        )
    top = y + count * tread
    msp.add_line(
        (x + w / 2, y + tread * 0.2), (x + w / 2, top - tread * 0.2), dxfattribs={"layer": layer}
    )  # walking line, arrow points up the flight
    msp.add_line(
        (x + w / 2, top - tread * 0.2),
        (x + w / 2 - 80, top - tread * 0.45),
        dxfattribs={"layer": layer},
    )
    msp.add_line(
        (x + w / 2, top - tread * 0.2),
        (x + w / 2 + 80, top - tread * 0.45),
        dxfattribs={"layer": layer},
    )
    if label:
        add_label(
            msp,
            label,
            (x + w + 150, y + count * tread / 2),
            height=150,
            layer=layer,
            align=TextEntityAlignment.MIDDLE_LEFT,
        )


# ─── Fence ───────────────────────────────────────────────────────────────────


def draw_fence(
    msp: Modelspace,
    doc: Drawing,
    width: float,
    length: float,
    gates: list[dict] | None = None,
    sides: Sequence[str] = SIDES,
) -> None:
    """Perimeter fence with gate openings.

    Each gate is ``{"side": "south", "center": 12500, "opening": 4000, "label": "GATE"}``,
    where ``center`` is measured from the west end (south/north sides) or the south end
    (east/west sides). ``sides`` limits the fence to some sides, e.g. when a wall or
    building closes the others.
    """
    for side in sides:
        if side not in SIDES:
            raise ValueError(f"fence side must be one of {SIDES}, got {side!r}")
    add_layer(doc, "FENCE", color=3)
    add_layer(doc, "GATES", color=1)
    gates = gates or []
    for g in gates:
        if g["side"] not in sides:
            raise ValueError(f"gate side must be one of {tuple(sides)}, got {g['side']!r}")

    side_len = {"south": width, "north": width, "east": length, "west": length}
    for side in sides:
        openings = sorted(
            (g["center"] - g["opening"] / 2, g["center"] + g["opening"] / 2)
            for g in gates
            if g["side"] == side
        )
        pos = 0.0
        for start, end in [*openings, (side_len[side], side_len[side])]:
            if start - pos > 10:
                msp.add_line(
                    _on_side(side, pos, width, length),
                    _on_side(side, start, width, length),
                    dxfattribs={"layer": "FENCE", "lineweight": 50},
                )
            pos = max(pos, end)
        for g in gates:
            if g["side"] == side:
                _draw_gate(msp, g, width, length)


def _on_side(side: str, t: float, width: float, length: float) -> Point:
    """Point at distance ``t`` along a plot side (west->east or south->north)."""
    return {"south": (t, 0), "north": (t, length), "west": (0, t), "east": (width, t)}[side]


def _draw_gate(msp: Modelspace, gate: dict, width: float, length: float) -> None:
    """Gate posts plus a leaf swinging into the plot."""
    side, c, opening = gate["side"], gate["center"], gate["opening"]
    a = _on_side(side, c - opening / 2, width, length)
    b = _on_side(side, c + opening / 2, width, length)
    post = 150
    if side in ("south", "north"):
        for px, py in (a, b):
            msp.add_line(
                (px, py - post), (px, py + post), dxfattribs={"layer": "GATES", "lineweight": 50}
            )
        inward = 1 if side == "south" else -1
        arc = (0, 90) if side == "south" else (270, 360)
        leaf_end = (a[0], a[1] + inward * opening)
        label_at = (c, a[1] - inward * 500)
    else:
        for px, py in (a, b):
            msp.add_line(
                (px - post, py), (px + post, py), dxfattribs={"layer": "GATES", "lineweight": 50}
            )
        inward = 1 if side == "west" else -1
        arc = (0, 90) if side == "west" else (90, 180)
        leaf_end = (a[0] + inward * opening, a[1])
        label_at = (a[0] - inward * 500, c)
    msp.add_line(a, leaf_end, dxfattribs={"layer": "GATES"})
    msp.add_arc(
        center=a,
        radius=opening,
        start_angle=arc[0],
        end_angle=arc[1],
        dxfattribs={"layer": "GATES"},
    )
    if gate.get("label"):
        rotation = 90 if side in ("east", "west") else 0
        add_label(msp, gate["label"], label_at, height=200, layer="GATES", rotation=rotation)


# ─── North arrow ─────────────────────────────────────────────────────────────


def draw_compass(msp: Modelspace, doc: Drawing, x: float, y: float, size: float = 1500) -> None:
    """North arrow with its base centred on (x, y)."""
    add_layer(doc, "COMPASS", color=7)
    half_w = size * 0.15
    tip = (x, y + size)
    msp.add_lwpolyline(
        [tip, (x - half_w, y), (x, y + size * 0.25), (x + half_w, y)],
        close=True,
        dxfattribs={"layer": "COMPASS"},
    )
    add_hatch(msp, [tip, (x, y + size * 0.25), (x + half_w, y)], layer="COMPASS")
    add_label(msp, "N", (x, y + size + size * 0.25), height=size * 0.3, layer="COMPASS")


# ─── Dimensions ──────────────────────────────────────────────────────────────


def draw_distance(
    msp: Modelspace,
    doc: Drawing,
    p1: Point,
    p2: Point,
    offset: float = 500,
    layer: str = "DIMENSIONS",
    text_height: float = 250,
) -> None:
    """Associative AutoCAD dimension between two points, measured in metres.

    ``offset`` moves the dimension line to the left of the direction p1 -> p2
    (negative values move it to the right).
    """
    add_layer(doc, layer, color=8)
    dim = msp.add_aligned_dim(
        p1=p1,
        p2=p2,
        distance=offset,
        dimstyle="EZDXF",
        override={
            "dimtxt": text_height,
            "dimasz": text_height * 0.8,  # tick size
            "dimexe": 150,  # extension past the dimension line
            "dimexo": 100,  # gap between object and extension line
            "dimgap": 60,
            "dimlfac": 0.001,  # model units are mm, label in metres
            "dimdec": 2,
            "dimzin": 8,  # suppress trailing zeros: 25 m, 2.5 m
            "dimpost": "<> m",
            "dimtad": 1,  # text above the line
        },
        dxfattribs={"layer": layer},
    )
    dim.render()
