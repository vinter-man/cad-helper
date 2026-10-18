"""Curved walkways: B-spline centreline offset to both sides and hatched."""

from __future__ import annotations

from collections.abc import Sequence

from ezdxf.document import Drawing
from ezdxf.layouts import Modelspace
from ezdxf.math import BSpline

from cad_helper.core import Point, add_hatch, add_layer, offset_polyline


def draw_path(
    msp: Modelspace,
    doc: Drawing,
    waypoints: Sequence[Point],
    path_width: float = 1200,
    layer: str = "PATHS",
    color: int = 33,
    segments: int = 50,
) -> None:
    """Smooth path shaped by ``waypoints``.

    The waypoints are B-spline control points: the path starts and ends exactly on
    the first and last one and is pulled towards the ones in between.

    Draws both edges and end caps on ``layer``, a CENTER-linetype centreline on
    ``<layer>_CL`` and a sand hatch on ``<layer>_FILL``.
    """
    if len(waypoints) < 2:
        raise ValueError("draw_path needs at least two waypoints")
    add_layer(doc, layer, color=color)
    add_layer(doc, f"{layer}_CL", color=8, linetype="CENTER")
    add_layer(doc, f"{layer}_FILL", color=color)

    if len(waypoints) == 2:
        curve = list(waypoints)
    else:
        spline = BSpline(waypoints, order=min(4, len(waypoints)))
        curve = [(p.x, p.y) for p in spline.approximate(segments)]

    left, right = offset_polyline(curve, path_width / 2)
    msp.add_lwpolyline(left, dxfattribs={"layer": layer})
    msp.add_lwpolyline(right, dxfattribs={"layer": layer})
    msp.add_line(left[0], right[0], dxfattribs={"layer": layer})
    msp.add_line(left[-1], right[-1], dxfattribs={"layer": layer})
    msp.add_lwpolyline(curve, dxfattribs={"layer": f"{layer}_CL", "ltscale": 20})
    add_hatch(
        msp,
        [*left, *reversed(right)],
        layer=f"{layer}_FILL",
        color=color,
        pattern="AR-SAND",
        scale=25,
    )


def draw_straight_path(
    msp: Modelspace,
    doc: Drawing,
    start: Point,
    end: Point,
    path_width: float = 1200,
    layer: str = "PATHS",
    color: int = 33,
) -> None:
    draw_path(msp, doc, [start, end], path_width, layer, color)
