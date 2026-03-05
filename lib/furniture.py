"""Outdoor furniture and structures — BBQ, pergola, benches, tables."""

import math
from lib.core import add_layer


def draw_bbq_zone(msp, doc, x: float, y: float,
                  grill_w: float = 1200, grill_h: float = 600,
                  counter_w: float = 2000, counter_h: float = 600,
                  layout: str = "L", layer: str = "BBQ", color: int = 1):
    """Draw a BBQ station with grill and counter.

    Args:
        x, y: Bottom-left corner of the BBQ area.
        layout: "L" for L-shaped, "I" for inline.
    """
    add_layer(doc, layer, color=color)

    # Grill
    _draw_filled_rect(msp, x, y, grill_w, grill_h, layer)
    msp.add_text("GRILL", height=100, dxfattribs={
        "layer": layer, "insert": (x + 100, y + grill_h / 2 - 50),
    })

    if layout == "L":
        # Counter perpendicular to grill
        cx = x + grill_w
        cy = y
        _draw_filled_rect(msp, cx, cy, counter_h, counter_w, layer)
        msp.add_text("COUNTER", height=100, dxfattribs={
            "layer": layer,
            "insert": (cx + 50, cy + counter_w / 2),
            "rotation": 90,
        })
    else:
        # Counter inline
        cx = x + grill_w + 100
        cy = y
        _draw_filled_rect(msp, cx, cy, counter_w, counter_h, layer)
        msp.add_text("COUNTER", height=100, dxfattribs={
            "layer": layer, "insert": (cx + 100, cy + counter_h / 2 - 50),
        })


def draw_pergola(msp, doc, x: float, y: float, w: float, h: float,
                 layer: str = "PERGOLA", color: int = 33):
    """Draw a pergola as rectangle with cross and 4 posts.

    Args:
        x, y: Bottom-left corner.
        w: Width in mm.
        h: Height in mm.
    """
    add_layer(doc, layer, color=color)

    # Outline
    msp.add_lwpolyline(
        [(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
        close=True,
        dxfattribs={"layer": layer, "const_width": 20},
    )

    # Cross
    msp.add_line((x, y), (x + w, y + h), dxfattribs={"layer": layer})
    msp.add_line((x + w, y), (x, y + h), dxfattribs={"layer": layer})

    # 4 posts (small squares)
    post = 200
    for px, py in [(x, y), (x + w - post, y), (x, y + h - post), (x + w - post, y + h - post)]:
        _draw_filled_rect(msp, px, py, post, post, layer)

    # Label
    msp.add_text("PERGOLA", height=200, dxfattribs={
        "layer": layer, "insert": (x + w / 2 - 400, y + h / 2 - 100),
    })


def draw_bench(msp, doc, x: float, y: float,
               w: float = 1800, h: float = 500,
               rotation: float = 0,
               layer: str = "FURNITURE", color: int = 6):
    """Draw a bench symbol."""
    add_layer(doc, layer, color=color)

    if rotation == 0:
        msp.add_lwpolyline(
            [(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
            close=True,
            dxfattribs={"layer": layer},
        )
        # Backrest line
        msp.add_line((x, y + h * 0.7), (x + w, y + h * 0.7),
                     dxfattribs={"layer": layer})
    else:
        # For rotated benches, use simple rectangle + backrest
        import ezdxf.math
        corners = [
            (x, y), (x + w, y), (x + w, y + h), (x, y + h),
        ]
        rad = math.radians(rotation)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        cx, cy = x + w / 2, y + h / 2
        rotated = []
        for px, py in corners:
            dx, dy = px - cx, py - cy
            rotated.append((cx + dx * cos_a - dy * sin_a,
                          cy + dx * sin_a + dy * cos_a))
        msp.add_lwpolyline(rotated, close=True, dxfattribs={"layer": layer})


def draw_table_with_chairs(msp, doc, cx: float, cy: float,
                           table_diameter: float = 1200,
                           num_chairs: int = 6,
                           chair_size: float = 400,
                           layer: str = "FURNITURE", color: int = 6):
    """Draw a round table with chairs arranged around it.

    Args:
        cx, cy: Center of the table.
        table_diameter: Table diameter in mm.
        num_chairs: Number of chairs.
        chair_size: Chair square size in mm.
    """
    add_layer(doc, layer, color=color)

    # Table circle
    msp.add_circle((cx, cy), radius=table_diameter / 2,
                   dxfattribs={"layer": layer})
    msp.add_text("TABLE", height=120, dxfattribs={
        "layer": layer, "insert": (cx - 200, cy - 60),
    })

    # Chairs
    chair_radius = table_diameter / 2 + chair_size
    for i in range(num_chairs):
        angle = 2 * math.pi * i / num_chairs
        chair_cx = cx + chair_radius * math.cos(angle)
        chair_cy = cy + chair_radius * math.sin(angle)

        half = chair_size / 2
        msp.add_lwpolyline(
            [
                (chair_cx - half, chair_cy - half),
                (chair_cx + half, chair_cy - half),
                (chair_cx + half, chair_cy + half),
                (chair_cx - half, chair_cy + half),
            ],
            close=True,
            dxfattribs={"layer": layer},
        )


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _draw_filled_rect(msp, x, y, w, h, layer):
    """Draw a rectangle with hatch fill."""
    msp.add_lwpolyline(
        [(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
        close=True,
        dxfattribs={"layer": layer},
    )
    hatch = msp.add_hatch(dxfattribs={"layer": layer})
    hatch.paths.add_polyline_path(
        [(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
        is_closed=True,
    )
    hatch.set_pattern_fill("ANSI31", scale=20)
