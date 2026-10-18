"""Stack bond (straight grid) and running bond (rows offset by half a tile)."""

from __future__ import annotations

from pathlib import Path

from cad_helper.patterns._sheet import PatternResult, TileSheet


def create_grid(
    width: float,
    length: float,
    tile_w: float = 600,
    tile_h: float = 300,
    gap: float = 5,
    offset_rows: bool = False,
    filled: bool = False,
    output: str | Path | None = None,
) -> PatternResult:
    """Lay ``tile_w`` x ``tile_h`` tiles over a ``length`` (X) by ``width`` (Y) area.

    With ``offset_rows`` every other row shifts by half a tile (running bond).
    Tiles crossing the edge are cut and counted separately.
    """
    name = "running_bond" if offset_rows else "grid"
    output = output or Path(f"{name}_{int(tile_w)}x{int(tile_h)}.dxf")
    sheet = TileSheet(length, width, filled)
    layer = sheet.layer(f"TILE_{int(tile_w)}x{int(tile_h)}", color=4)

    row = 0
    y = 0.0
    while y < width:
        x = -(tile_w + gap) / 2 if offset_rows and row % 2 else 0.0
        while x < length:
            sheet.place(x, y, tile_w, tile_h, layer)
            x += tile_w + gap
        y += tile_h + gap
        row += 1

    label = "Running bond" if offset_rows else "Stack bond"
    return sheet.finish(
        f"{label} {int(tile_w)}x{int(tile_h)} mm, joint {gap:g} mm, "
        f"area {length / 1000:g} x {width / 1000:g} m",
        output,
    )
