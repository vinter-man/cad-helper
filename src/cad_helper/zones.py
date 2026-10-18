"""Functional zones: outlined, hatched areas with a centred name."""

from __future__ import annotations

from collections.abc import Sequence

from ezdxf.document import Drawing
from ezdxf.layouts import Modelspace

from cad_helper.core import Point, add_hatch, add_label, add_layer, polygon_centroid, rect_points


def zone_layer(name: str) -> str:
    return "ZONE_" + name.upper().replace(" ", "_")


def draw_zone(
    msp: Modelspace,
    doc: Drawing,
    points: Sequence[Point],
    name: str,
    color: int = 3,
    hatch_pattern: str = "ANSI31",
    hatch_scale: float = 100,
    label: bool = True,
) -> None:
    """Zone polygon on ``ZONE_<NAME>``, its hatch on ``ZONE_<NAME>_FILL``.

    ``label=False`` skips the centred name, e.g. when something else sits in the middle.
    """
    layer = zone_layer(name)
    add_layer(doc, layer, color=color)
    add_layer(doc, f"{layer}_FILL", color=color)

    msp.add_lwpolyline(points, close=True, dxfattribs={"layer": layer, "const_width": 15})
    add_hatch(
        msp, points, layer=f"{layer}_FILL", color=color, pattern=hatch_pattern, scale=hatch_scale
    )
    if label:
        add_label(msp, name, polygon_centroid(points), height=250, layer=layer)


def draw_rect_zone(
    msp: Modelspace,
    doc: Drawing,
    x: float,
    y: float,
    w: float,
    h: float,
    name: str,
    color: int = 3,
    hatch_pattern: str = "ANSI31",
    hatch_scale: float = 100,
) -> None:
    draw_zone(msp, doc, rect_points(x, y, w, h), name, color, hatch_pattern, hatch_scale)
