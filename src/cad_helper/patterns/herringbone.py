"""90-degree herringbone.

The pattern is a lattice: every horizontal tile sits at m*(S, S) + n*(L, -L)
(L = long side + joint, S = short side + joint) and has a vertical partner at
(+L, S - L) from it. One horizontal + one vertical tile per lattice cell covers the
plane with no holes, so cutting at the area edge is all that is left to do.
"""

from __future__ import annotations

import math
from pathlib import Path

from cad_helper.patterns._sheet import PatternResult, TileSheet


def create_herringbone(
    width: float,
    length: float,
    tile_w: float = 300,
    tile_h: float = 100,
    gap: float = 5,
    filled: bool = False,
    output: str | Path | None = None,
) -> PatternResult:
    """Herringbone of ``tile_w`` (long side) x ``tile_h`` (short side) pavers."""
    if tile_h >= tile_w:
        raise ValueError("herringbone needs tile_w (long side) > tile_h (short side)")
    output = output or Path(f"herringbone_{int(tile_w)}x{int(tile_h)}.dxf")
    sheet = TileSheet(length, width, filled)
    horizontal = sheet.layer("TILE_H", color=1)
    vertical = sheet.layer("TILE_V", color=4)

    big, small = tile_w + gap, tile_h + gap
    # m runs along x+y, n along x-y; pad the ranges so the corners are covered.
    m_range = range(-2, math.ceil((length + width) / (2 * small)) + 3)
    n_range = range(math.floor(-width / (2 * big)) - 2, math.ceil(length / (2 * big)) + 3)
    for m in m_range:
        for n in n_range:
            hx, hy = m * small + n * big, m * small - n * big
            sheet.place(hx, hy, tile_w, tile_h, horizontal)
            sheet.place(hx + big, hy + small - big, tile_h, tile_w, vertical)

    return sheet.finish(
        f"Herringbone {int(tile_w)}x{int(tile_h)} mm, joint {gap:g} mm, "
        f"area {length / 1000:g} x {width / 1000:g} m",
        output,
    )
