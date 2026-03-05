"""Functional zones — colored/hatched areas for landscape zoning."""

import ezdxf
from lib.core import add_layer


def draw_zone(msp, doc, points: list[tuple[float, float]],
              name: str, color: int = 3, hatch_pattern: str = "ANSI31",
              hatch_scale: float = 100, opacity: float = 0.5):
    """Draw a functional zone as an outlined, hatched area with label.

    Args:
        points: List of (x, y) vertices defining the zone boundary.
        name: Zone name (used for layer and label).
        color: ACI color index.
        hatch_pattern: DXF hatch pattern name (e.g. "ANSI31", "GRASS", "GRAVEL").
        hatch_scale: Scale of the hatch pattern.
    """
    layer_outline = f"ZONE_{name.upper().replace(' ', '_')}"
    layer_fill = f"ZONE_{name.upper().replace(' ', '_')}_FILL"

    add_layer(doc, layer_outline, color=color)
    add_layer(doc, layer_fill, color=color)

    # Outline
    msp.add_lwpolyline(
        points, close=True,
        dxfattribs={"layer": layer_outline, "const_width": 15},
    )

    # Hatched fill
    hatch = msp.add_hatch(color=color, dxfattribs={"layer": layer_fill})
    hatch.paths.add_polyline_path(points, is_closed=True)
    try:
        hatch.set_pattern_fill(hatch_pattern, scale=hatch_scale)
    except ezdxf.DXFValueError:
        pass  # fallback to solid if pattern not available

    # Label at centroid
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    msp.add_text(name, height=250, dxfattribs={
        "layer": layer_outline,
        "insert": (cx - len(name) * 60, cy),
    })


def draw_rect_zone(msp, doc, x: float, y: float, w: float, h: float,
                   name: str, color: int = 3, hatch_pattern: str = "ANSI31",
                   hatch_scale: float = 100):
    """Shortcut for rectangular zones."""
    points = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    draw_zone(msp, doc, points, name, color, hatch_pattern, hatch_scale)
