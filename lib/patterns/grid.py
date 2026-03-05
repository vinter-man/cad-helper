"""Regular grid tile pattern generator.

Creates a uniform grid of same-sized tiles with configurable gap.
Supports optional offset (brick-like) pattern for alternating rows.
"""

from pathlib import Path
from lib.core import (
    create_document, add_layer, draw_tile, save, add_dimensions_label,
)


def create_grid(
    width: float,
    length: float,
    tile_w: float = 600,
    tile_h: float = 300,
    gap: float = 5,
    offset_rows: bool = False,
    filled: bool = False,
    output: str | Path | None = None,
) -> Path:
    """Generate a regular grid of tiles.

    Args:
        width: Area width in mm.
        length: Area length in mm.
        tile_w: Tile width in mm.
        tile_h: Tile height in mm.
        gap: Gap between tiles in mm.
        offset_rows: If True, every other row is offset by half a tile width
                     (brick/running bond pattern).
        filled: If True, tiles are drawn with solid fill.
        output: Output DXF file path.

    Returns:
        Path to the generated DXF file.
    """
    if output is None:
        suffix = "_offset" if offset_rows else ""
        output = Path("projects") / f"grid_{int(tile_w)}x{int(tile_h)}{suffix}.dxf"

    doc = create_document()
    msp = doc.modelspace()

    add_layer(doc, "TILES", color=4)
    add_layer(doc, "BORDER", color=7)
    add_layer(doc, "LABELS", color=8)

    # Draw area border
    msp.add_lwpolyline(
        [(0, 0), (length, 0), (length, width), (0, width)],
        close=True,
        dxfattribs={"layer": "BORDER"},
    )

    y = gap
    row = 0
    while y + tile_h <= width:
        x_offset = (tile_w / 2 + gap / 2) if (offset_rows and row % 2 == 1) else 0
        x = gap + x_offset

        while x + tile_w <= length:
            draw_tile(msp, x, y, tile_w, tile_h, layer="TILES", filled=filled)
            x += tile_w + gap

        # Handle partial tile at end of offset rows
        if offset_rows and row % 2 == 1 and gap < x_offset:
            # Draw partial tile at the start
            partial_w = tile_w / 2 - gap / 2
            if partial_w > 0:
                draw_tile(msp, gap, y, partial_w, tile_h, layer="TILES", filled=filled)

        y += tile_h + gap
        row += 1

    pattern_name = "Running bond" if offset_rows else "Grid"
    add_dimensions_label(
        msp, 0, width + 100,
        f"{pattern_name} {int(tile_w)}x{int(tile_h)}mm, area {int(length)}x{int(width)}mm",
        height=80,
        layer="LABELS",
    )

    return save(doc, output)
