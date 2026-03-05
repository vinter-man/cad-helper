"""Herringbone (елочка) tile pattern generator.

Creates a herringbone pattern from rectangular tiles. Tiles are placed
alternately horizontal and vertical in a zigzag arrangement.
"""

import math
from pathlib import Path
from lib.core import (
    create_document, add_layer, draw_tile, save, add_dimensions_label,
)


def create_herringbone(
    width: float,
    length: float,
    tile_w: float = 300,
    tile_h: float = 100,
    gap: float = 5,
    angle: float = 90,
    filled: bool = False,
    output: str | Path | None = None,
) -> Path:
    """Generate a herringbone tile pattern.

    Args:
        width: Area width in mm.
        length: Area length in mm.
        tile_w: Tile long side in mm.
        tile_h: Tile short side in mm.
        gap: Gap between tiles in mm.
        angle: Herringbone angle (90 for standard).
        filled: If True, tiles are drawn with solid fill.
        output: Output DXF file path.

    Returns:
        Path to the generated DXF file.
    """
    if output is None:
        output = Path("projects") / f"herringbone_{int(tile_w)}x{int(tile_h)}.dxf"

    doc = create_document()
    msp = doc.modelspace()

    add_layer(doc, "TILE_H", color=1)
    add_layer(doc, "TILE_V", color=4)
    add_layer(doc, "BORDER", color=7)
    add_layer(doc, "LABELS", color=8)

    # Draw area border
    msp.add_lwpolyline(
        [(0, 0), (length, 0), (length, width), (0, width)],
        close=True,
        dxfattribs={"layer": "BORDER"},
    )

    # Herringbone: pairs of tiles — one horizontal, one vertical.
    # A "unit" is one H tile + one V tile stacked.
    # Unit size: tile_w x (tile_h * 2 + gap)
    unit_step_x = tile_w + gap
    unit_step_y = tile_h * 2 + gap

    y = gap
    row = 0
    while y < width:
        x_start = gap + (row % 2) * (tile_w / 2 + gap / 2)
        x = x_start

        while x < length:
            # Horizontal tile
            if y + tile_h <= width and x + tile_w <= length:
                draw_tile(msp, x, y, tile_w, tile_h,
                         layer="TILE_H", filled=filled)

            # Vertical tile (rotated: swap w and h), placed to the right-bottom
            vy = y + tile_h + gap
            vx = x
            if vy + tile_w <= width and vx + tile_h <= length:
                draw_tile(msp, vx, vy, tile_h, tile_w,
                         layer="TILE_V", filled=filled)

            x += unit_step_x

        y += unit_step_y
        row += 1

    add_dimensions_label(
        msp, 0, width + 100,
        f"Herringbone {int(tile_w)}x{int(tile_h)}mm, area {int(length)}x{int(width)}mm",
        height=80,
        layer="LABELS",
    )

    return save(doc, output)
