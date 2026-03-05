"""Curved path and walkway generators.

Creates smooth curved paths using splines, with optional tile fill.
"""

import math
import ezdxf
from ezdxf.math import BSpline
from lib.core import add_layer


def draw_path(msp, doc, waypoints: list[tuple[float, float]],
              path_width: float = 1200, layer: str = "PATHS",
              color: int = 33, segments: int = 50):
    """Draw a smooth curved path through waypoints.

    The path is drawn as two parallel offset splines with closing caps.

    Args:
        waypoints: Control points the path passes through (x, y).
        path_width: Width of the path in mm.
        layer: Layer name.
        color: ACI color.
        segments: Number of segments for spline interpolation.
    """
    add_layer(doc, layer, color=color)

    if len(waypoints) < 2:
        return

    # Generate smooth curve points via B-spline
    if len(waypoints) == 2:
        # Straight path — just two points
        curve_points = waypoints
    else:
        spline = BSpline(waypoints, order=min(4, len(waypoints)))
        curve_points = list(spline.approximate(segments))

    # Calculate offset curves (left and right of centerline)
    left_points = []
    right_points = []
    half_w = path_width / 2

    for i in range(len(curve_points)):
        p = curve_points[i]
        px, py = p[0], p[1]

        # Calculate normal direction
        if i == 0:
            dx = curve_points[i + 1][0] - px
            dy = curve_points[i + 1][1] - py
        elif i == len(curve_points) - 1:
            dx = px - curve_points[i - 1][0]
            dy = py - curve_points[i - 1][1]
        else:
            dx = curve_points[i + 1][0] - curve_points[i - 1][0]
            dy = curve_points[i + 1][1] - curve_points[i - 1][1]

        length = math.sqrt(dx * dx + dy * dy)
        if length < 0.001:
            continue

        # Normal vector (perpendicular to direction)
        nx = -dy / length
        ny = dx / length

        left_points.append((px + nx * half_w, py + ny * half_w))
        right_points.append((px - nx * half_w, py - ny * half_w))

    # Draw left edge
    if left_points:
        msp.add_lwpolyline(left_points, dxfattribs={"layer": layer})

    # Draw right edge
    if right_points:
        msp.add_lwpolyline(right_points, dxfattribs={"layer": layer})

    # Draw closing caps
    if left_points and right_points:
        msp.add_line(left_points[0], right_points[0], dxfattribs={"layer": layer})
        msp.add_line(left_points[-1], right_points[-1], dxfattribs={"layer": layer})

    # Draw centerline as dashed
    add_layer(doc, f"{layer}_CL", color=8)
    center_2d = [(p[0], p[1]) for p in curve_points]
    msp.add_lwpolyline(center_2d, dxfattribs={"layer": f"{layer}_CL"})

    # Hatch the path area
    add_layer(doc, f"{layer}_FILL", color=color)
    boundary = list(left_points) + list(reversed(right_points))
    if len(boundary) >= 3:
        hatch = msp.add_hatch(color=color, dxfattribs={"layer": f"{layer}_FILL"})
        hatch.paths.add_polyline_path(boundary, is_closed=True)
        hatch.set_pattern_fill("AR-SAND", scale=25)


def draw_straight_path(msp, doc, start: tuple[float, float],
                       end: tuple[float, float],
                       path_width: float = 1200,
                       layer: str = "PATHS", color: int = 33):
    """Draw a straight path segment."""
    draw_path(msp, doc, [start, end], path_width, layer, color)
