"""Core DXF utilities for cad-helper.

Provides document creation, layer management, and basic shape drawing.
All dimensions are in millimeters.
"""

import ezdxf
from ezdxf import units
from pathlib import Path

# Default AutoCAD color indices (ACI)
COLORS = {
    "red": 1,
    "yellow": 2,
    "green": 3,
    "cyan": 4,
    "blue": 5,
    "magenta": 6,
    "white": 7,
    "grey": 8,
    "light_red": 11,
    "light_green": 83,
    "orange": 30,
    "brown": 33,
    "light_blue": 140,
    "purple": 200,
    "pink": 220,
}

# Color rotation for auto-assigning colors to layers
COLOR_CYCLE = [1, 2, 3, 4, 5, 6, 30, 140, 200, 83, 33, 220]


def create_document(description: str = "") -> ezdxf.document.Drawing:
    """Create a new DXF document configured for mm units."""
    doc = ezdxf.new(dxfversion="R2010")
    doc.units = units.MM
    if description:
        doc.header["$INSUNITS"] = units.MM
    return doc


def add_layer(doc: ezdxf.document.Drawing, name: str, color: int = 7) -> None:
    """Add a named layer with specified ACI color. Safe to call multiple times."""
    if name not in doc.layers:
        doc.layers.add(name, color=color)


def add_layers_for_tiles(doc: ezdxf.document.Drawing, tile_sizes: list[tuple[float, float]]) -> dict[tuple[float, float], str]:
    """Create a layer for each unique tile size, return mapping of size -> layer name."""
    layer_map = {}
    for i, size in enumerate(tile_sizes):
        w, h = size
        layer_name = f"TILE_{int(w)}x{int(h)}"
        color = COLOR_CYCLE[i % len(COLOR_CYCLE)]
        if layer_name not in [layer.dxf.name for layer in doc.layers]:
            add_layer(doc, layer_name, color)
        layer_map[size] = layer_name
    return layer_map


def draw_rect(msp, x: float, y: float, w: float, h: float,
              layer: str = "0") -> None:
    """Draw a rectangle as a closed lightweight polyline."""
    points = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    msp.add_lwpolyline(points, close=True, dxfattribs={"layer": layer})


def draw_hatch(msp, x: float, y: float, w: float, h: float,
               layer: str = "0", color: int | None = None) -> None:
    """Draw a solid hatch (filled rectangle) for visual preview."""
    attribs = {"layer": layer}
    if color is not None:
        attribs["color"] = color
    hatch = msp.add_hatch(dxfattribs=attribs)
    hatch.paths.add_polyline_path(
        [(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
        is_closed=True,
    )


def draw_tile(msp, x: float, y: float, w: float, h: float,
              layer: str = "0", filled: bool = False) -> None:
    """Draw a tile as outline + optional solid fill."""
    draw_rect(msp, x, y, w, h, layer=layer)
    if filled:
        draw_hatch(msp, x, y, w, h, layer=layer)


def add_dimensions_label(msp, x: float, y: float, text: str,
                         height: float = 50, layer: str = "0") -> None:
    """Add a text label at the given position."""
    msp.add_text(text, height=height, dxfattribs={
        "layer": layer,
        "insert": (x, y),
    })


def save(doc: ezdxf.document.Drawing, filepath: str | Path) -> Path:
    """Save the DXF document to file."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(str(filepath))
    return filepath
