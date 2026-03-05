"""Lighting elements — path lights, spotlights, ambient lights."""

import math
from lib.core import add_layer


def draw_path_light(msp, doc, cx: float, cy: float,
                    layer: str = "LIGHTING", color: int = 2):
    """Draw a path light symbol (circle with radiating lines)."""
    add_layer(doc, layer, color=color)

    r = 150
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})
    msp.add_circle((cx, cy), radius=30, dxfattribs={"layer": layer})

    # Radiating lines
    for angle_deg in range(0, 360, 45):
        angle = math.radians(angle_deg)
        msp.add_line(
            (cx + r * math.cos(angle), cy + r * math.sin(angle)),
            (cx + r * 1.5 * math.cos(angle), cy + r * 1.5 * math.sin(angle)),
            dxfattribs={"layer": layer},
        )


def draw_spotlight(msp, doc, cx: float, cy: float,
                   layer: str = "LIGHTING", color: int = 2):
    """Draw a spotlight symbol (filled dot)."""
    add_layer(doc, layer, color=color)

    msp.add_circle((cx, cy), radius=100, dxfattribs={"layer": layer})
    hatch = msp.add_hatch(color=color, dxfattribs={"layer": layer})
    edge_path = hatch.paths.add_edge_path()
    edge_path.add_arc(center=(cx, cy), radius=100, start_angle=0, end_angle=360)


def draw_lights_along_path(msp, doc, waypoints: list[tuple[float, float]],
                           spacing: float = 3000,
                           layer: str = "LIGHTING", color: int = 2):
    """Place path lights at regular intervals along a polyline.

    Args:
        waypoints: Points defining the path centerline.
        spacing: Distance between lights in mm.
    """
    if len(waypoints) < 2:
        return

    distance_covered = 0
    draw_path_light(msp, doc, waypoints[0][0], waypoints[0][1], layer, color)

    for i in range(1, len(waypoints)):
        x1, y1 = waypoints[i - 1]
        x2, y2 = waypoints[i]
        seg_len = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        if seg_len < 0.001:
            continue

        while distance_covered + spacing <= seg_len + distance_covered:
            remaining = spacing - distance_covered
            if remaining > seg_len:
                distance_covered += seg_len
                break

            t = remaining / seg_len
            lx = x1 + t * (x2 - x1)
            ly = y1 + t * (y2 - y1)
            draw_path_light(msp, doc, lx, ly, layer, color)

            x1, y1 = lx, ly
            seg_len = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            distance_covered = 0

        distance_covered = seg_len
