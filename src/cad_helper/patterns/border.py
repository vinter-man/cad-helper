"""Soldier-course border (edging) around a rectangular area."""

from __future__ import annotations

from pathlib import Path

from cad_helper.core import rect_points
from cad_helper.patterns._sheet import PatternResult, TileSheet


def create_border(
    width: float,
    length: float,
    tile_w: float = 300,
    tile_h: float = 150,
    gap: float = 5,
    border_rows: int = 1,
    filled: bool = False,
    output: str | Path | None = None,
) -> PatternResult:
    """``border_rows`` rings of ``tile_w`` x ``tile_h`` edging around a ``length`` x ``width`` area.

    The long side of each tile runs along the edge. South and north courses run the
    full length; east and west courses fit between them. The paved field left inside
    is outlined with a dashed line.
    """
    output = output or Path(f"border_{int(length)}x{int(width)}.dxf")
    sheet = TileSheet(length, width, filled)
    layer = sheet.layer("BORDER_TILES", color=30)

    for ring in range(border_rows):
        o = ring * (tile_h + gap)  # inset of this ring
        x0, x1 = o, length - o
        y0, y1 = o, width - o
        if x1 - x0 < 2 * tile_h or y1 - y0 < 2 * tile_h:
            break
        ring_clip = (x0, y0, x1, y1)
        x = x0
        while x < x1:
            sheet.place(x, y0, tile_w, tile_h, layer, ring_clip)
            sheet.place(x, y1 - tile_h, tile_w, tile_h, layer, ring_clip)
            x += tile_w + gap
        y = y0 + tile_h + gap
        side_clip = (x0, y, x1, y1 - tile_h - gap)
        while y < side_clip[3]:
            sheet.place(x0, y, tile_h, tile_w, layer, side_clip)
            sheet.place(x1 - tile_h, y, tile_h, tile_w, layer, side_clip)
            y += tile_w + gap

    inset = border_rows * (tile_h + gap)
    if 2 * inset < min(width, length):
        sheet.msp.add_lwpolyline(
            rect_points(inset, inset, length - 2 * inset, width - 2 * inset),
            close=True,
            dxfattribs={"layer": "BORDER", "linetype": "DASHED", "ltscale": 10},
        )
    return sheet.finish(
        f"Border {int(tile_w)}x{int(tile_h)} mm x {border_rows} row(s), "
        f"area {length / 1000:g} x {width / 1000:g} m",
        output,
    )
