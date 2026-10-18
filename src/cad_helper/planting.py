"""Planting: trees, shrubs, flower beds, lawn, hedges."""

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
    offset_polyline,
    polygon_centroid,
    rect_points,
    smooth_closed,
)

_LEFT = TextEntityAlignment.MIDDLE_LEFT


def draw_tree(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    crown_diameter: float = 4000,
    label: str = "",
    layer: str = "TREES",
    color: int = 83,
) -> None:
    """Tree symbol: crown circle, trunk dot and crosshair. Size it at mature crown diameter."""
    add_layer(doc, layer, color=color)
    r = crown_diameter / 2
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})
    msp.add_circle((cx, cy), radius=r * 0.05, dxfattribs={"layer": layer})
    cross = r * 0.7
    msp.add_line((cx - cross, cy), (cx + cross, cy), dxfattribs={"layer": layer})
    msp.add_line((cx, cy - cross), (cx, cy + cross), dxfattribs={"layer": layer})
    if label:
        add_label(msp, label, (cx + r + 100, cy), height=150, layer=layer, align=_LEFT)


def draw_shrub(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    diameter: float = 1500,
    label: str = "",
    layer: str = "SHRUBS",
    color: int = 3,
) -> None:
    """Shrub symbol: outline plus six overlapping circles suggesting foliage."""
    add_layer(doc, layer, color=color)
    r = diameter / 2
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})
    for deg in range(0, 360, 60):
        a = math.radians(deg)
        msp.add_circle(
            (cx + r * 0.5 * math.cos(a), cy + r * 0.5 * math.sin(a)),
            radius=r * 0.35,
            dxfattribs={"layer": layer},
        )
    if label:
        add_label(msp, label, (cx + r + 100, cy), height=150, layer=layer, align=_LEFT)


def draw_flower_bed(
    msp: Modelspace,
    doc: Drawing,
    points: Sequence[Point],
    name: str = "FLOWER BED",
    layer: str = "FLOWER_BEDS",
    color: int = 200,
    smooth: bool = True,
) -> None:
    """Planting bed. With ``smooth=True`` the outline is rounded through the given corners."""
    add_layer(doc, layer, color=color)
    add_layer(doc, f"{layer}_FILL", color=color)
    outline = smooth_closed(points) if smooth else list(points)
    msp.add_lwpolyline(outline, close=True, dxfattribs={"layer": layer})
    add_hatch(msp, outline, layer=f"{layer}_FILL", color=color, pattern="GRASS", scale=50)
    add_label(msp, name, polygon_centroid(points), height=180, layer=layer)


def draw_round_bed(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    diameter: float = 3000,
    name: str = "FLOWER BED",
    layer: str = "FLOWER_BEDS",
    color: int = 200,
) -> None:
    add_layer(doc, layer, color=color)
    add_layer(doc, f"{layer}_FILL", color=color)
    msp.add_circle((cx, cy), radius=diameter / 2, dxfattribs={"layer": layer})
    add_circle_hatch(
        msp, (cx, cy), diameter / 2, layer=f"{layer}_FILL", color=color, pattern="GRASS", scale=50
    )
    add_label(msp, name, (cx, cy), height=150, layer=layer)


def draw_planter(
    msp: Modelspace,
    doc: Drawing,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str = "",
    layer: str = "PLANTERS",
    color: int = 30,
) -> None:
    """Raised planter or trough: double outline (wall + soil line), soil hatch, label along
    its long side."""
    add_layer(doc, layer, color=color)
    msp.add_lwpolyline(rect_points(x, y, w, h), close=True, dxfattribs={"layer": layer})
    wall = min(50, w / 6, h / 6)
    inner = rect_points(x + wall, y + wall, w - 2 * wall, h - 2 * wall)
    msp.add_lwpolyline(inner, close=True, dxfattribs={"layer": layer})
    add_hatch(msp, inner, layer=layer, color=color, pattern="EARTH", scale=8)
    if label:
        add_label(
            msp, label, (x + w / 2, y + h / 2), height=150, layer=layer, rotation=90 if h > w else 0
        )


def draw_lawn(
    msp: Modelspace, doc: Drawing, points: Sequence[Point], layer: str = "LAWN", color: int = 83
) -> None:
    add_layer(doc, layer, color=color)
    msp.add_lwpolyline(points, close=True, dxfattribs={"layer": layer, "const_width": 5})
    add_hatch(msp, points, layer=layer, color=color, pattern="GRASS", scale=80)


def draw_hedge(
    msp: Modelspace,
    doc: Drawing,
    points: Sequence[Point],
    hedge_width: float = 800,
    layer: str = "HEDGES",
    color: int = 3,
) -> None:
    """Clipped hedge of ``hedge_width`` along the centreline ``points``."""
    if len(points) < 2:
        raise ValueError("draw_hedge needs at least two points")
    add_layer(doc, layer, color=color)
    left, right = offset_polyline(points, hedge_width / 2)
    boundary = [*left, *reversed(right)]
    msp.add_lwpolyline(boundary, close=True, dxfattribs={"layer": layer})
    add_hatch(msp, boundary, layer=layer, color=color, pattern="GRASS", scale=30)
