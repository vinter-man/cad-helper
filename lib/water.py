"""Water features — ponds, streams, bridges."""

import math
from lib.core import add_layer


def draw_pond(msp, doc, cx: float, cy: float,
              rx: float = 3000, ry: float = 2000,
              rotation: float = 0,
              irregular: bool = True,
              layer: str = "POND", color: int = 140):
    """Draw a natural-looking pond — organic shape based on ellipse.

    Args:
        cx, cy: Center position.
        rx, ry: Semi-axes of the base ellipse.
        rotation: Rotation in degrees.
        irregular: If True, add natural irregularity to shape.
    """
    add_layer(doc, layer, color=color)
    add_layer(doc, f"{layer}_FILL", color=140)

    pts = []
    n_points = 36
    rad = math.radians(rotation)

    for i in range(n_points):
        angle = 2 * math.pi * i / n_points
        # Base ellipse
        x = rx * math.cos(angle)
        y = ry * math.sin(angle)

        if irregular:
            # Natural irregularity — multiple sine waves
            wave = (0.08 * math.sin(angle * 3 + 0.5)
                    + 0.05 * math.sin(angle * 5 + 1.2)
                    + 0.03 * math.sin(angle * 7 + 2.1))
            r = math.sqrt(x * x + y * y)
            x *= (1 + wave)
            y *= (1 + wave)

        # Rotate
        rx2 = x * math.cos(rad) - y * math.sin(rad)
        ry2 = x * math.sin(rad) + y * math.cos(rad)

        pts.append((cx + rx2, cy + ry2))

    # Outline
    msp.add_lwpolyline(pts, close=True,
                       dxfattribs={"layer": layer, "const_width": 15})

    # Water fill
    hatch = msp.add_hatch(color=140, dxfattribs={"layer": f"{layer}_FILL"})
    hatch.paths.add_polyline_path(pts, is_closed=True)

    # Inner ripple
    inner_pts = []
    for px, py in pts:
        dx, dy = px - cx, py - cy
        inner_pts.append((cx + dx * 0.7, cy + dy * 0.7))
    msp.add_lwpolyline(inner_pts, close=True,
                       dxfattribs={"layer": layer})

    # Label
    msp.add_text("POND", height=200, dxfattribs={
        "layer": layer, "insert": (cx - 200, cy - 100),
    })


def draw_stream(msp, doc, waypoints: list[tuple[float, float]],
                width: float = 600,
                layer: str = "STREAM", color: int = 140):
    """Draw a naturalistic stream between waypoints."""
    add_layer(doc, layer, color=color)

    if len(waypoints) < 2:
        return

    # Build offset banks with natural wobble
    left_bank = []
    right_bank = []
    half_w = width / 2

    for i in range(len(waypoints)):
        px, py = waypoints[i]

        if i == 0:
            dx = waypoints[1][0] - px
            dy = waypoints[1][1] - py
        elif i == len(waypoints) - 1:
            dx = px - waypoints[i - 1][0]
            dy = py - waypoints[i - 1][1]
        else:
            dx = waypoints[i + 1][0] - waypoints[i - 1][0]
            dy = waypoints[i + 1][1] - waypoints[i - 1][1]

        length = math.sqrt(dx * dx + dy * dy)
        if length < 0.001:
            continue

        nx = -dy / length
        ny = dx / length

        # Vary width slightly for natural look
        wobble = 1.0 + 0.15 * math.sin(i * 2.3)
        left_bank.append((px + nx * half_w * wobble, py + ny * half_w * wobble))
        right_bank.append((px - nx * half_w * wobble, py - ny * half_w * wobble))

    # Draw banks
    if left_bank:
        msp.add_lwpolyline(left_bank, dxfattribs={"layer": layer, "const_width": 10})
    if right_bank:
        msp.add_lwpolyline(right_bank, dxfattribs={"layer": layer, "const_width": 10})

    # Fill
    boundary = left_bank + list(reversed(right_bank))
    if len(boundary) >= 3:
        hatch = msp.add_hatch(color=140, dxfattribs={"layer": layer})
        hatch.paths.add_polyline_path(boundary, is_closed=True)


def draw_bridge(msp, doc, cx: float, cy: float,
                width: float = 2000, depth: float = 1200,
                arched: bool = True, rotation: float = 0,
                layer: str = "BRIDGE", color: int = 33):
    """Draw a Japanese-style wooden bridge — top view.

    Args:
        cx, cy: Center of the bridge.
        width: Bridge span (along the stream).
        depth: Bridge width (crossing direction).
        arched: If True, draw curved sides (arched bridge).
        rotation: Rotation in degrees.
    """
    add_layer(doc, layer, color=color)
    half_w = width / 2
    half_d = depth / 2
    rad = math.radians(rotation)

    def rotate_pt(x, y):
        rx = x * math.cos(rad) - y * math.sin(rad)
        ry = x * math.sin(rad) + y * math.cos(rad)
        return (cx + rx, cy + ry)

    if arched:
        # Curved sides
        n_pts = 12
        top_edge = []
        bottom_edge = []
        for i in range(n_pts + 1):
            t = i / n_pts
            x = -half_w + t * width
            # Arch curve
            arch = half_d * 0.2 * math.sin(t * math.pi)
            top_edge.append(rotate_pt(x, half_d + arch))
            bottom_edge.append(rotate_pt(x, -half_d - arch))

        msp.add_lwpolyline(top_edge, dxfattribs={"layer": layer, "const_width": 20})
        msp.add_lwpolyline(bottom_edge, dxfattribs={"layer": layer, "const_width": 20})

        # End caps
        msp.add_line(top_edge[0], bottom_edge[0], dxfattribs={"layer": layer})
        msp.add_line(top_edge[-1], bottom_edge[-1], dxfattribs={"layer": layer})

        # Planks (cross lines)
        for i in range(1, n_pts):
            msp.add_line(top_edge[i], bottom_edge[i], dxfattribs={"layer": layer})
    else:
        # Simple rectangle
        corners = [
            rotate_pt(-half_w, -half_d),
            rotate_pt(half_w, -half_d),
            rotate_pt(half_w, half_d),
            rotate_pt(-half_w, half_d),
        ]
        msp.add_lwpolyline(corners, close=True,
                           dxfattribs={"layer": layer, "const_width": 20})

    msp.add_text("BRIDGE", height=120, dxfattribs={
        "layer": layer, "insert": rotate_pt(-200, 0),
    })
