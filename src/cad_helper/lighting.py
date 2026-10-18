"""Lighting: bollard/path lights and ground spotlights."""

from __future__ import annotations

import math
from collections.abc import Sequence

from ezdxf.document import Drawing
from ezdxf.layouts import Modelspace

from cad_helper.core import Point, add_circle_hatch, add_layer, walk_polyline


def draw_path_light(
    msp: Modelspace, doc: Drawing, cx: float, cy: float, layer: str = "LIGHTING", color: int = 2
) -> None:
    """Path light: ring, lamp dot and eight rays."""
    add_layer(doc, layer, color=color)
    r = 150
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})
    msp.add_circle((cx, cy), radius=30, dxfattribs={"layer": layer})
    for deg in range(0, 360, 45):
        a = math.radians(deg)
        msp.add_line(
            (cx + r * math.cos(a), cy + r * math.sin(a)),
            (cx + r * 1.5 * math.cos(a), cy + r * 1.5 * math.sin(a)),
            dxfattribs={"layer": layer},
        )


def draw_spotlight(
    msp: Modelspace, doc: Drawing, cx: float, cy: float, layer: str = "LIGHTING", color: int = 2
) -> None:
    """In-ground spotlight: filled 200 mm dot."""
    add_layer(doc, layer, color=color)
    msp.add_circle((cx, cy), radius=100, dxfattribs={"layer": layer})
    add_circle_hatch(msp, (cx, cy), 100, layer=layer, color=color)


def draw_lights_along_path(
    msp: Modelspace,
    doc: Drawing,
    waypoints: Sequence[Point],
    spacing: float = 3000,
    layer: str = "LIGHTING",
    color: int = 2,
) -> None:
    """Path lights every ``spacing`` mm along the polyline ``waypoints``."""
    if len(waypoints) < 2:
        raise ValueError("draw_lights_along_path needs at least two waypoints")
    for (x, y), _ in walk_polyline(waypoints, spacing):
        draw_path_light(msp, doc, x, y, layer, color)
