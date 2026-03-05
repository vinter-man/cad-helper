"""Border/frame pattern generator.

Creates a rectangular border (frame) made of tiles around a given area.
Useful for edging around paving, flower beds, paths, etc.
"""

from pathlib import Path
from lib.core import (
    create_document, add_layer, draw_tile, save, add_dimensions_label,
)


def create_border(
    width: float,
    length: float,
    tile_w: float = 300,
    tile_h: float = 150,
    gap: float = 5,
    border_rows: int = 1,
    filled: bool = False,
    output: str | Path | None = None,
) -> Path:
    """Generate a tile border around a rectangular area.

    Args:
        width: Total area width in mm (including border).
        length: Total area length in mm (including border).
        tile_w: Border tile width in mm (along the border direction).
        tile_h: Border tile height in mm (perpendicular to border).
        gap: Gap between tiles in mm.
        border_rows: Number of border rows (thickness).
        filled: If True, tiles are drawn with solid fill.
        output: Output DXF file path.

    Returns:
        Path to the generated DXF file.
    """
    if output is None:
        output = Path("projects") / f"border_{int(width)}x{int(length)}.dxf"

    doc = create_document()
    msp = doc.modelspace()

    add_layer(doc, "BORDER_TILES", color=30)
    add_layer(doc, "AREA_OUTLINE", color=7)
    add_layer(doc, "LABELS", color=8)

    # Outer boundary
    msp.add_lwpolyline(
        [(0, 0), (length, 0), (length, width), (0, width)],
        close=True,
        dxfattribs={"layer": "AREA_OUTLINE"},
    )

    for row in range(border_rows):
        offset = row * (tile_h + gap)

        # Bottom edge (left to right)
        x = gap + offset
        y = gap + offset
        while x + tile_w <= length - gap - offset:
            draw_tile(msp, x, y, tile_w, tile_h,
                     layer="BORDER_TILES", filled=filled)
            x += tile_w + gap

        # Top edge (left to right)
        x = gap + offset
        y = width - gap - offset - tile_h
        while x + tile_w <= length - gap - offset:
            draw_tile(msp, x, y, tile_w, tile_h,
                     layer="BORDER_TILES", filled=filled)
            x += tile_w + gap

        # Left edge (bottom to top, excluding corners)
        x = gap + offset
        y = gap + offset + tile_h + gap
        while y + tile_w <= width - gap - offset - tile_h - gap:
            # Rotate tile for vertical placement
            draw_tile(msp, x, y, tile_h, tile_w,
                     layer="BORDER_TILES", filled=filled)
            y += tile_w + gap

        # Right edge (bottom to top, excluding corners)
        x = length - gap - offset - tile_h
        y = gap + offset + tile_h + gap
        while y + tile_w <= width - gap - offset - tile_h - gap:
            draw_tile(msp, x, y, tile_h, tile_w,
                     layer="BORDER_TILES", filled=filled)
            y += tile_w + gap

    # Inner area outline
    border_thickness = border_rows * (tile_h + gap) + gap
    if border_thickness * 2 < min(width, length):
        inner = [
            (border_thickness, border_thickness),
            (length - border_thickness, border_thickness),
            (length - border_thickness, width - border_thickness),
            (border_thickness, width - border_thickness),
        ]
        msp.add_lwpolyline(inner, close=True,
                           dxfattribs={"layer": "AREA_OUTLINE", "linetype": "DASHED"})

    add_dimensions_label(
        msp, 0, width + 100,
        f"Border {int(length)}x{int(width)}mm, tile {int(tile_w)}x{int(tile_h)}mm",
        height=80,
        layer="LABELS",
    )

    return save(doc, output)
