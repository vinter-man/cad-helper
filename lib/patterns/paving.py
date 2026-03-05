"""Mixed-size paving pattern generator.

Creates a paving layout with tiles of different sizes arranged in rows.
Each row is filled left-to-right, cycling through available tile sizes
with offsets between rows for a natural look.
"""

from pathlib import Path
from lib.core import (
    create_document, add_layers_for_tiles, draw_tile, save,
    add_dimensions_label, add_layer,
)


def create_paving(
    width: float,
    length: float,
    tiles: list[tuple[float, float]] | None = None,
    gap: float = 5,
    filled: bool = False,
    output: str | Path | None = None,
) -> Path:
    """Generate a mixed paving pattern.

    Args:
        width: Paving area width in mm.
        length: Paving area length in mm.
        tiles: List of (width, height) tile sizes in mm.
               Defaults to a standard mix if not provided.
        gap: Gap between tiles in mm (grout/joint width).
        filled: If True, tiles are drawn with solid fill.
        output: Output DXF file path.

    Returns:
        Path to the generated DXF file.
    """
    if tiles is None:
        tiles = [
            (600, 600),
            (600, 300),
            (400, 400),
            (300, 300),
            (300, 200),
        ]

    if output is None:
        output = Path("projects") / f"paving_{int(width)}x{int(length)}.dxf"

    doc = create_document()
    msp = doc.modelspace()

    # Create layers
    add_layer(doc, "BORDER", color=7)
    add_layer(doc, "LABELS", color=8)
    layer_map = add_layers_for_tiles(doc, tiles)

    # Draw area border
    msp.add_lwpolyline(
        [(0, 0), (length, 0), (length, width), (0, width)],
        close=True,
        dxfattribs={"layer": "BORDER"},
    )

    # Fill with tiles row by row
    y = gap
    row_index = 0

    while y < width:
        x = gap
        # Offset every other row for visual variety
        tile_start_idx = row_index % len(tiles)
        col_index = 0

        # Determine row height from first tile placed
        row_tile_idx = (tile_start_idx + col_index) % len(tiles)
        tile_w, tile_h = tiles[row_tile_idx]
        row_height = tile_h

        # Don't exceed area height
        if y + row_height > width:
            # Try to find a tile that fits
            fitted = False
            for t in tiles:
                if y + t[1] + gap <= width:
                    row_height = t[1]
                    tile_start_idx = tiles.index(t)
                    fitted = True
                    break
            if not fitted:
                break

        while x < length:
            tile_idx = (tile_start_idx + col_index) % len(tiles)
            tw, th = tiles[tile_idx]
            th = row_height  # Keep row height consistent

            # If tile doesn't fit in remaining width, try smaller tiles
            if x + tw + gap > length:
                placed = False
                for t in tiles:
                    if x + t[0] + gap <= length:
                        tw = t[0]
                        tile_idx = tiles.index(t)
                        placed = True
                        break
                if not placed:
                    break

            layer = layer_map[tiles[tile_idx]]
            draw_tile(msp, x, y, tw, th, layer=layer, filled=filled)

            x += tw + gap
            col_index += 1

        y += row_height + gap
        row_index += 1

    # Add label
    add_dimensions_label(
        msp, 0, width + 100,
        f"Paving {int(length)}x{int(width)}mm, gap={int(gap)}mm",
        height=80,
        layer="LABELS",
    )

    return save(doc, output)
