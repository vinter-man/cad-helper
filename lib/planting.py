"""Planting elements — trees, shrubs, flower beds, lawn, hedges."""

import math
from lib.core import add_layer


def draw_tree(msp, doc, cx: float, cy: float, crown_diameter: float = 4000,
              label: str = "", layer: str = "TREES", color: int = 83):
    """Draw a tree symbol (circle with center dot and cross).

    Args:
        cx, cy: Center position.
        crown_diameter: Crown diameter in mm.
        label: Optional tree name/label.
    """
    add_layer(doc, layer, color=color)
    r = crown_diameter / 2

    # Crown circle
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})

    # Center dot (small filled circle)
    msp.add_circle((cx, cy), radius=r * 0.05, dxfattribs={"layer": layer})

    # Cross through center
    cross = r * 0.7
    msp.add_line((cx - cross, cy), (cx + cross, cy), dxfattribs={"layer": layer})
    msp.add_line((cx, cy - cross), (cx, cy + cross), dxfattribs={"layer": layer})

    if label:
        msp.add_text(label, height=150, dxfattribs={
            "layer": layer, "insert": (cx + r + 100, cy - 75),
        })


def draw_shrub(msp, doc, cx: float, cy: float, diameter: float = 1500,
               label: str = "", layer: str = "SHRUBS", color: int = 3):
    """Draw a shrub symbol (filled circle with wavy edge effect)."""
    add_layer(doc, layer, color=color)
    r = diameter / 2

    # Main circle
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})

    # Inner texture circles (suggest foliage)
    for angle_deg in range(0, 360, 60):
        angle = math.radians(angle_deg)
        ix = cx + r * 0.5 * math.cos(angle)
        iy = cy + r * 0.5 * math.sin(angle)
        msp.add_circle((ix, iy), radius=r * 0.35, dxfattribs={"layer": layer})

    if label:
        msp.add_text(label, height=120, dxfattribs={
            "layer": layer, "insert": (cx + r + 100, cy - 60),
        })


def draw_flower_bed(msp, doc, points: list[tuple[float, float]],
                    name: str = "FLOWER BED",
                    layer: str = "FLOWER_BEDS", color: int = 200):
    """Draw a flower bed area with organic-looking boundary.

    Args:
        points: Boundary vertices. Use many points for organic shapes.
        name: Label text.
    """
    add_layer(doc, layer, color=color)
    add_layer(doc, f"{layer}_FILL", color=color)

    # Smooth boundary using spline
    if len(points) >= 4:
        msp.add_spline(points, dxfattribs={"layer": layer})
        # Also draw as polyline for hatch boundary
        msp.add_lwpolyline(points, close=True, dxfattribs={"layer": layer})
    else:
        msp.add_lwpolyline(points, close=True, dxfattribs={"layer": layer})

    # Hatch
    hatch = msp.add_hatch(color=color, dxfattribs={"layer": f"{layer}_FILL"})
    hatch.paths.add_polyline_path(points, is_closed=True)
    try:
        hatch.set_pattern_fill("GRASS", scale=50)
    except Exception:
        hatch.set_pattern_fill("ANSI37", scale=30)

    # Label at centroid
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    msp.add_text(name, height=180, dxfattribs={
        "layer": layer, "insert": (cx - len(name) * 50, cy),
    })


def draw_round_bed(msp, doc, cx: float, cy: float, diameter: float = 3000,
                   name: str = "FLOWER BED",
                   layer: str = "FLOWER_BEDS", color: int = 200):
    """Draw a circular flower bed."""
    add_layer(doc, layer, color=color)
    add_layer(doc, f"{layer}_FILL", color=color)

    r = diameter / 2
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})

    # Hatch
    hatch = msp.add_hatch(color=color, dxfattribs={"layer": f"{layer}_FILL"})
    edge_path = hatch.paths.add_edge_path()
    edge_path.add_arc(center=(cx, cy), radius=r, start_angle=0, end_angle=360)

    msp.add_text(name, height=150, dxfattribs={
        "layer": layer, "insert": (cx - len(name) * 40, cy - 75),
    })


def draw_lawn(msp, doc, points: list[tuple[float, float]],
              layer: str = "LAWN", color: int = 83):
    """Draw a lawn area (green hatched polygon)."""
    add_layer(doc, layer, color=color)

    msp.add_lwpolyline(points, close=True,
                       dxfattribs={"layer": layer, "const_width": 5})

    hatch = msp.add_hatch(color=color, dxfattribs={"layer": layer})
    hatch.paths.add_polyline_path(points, is_closed=True)
    try:
        hatch.set_pattern_fill("GRASS", scale=80)
    except Exception:
        hatch.set_pattern_fill("ANSI37", scale=50)


def draw_hedge(msp, doc, points: list[tuple[float, float]],
               hedge_width: float = 800,
               layer: str = "HEDGES", color: int = 3):
    """Draw a hedge line with width.

    Args:
        points: Centerline points of the hedge.
        hedge_width: Width of the hedge in mm.
    """
    add_layer(doc, layer, color=color)
    half_w = hedge_width / 2

    if len(points) < 2:
        return

    # Build offset polygons for left and right sides
    left_points = []
    right_points = []

    for i in range(len(points)):
        px, py = points[i]

        if i == 0:
            dx = points[1][0] - px
            dy = points[1][1] - py
        elif i == len(points) - 1:
            dx = px - points[i - 1][0]
            dy = py - points[i - 1][1]
        else:
            dx = points[i + 1][0] - points[i - 1][0]
            dy = points[i + 1][1] - points[i - 1][1]

        length = math.sqrt(dx * dx + dy * dy)
        if length < 0.001:
            continue

        nx = -dy / length
        ny = dx / length

        left_points.append((px + nx * half_w, py + ny * half_w))
        right_points.append((px - nx * half_w, py - ny * half_w))

    # Draw as closed polygon
    boundary = left_points + list(reversed(right_points))
    if len(boundary) >= 3:
        msp.add_lwpolyline(boundary, close=True, dxfattribs={"layer": layer})

        hatch = msp.add_hatch(color=color, dxfattribs={"layer": layer})
        hatch.paths.add_polyline_path(boundary, is_closed=True)
        try:
            hatch.set_pattern_fill("GRASS", scale=30)
        except Exception:
            hatch.set_pattern_fill("ANSI37", scale=20)
