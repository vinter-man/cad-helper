"""Water features: ponds, streams, bridges."""

from __future__ import annotations

import math
from collections.abc import Sequence

from ezdxf.document import Drawing
from ezdxf.layouts import Modelspace

from cad_helper.core import Point, add_hatch, add_label, add_layer, offset_polyline, rotate_point

WATER_COLOR = 140
WATER_FILL = 150  # a shade darker, so the shoreline and label stay readable


def pond_outline(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    rotation: float = 0,
    irregular: bool = True,
    n: int = 48,
) -> list[Point]:
    """Ellipse, optionally with a few low-frequency waves so it reads as a natural shoreline."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1.0
        if irregular:
            k += (
                0.08 * math.sin(3 * a + 0.5)
                + 0.05 * math.sin(5 * a + 1.2)
                + 0.03 * math.sin(7 * a + 2.1)
            )
        pts.append(
            rotate_point((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)), (cx, cy), rotation)
        )
    return pts


def draw_pond(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    rx: float = 3000,
    ry: float = 2000,
    rotation: float = 0,
    irregular: bool = True,
    label: str = "POND",
    layer: str = "POND",
    color: int = WATER_COLOR,
) -> None:
    """Pond with shoreline, solid water fill on ``<layer>_FILL`` and an inner depth line."""
    add_layer(doc, layer, color=color)
    add_layer(doc, f"{layer}_FILL", color=WATER_FILL)

    shore = pond_outline(cx, cy, rx, ry, rotation, irregular)
    msp.add_lwpolyline(shore, close=True, dxfattribs={"layer": layer, "const_width": 15})
    add_hatch(msp, shore, layer=f"{layer}_FILL", color=WATER_FILL)
    deep = [(cx + (x - cx) * 0.7, cy + (y - cy) * 0.7) for x, y in shore]
    msp.add_lwpolyline(deep, close=True, dxfattribs={"layer": layer})
    if label:
        add_label(msp, label, (cx, cy), height=200, layer=layer)


def draw_stream(
    msp: Modelspace,
    doc: Drawing,
    waypoints: Sequence[Point],
    width: float = 600,
    layer: str = "STREAM",
    color: int = WATER_COLOR,
) -> None:
    """Stream along ``waypoints`` whose width wobbles by +-15 % for a natural bank line."""
    if len(waypoints) < 2:
        raise ValueError("draw_stream needs at least two waypoints")
    add_layer(doc, layer, color=color)
    wobble = [1.0 + 0.15 * math.sin(i * 2.3) for i in range(len(waypoints))]
    left, right = offset_polyline(waypoints, width / 2, wobble)
    msp.add_lwpolyline(left, dxfattribs={"layer": layer, "const_width": 10})
    msp.add_lwpolyline(right, dxfattribs={"layer": layer, "const_width": 10})
    add_hatch(msp, [*left, *reversed(right)], layer=layer, color=WATER_FILL)


def draw_bridge(
    msp: Modelspace,
    doc: Drawing,
    cx: float,
    cy: float,
    width: float = 2000,
    depth: float = 1200,
    arched: bool = True,
    rotation: float = 0,
    layer: str = "BRIDGE",
    color: int = 33,
) -> None:
    """Timber footbridge in plan.

    ``width`` is the span (walking direction, along X before rotation), ``depth``
    the deck width. Arched bridges get bowed rails and plank lines.
    """
    add_layer(doc, layer, color=color)
    hw, hd = width / 2, depth / 2

    def at(x: float, y: float) -> Point:
        return rotate_point((cx + x, cy + y), (cx, cy), rotation)

    if arched:
        n = 12
        top, bottom = [], []
        for i in range(n + 1):
            t = i / n
            bow = hd * 0.2 * math.sin(t * math.pi)
            top.append(at(-hw + t * width, hd + bow))
            bottom.append(at(-hw + t * width, -hd - bow))
        msp.add_lwpolyline(top, dxfattribs={"layer": layer, "const_width": 20})
        msp.add_lwpolyline(bottom, dxfattribs={"layer": layer, "const_width": 20})
        for a, b in zip(top, bottom, strict=True):
            msp.add_line(a, b, dxfattribs={"layer": layer})
    else:
        msp.add_lwpolyline(
            [at(-hw, -hd), at(hw, -hd), at(hw, hd), at(-hw, hd)],
            close=True,
            dxfattribs={"layer": layer, "const_width": 20},
        )
