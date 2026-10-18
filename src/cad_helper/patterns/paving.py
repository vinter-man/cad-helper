"""Mixed-size paving laid in courses (ashlar style).

Each course (row) has one height. Tiles of that height alternate along the
course; courses cycle through the available heights so the joints never line
up across the whole area.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from cad_helper.core import Point, add_layers_for_tiles
from cad_helper.patterns._sheet import PatternResult, TileSheet

DEFAULT_TILES: list[Point] = [(600, 600), (600, 300), (400, 400), (300, 300), (300, 200)]


def create_paving(
    width: float,
    length: float,
    tiles: Sequence[Point] | None = None,
    gap: float = 5,
    filled: bool = False,
    output: str | Path | None = None,
) -> PatternResult:
    """Mixed paving over a ``length`` (X) by ``width`` (Y) area, one layer per tile size."""
    tiles = list(tiles or DEFAULT_TILES)
    output = output or Path(f"paving_{int(length)}x{int(width)}.dxf")
    sheet = TileSheet(length, width, filled)
    layer_of = add_layers_for_tiles(sheet.doc, tiles)

    heights = sorted({h for _, h in tiles}, reverse=True)
    courses = {h: [t for t in tiles if t[1] == h] for h in heights}

    y, course = 0.0, 0
    while y < width:
        h = heights[course % len(heights)]
        row = courses[h]
        x, i = 0.0, course  # start each course on a different tile
        while x < length:
            w = row[i % len(row)][0]
            sheet.place(x, y, w, h, layer_of[(w, h)])
            x += w + gap
            i += 1
        y += h + gap
        course += 1

    sizes = ", ".join(f"{int(w)}x{int(h)}" for w, h in tiles)
    return sheet.finish(
        f"Mixed paving ({sizes}) mm, joint {gap:g} mm, area {length / 1000:g} x {width / 1000:g} m",
        output,
    )
