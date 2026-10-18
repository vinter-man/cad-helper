"""Outdoor furniture and structures: BBQ, pergola, benches, tables."""

from __future__ import annotations

import math

from ezdxf.document import Drawing
from ezdxf.layouts import Modelspace

from cad_helper.core import (
    add_circle_hatch,
    add_hatch,
    add_label,
    add_layer,
    rect_points,
    rotate_point,
)


def draw_bbq_zone(
    msp: Modelspace,
    doc: Drawing,
    x: float,
    y: float,
    grill_w: float = 1200,
    grill_h: float = 600,
    counter_w: float = 2000,
    counter_h: float = 600,
    layout: str = "L",
    layer: str = "BBQ",
    color: int = 1,
) -> None:
    """Grill plus worktop. ``layout="L"`` turns the counter north, ``"I"`` keeps it in line."""
    if layout not in ("L", "I"):
        raise ValueError(f"layout must be 'L' or 'I', got {layout!r}")
    add_layer(doc, layer, color=color)

    _filled_rect(msp, x, y, grill_w, grill_h, layer)
    add_label(msp, "GRILL", (x + grill_w / 2, y + grill_h / 2), height=150, layer=layer)

    if layout == "L":
        cx = x + grill_w
        _filled_rect(msp, cx, y, counter_h, counter_w, layer)
        add_label(
            msp,
            "COUNTER",
            (cx + counter_h / 2, y + counter_w / 2),
            height=150,
            layer=layer,
            rotation=90,
        )
    else:
        cx = x + grill_w + 100
        _filled_rect(msp, cx, y, counter_w, counter_h, layer)
        add_label(msp, "COUNTER", (cx + counter_w / 2, y + counter_h / 2), height=150, layer=layer)


def draw_pergola(
    msp: Modelspace,
    doc: Drawing,
    x: float,
    y: float,
    w: float,
    h: float,
    layer: str = "PERGOLA",
    color: int = 33,
) -> None:
    """Pergola footprint: frame, roof diagonals and four 200 mm posts."""
    add_layer(doc, layer, color=color)
    msp.add_lwpolyline(
        rect_points(x, y, w, h), close=True, dxfattribs={"layer": layer, "const_width": 20}
    )
    msp.add_line((x, y), (x + w, y + h), dxfattribs={"layer": layer})
    msp.add_line((x + w, y), (x, y + h), dxfattribs={"layer": layer})
    post = 200
    for px, py in [(x, y), (x + w - post, y), (x, y + h - post), (x + w - post, y + h - post)]:
        _filled_rect(msp, px, py, post, post, layer)
    add_label(msp, "PERGOLA", (x + w / 2, y + h / 2 + 250), height=200, layer=layer)


def draw_bench(
    msp: Modelspace,
    doc: Drawing,
    x: float,
    y: float,
    w: float = 1800,
    h: float = 500,
    rotation: float = 0,
    layer: str = "FURNITURE",
    color: int = 6,
) -> None:
    """Bench seat with its backrest along the north edge (before rotation).

    (x, y) is the south-west corner; ``rotation`` turns the bench about its centre.
    """
    add_layer(doc, layer, color=color)
    center = (x + w / 2, y + h / 2)
    seat = [rotate_point(p, center, rotation) for p in rect_points(x, y, w, h)]
    back = [rotate_point(p, center, rotation) for p in ((x, y + h * 0.7), (x + w, y + h * 0.7))]
    msp.add_lwpolyline(seat, close=True, dxfattribs={"layer": layer})
    msp.add_line(*back, dxfattribs={"layer": layer})


def draw_table_with_chairs(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    table_diameter: float = 1200,
    num_chairs: int = 6,
    chair_size: float = 400,
    layer: str = "FURNITURE",
    color: int = 6,
) -> None:
    """Round table with chairs evenly spaced around it, each turned to face the centre."""
    add_layer(doc, layer, color=color)
    msp.add_circle((cx, cy), radius=table_diameter / 2, dxfattribs={"layer": layer})

    ring = table_diameter / 2 + chair_size * 0.75
    half = chair_size / 2
    for i in range(num_chairs):
        angle = 360 * i / num_chairs
        ccx = cx + ring * math.cos(math.radians(angle))
        ccy = cy + ring * math.sin(math.radians(angle))
        square = rect_points(ccx - half, ccy - half, chair_size, chair_size)
        msp.add_lwpolyline(
            [rotate_point(p, (ccx, ccy), angle) for p in square],
            close=True,
            dxfattribs={"layer": layer},
        )


def draw_fire_pit(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    diameter: float = 1000,
    seat_radius: float = 1800,
    seat_arc: float = 240,
    layer: str = "FIRE_PIT",
    color: int = 30,
) -> None:
    """Round fire pit with a stone rim and a curved bench around it.

    The bench (on ``<layer>_SEATING``) is a ``seat_arc``-degree ring at ``seat_radius``,
    open to the south so the pit can be reached from that side. Keeping the fire and the
    seating on separate layers lets clearance rules measure from the fire itself.
    """
    add_layer(doc, layer, color=color)
    seating = f"{layer}_SEATING"
    add_layer(doc, seating, color=33)
    r = diameter / 2
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer, "lineweight": 50})
    msp.add_circle((cx, cy), radius=r - 150, dxfattribs={"layer": layer})
    add_circle_hatch(msp, (cx, cy), r - 150, layer=layer, color=1, pattern="AR-SAND", scale=4)
    start = 270 + (360 - seat_arc) / 2
    for radius in (seat_radius, seat_radius + 450):
        msp.add_arc(
            (cx, cy),
            radius=radius,
            start_angle=start,
            end_angle=start + seat_arc,
            dxfattribs={"layer": seating},
        )
    for a in (start, start + seat_arc):
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
        msp.add_line(
            (cx + seat_radius * c, cy + seat_radius * s_),
            (cx + (seat_radius + 450) * c, cy + (seat_radius + 450) * s_),
            dxfattribs={"layer": seating},
        )
    add_label(msp, "FIRE PIT", (cx, cy + r + 250), height=150, layer=layer)


def draw_rect_table(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    w: float = 800,
    h: float = 600,
    chairs: str = "NS",
    chair_diameter: float = 450,
    label: str = "",
    layer: str = "FURNITURE",
    color: int = 33,
) -> None:
    """Rectangular table centred on (cx, cy) with round chairs pulled up to the sides
    listed in ``chairs`` (any of "N", "S", "E", "W")."""
    add_layer(doc, layer, color=color)
    msp.add_lwpolyline(
        rect_points(cx - w / 2, cy - h / 2, w, h), close=True, dxfattribs={"layer": layer}
    )
    r = chair_diameter / 2
    gap = 50
    offsets = {
        "N": (0, h / 2 + gap + r),
        "S": (0, -h / 2 - gap - r),
        "E": (w / 2 + gap + r, 0),
        "W": (-w / 2 - gap - r, 0),
    }
    for side in chairs.upper():
        dx, dy = offsets[side]
        msp.add_circle((cx + dx, cy + dy), radius=r, dxfattribs={"layer": layer})
    if label:
        add_label(msp, label, (cx, cy), height=150, layer=layer)


def _filled_rect(msp: Modelspace, x: float, y: float, w: float, h: float, layer: str) -> None:
    pts = rect_points(x, y, w, h)
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})
    add_hatch(msp, pts, layer=layer, pattern="ANSI31", scale=20)
