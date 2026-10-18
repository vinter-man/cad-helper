#!/usr/bin/env python3
"""School alley, Sofia: a 3 x 50 m walk between two schools.

Paving grades from light in the centre to dark at the edges using five tile
sizes (600x300, 450x300, 300x300, 300x150, 100x100). A seating pocket with a
pergola sits at each end, on opposite sides; flower beds run along the walk.

Build: uv run cad-helper build school_alley
"""

import random

from cad_helper.checks import Clearance
from cad_helper.core import add_layer, create_document, draw_rect
from cad_helper.furniture import draw_bench, draw_pergola
from cad_helper.planting import draw_flower_bed, draw_round_bed, draw_shrub
from cad_helper.site import draw_compass, draw_distance

# ── CONFIGURATION ──────────────────────────────────────────────────────────

ALLEY_LENGTH = 50_000  # X axis (east-west)
ALLEY_WIDTH = 3_000  # Y axis (north-south)
CURB_W = 150  # curb width
GAP = 5  # gap between tiles
MIN_CUT = 20  # a remainder at least this wide gets a cut tile; narrower is left as joint

# Tile sizes (width x height, mm)
TILE_SM = (100, 100)
TILE_MD = (300, 150)
TILE_SQ = (300, 300)
TILE_LG = (450, 300)
TILE_XL = (600, 300)

# Seamless vertical layout — zones defined by Y position
# Each zone has its own column grid (different tile widths don't need to align)
# Edge zones: 100x100 tiles, 3 rows = 310mm
# Transition zones: 150x300 tiles, 1 row = 300mm
# Center zone: 300-wide columns, mixed heights (600/450/300) + fillers
EDGE_H = 310  # 3 rows: 100+5+100+5+100
TRANS_H = 300  # 1 tile height

# Computed Y positions (seamless, no extra gaps between zones)
EDGE_S_Y = 0  # 0..310
TRANS_S_Y = EDGE_H + GAP  # 315..615
CENTER_Y = TRANS_S_Y + TRANS_H + GAP  # 620
EDGE_N_Y = ALLEY_WIDTH - EDGE_H  # 2690..3000
TRANS_N_Y = EDGE_N_Y - GAP - TRANS_H  # 2385..2685
CENTER_H = TRANS_N_Y - GAP - CENTER_Y  # 1760

# Seating pockets
POCKET_W = 4_000  # pocket width (along X)
POCKET_D = 3_500  # pocket depth (extending from alley)

# West pocket — extends south
WP_X = 1_000
WP_Y = -POCKET_D

# East pocket — extends north
EP_X = 45_000
EP_Y = ALLEY_WIDTH

SEED = 42  # the centre band picks tile heights at random; fixed seed = same drawing every build

PLOT_SCALE = 100
BOUNDS = (-6_000, WP_Y - 1_500, ALLEY_LENGTH, EP_Y + POCKET_D + 7_000)
CLEARANCES = [
    Clearance("FLOWER_BEDS", "TILE_*", 150, "beds stay off the paving"),
    Clearance("SHRUBS", "TILE_POCKET", 100, "shrubs outside the seating pockets"),
    Clearance("SHRUBS", "CURB", 50, "shrubs planted off the curbs"),
    Clearance("SHRUBS", "FLOWER_BEDS", 100, "shrubs and beds kept apart"),
    Clearance("FLOWER_BED_ROUND", "FLOWER_BEDS", 100, "accent bed clear of the mixborder"),
]


# ── TILE FILLING (vertical, seamless) ──────────────────────────────────────


def tile_runs(start, length, size):
    """(position, size) of the tiles along one axis: whole tiles, then one cut tile
    if the remainder is at least MIN_CUT, so the run ends flush with start + length."""
    runs = []
    pos, end = start, start + length
    while pos + size <= end:
        runs.append((pos, size))
        pos += size + GAP
    if end - pos >= MIN_CUT:
        runs.append((pos, end - pos))
    return runs


def fill_grid(msp, x0, y0, area_w, area_h, tw, th, layer):
    """Fill rectangular area with uniform tiles on a plain grid, cut to fit at the far edges."""
    for x, w in tile_runs(x0, area_w, tw):
        for y, h in tile_runs(y0, area_h, th):
            draw_rect(msp, x, y, w, h, layer=layer)


def fill_center_zone(msp, x0, y0, area_w, area_h):
    """Fill center zone with mixed large tiles + small fillers.

    300mm-wide columns. Odd columns start with a shorter tile for stagger.
    Remaining vertical space filled with 300x150 or 100x100 tiles.
    """
    large_heights = [600, 450, 300]
    large_weights = [3, 3, 4]
    y_end = y0 + area_h

    # The last column is cut to fit the end of the alley.
    for col, (x, col_w) in enumerate(tile_runs(x0, area_w, 300)):
        y = y0

        # Odd columns: start with a 150mm tile for visual stagger
        if col % 2:
            draw_rect(msp, x, y, col_w, 150, layer="TILE_MID")
            y += 150 + GAP

        # Main fill with large tiles
        while y + 300 <= y_end:
            candidates = [h for h in large_heights if y + h <= y_end]
            if not candidates:
                break
            w = large_weights[: len(candidates)]
            th = random.choices(candidates, weights=w, k=1)[0]
            draw_rect(msp, x, y, col_w, th, layer="TILE_LIGHT")
            y += th + GAP

        # Fill remaining with smaller tiles
        remaining = y_end - y
        if remaining >= 150:
            draw_rect(msp, x, y, col_w, 150, layer="TILE_MID")
            y += 150 + GAP
            remaining = y_end - y
        # Fill last bit with 100x100 tiles (2 fit in 300mm width: 100+5+100=205)
        while y + 100 <= y_end:
            draw_rect(msp, x, y, 100, 100, layer="TILE_DARK")
            draw_rect(msp, x + 105, y, 100, 100, layer="TILE_DARK")
            y += 100 + GAP
        # Close the column against the transition band with a cut tile.
        if y_end - y >= MIN_CUT:
            draw_rect(msp, x, y, col_w, y_end - y, layer="TILE_MID")


def fill_pocket(msp, px, py, pw, pd, layer):
    """Fill a pocket area with 300x300 tiles in a grid."""
    fill_grid(msp, px, py, pw, pd, 300, 300, layer)


# ── BUILD FUNCTIONS ────────────────────────────────────────────────────────


def draw_curbs(msp):
    """Draw curbs along alley and around pockets."""
    C = CURB_W

    # South curb — split for west pocket opening
    draw_rect(msp, 0, -C, WP_X, C, layer="CURB")
    draw_rect(msp, WP_X + POCKET_W, -C, ALLEY_LENGTH - WP_X - POCKET_W, C, layer="CURB")

    # North curb — split for east pocket opening
    draw_rect(msp, 0, ALLEY_WIDTH, EP_X, C, layer="CURB")
    draw_rect(msp, EP_X + POCKET_W, ALLEY_WIDTH, ALLEY_LENGTH - EP_X - POCKET_W, C, layer="CURB")

    # West pocket curbs (west, south, east sides)
    draw_rect(msp, WP_X - C, WP_Y - C, C, POCKET_D + C, layer="CURB")  # west
    draw_rect(msp, WP_X - C, WP_Y - C, POCKET_W + 2 * C, C, layer="CURB")  # south
    draw_rect(msp, WP_X + POCKET_W, WP_Y - C, C, POCKET_D + C, layer="CURB")  # east

    # East pocket curbs (west, north, east sides)
    draw_rect(msp, EP_X - C, EP_Y, C, POCKET_D + C, layer="CURB")  # west
    draw_rect(msp, EP_X - C, EP_Y + POCKET_D, POCKET_W + 2 * C, C, layer="CURB")  # north
    draw_rect(msp, EP_X + POCKET_W, EP_Y, C, POCKET_D + C, layer="CURB")  # east


def draw_tile_bands(msp):
    """Draw seamless vertical tile composition across the alley.

    5 zones from south to north, each with own column grid.
    No gaps between zones — tiles packed tightly.
    Small tiles used as fillers in center zone too.
    """
    # Edge South: 100x100 grid (Y=0..310)
    fill_grid(msp, 0, EDGE_S_Y, ALLEY_LENGTH, EDGE_H, 100, 100, "TILE_DARK")

    # Transition South: 150x300 (Y=315..615)
    fill_grid(msp, 0, TRANS_S_Y, ALLEY_LENGTH, TRANS_H, 150, 300, "TILE_MID")

    # Center: 300-wide columns with mixed heights + fillers (Y=620..2380)
    fill_center_zone(msp, 0, CENTER_Y, ALLEY_LENGTH, CENTER_H)

    # Transition North: 150x300 (Y=2385..2685)
    fill_grid(msp, 0, TRANS_N_Y, ALLEY_LENGTH, TRANS_H, 150, 300, "TILE_MID")

    # Edge North: 100x100 grid (Y=2690..3000)
    fill_grid(msp, 0, EDGE_N_Y, ALLEY_LENGTH, EDGE_H, 100, 100, "TILE_DARK")


def draw_pockets(msp, doc):
    """Draw seating pockets with paving, pergolas, benches, shrubs."""

    # ── West pocket (south side) ──
    fill_pocket(msp, WP_X, WP_Y, POCKET_W, POCKET_D, "TILE_POCKET")
    draw_pergola(msp, doc, WP_X + 250, WP_Y + 250, w=3500, h=3000)
    draw_bench(msp, doc, WP_X + 600, WP_Y + 700, w=1800, h=500)
    draw_bench(msp, doc, WP_X + 600, WP_Y + 1800, w=1800, h=500)
    # Shrubs flanking the pocket
    draw_shrub(msp, doc, WP_X - 700, WP_Y + POCKET_D / 2, 1000, label="Spiraea")
    draw_shrub(msp, doc, WP_X + POCKET_W + 700, WP_Y + POCKET_D / 2, 1000, label="Spiraea")
    draw_shrub(msp, doc, WP_X + POCKET_W / 2, WP_Y - 850, 1200, label="Berberis")

    # ── East pocket (north side) ──
    fill_pocket(msp, EP_X, EP_Y, POCKET_W, POCKET_D, "TILE_POCKET")
    draw_pergola(msp, doc, EP_X + 250, EP_Y + 250, w=3500, h=3000)
    draw_bench(msp, doc, EP_X + 600, EP_Y + 700, w=1800, h=500)
    draw_bench(msp, doc, EP_X + 600, EP_Y + 1800, w=1800, h=500)
    # Shrubs flanking the pocket
    draw_shrub(msp, doc, EP_X - 700, EP_Y + POCKET_D / 2, 1000, label="Spiraea")
    draw_shrub(msp, doc, EP_X + POCKET_W + 600, EP_Y + POCKET_D / 2, 600, label="Spiraea")
    draw_shrub(msp, doc, EP_X + POCKET_W / 2, EP_Y + POCKET_D + 850, 1200, label="Berberis")


def draw_flowers(msp, doc):
    """Draw flower beds along the alley."""
    # West side — south of alley
    draw_flower_bed(
        msp,
        doc,
        [(7_500, -1_800), (10_500, -1_800), (10_500, -400), (7_500, -400)],
        name="LAVANDULA",
    )

    # Center-south
    draw_flower_bed(
        msp,
        doc,
        [(21_000, -1_500), (26_000, -1_500), (26_000, -400), (21_000, -400)],
        name="MIXBORDER",
    )

    # Center-north
    draw_flower_bed(
        msp,
        doc,
        [
            (23_000, ALLEY_WIDTH + 400),
            (28_000, ALLEY_WIDTH + 400),
            (28_000, ALLEY_WIDTH + 1_500),
            (23_000, ALLEY_WIDTH + 1_500),
        ],
        name="MIXBORDER",
    )

    # East side — north of alley
    draw_flower_bed(
        msp,
        doc,
        [
            (40_000, ALLEY_WIDTH + 400),
            (43_000, ALLEY_WIDTH + 400),
            (43_000, ALLEY_WIDTH + 1_800),
            (40_000, ALLEY_WIDTH + 1_800),
        ],
        name="ROSES & GRASSES",
    )

    # Round accent bed — center north
    draw_round_bed(
        msp,
        doc,
        cx=25_000,
        cy=ALLEY_WIDTH + 2_800,
        diameter=2_000,
        name="ACCENT BED",
        layer="FLOWER_BED_ROUND",
    )


def draw_labels(msp, doc):
    """Add project title and dimension labels."""
    msp.add_text(
        "SCHOOL ALLEY",
        height=600,
        dxfattribs={
            "layer": "LABELS",
            "insert": (18_000, ALLEY_WIDTH + 6_000),
        },
    )
    msp.add_text(
        "Gradient Tile Composition — 3m x 50m",
        height=300,
        dxfattribs={
            "layer": "LABELS",
            "insert": (15_000, ALLEY_WIDTH + 5_200),
        },
    )

    draw_compass(msp, doc, x=-3_000, y=ALLEY_WIDTH + 1_500, size=1_500)
    draw_distance(msp, doc, (0, ALLEY_WIDTH), (0, 0), offset=-1_200)
    draw_distance(msp, doc, (0, WP_Y - CURB_W), (ALLEY_LENGTH, WP_Y - CURB_W), offset=-1_000)

    # Band labels (along west edge)
    msp.add_text(
        "DARK (100x100)",
        height=150,
        dxfattribs={
            "layer": "LABELS",
            "insert": (-5_000, 80),
        },
    )
    msp.add_text(
        "MID (150x300)",
        height=150,
        dxfattribs={
            "layer": "LABELS",
            "insert": (-5_000, 350),
        },
    )
    msp.add_text(
        "LIGHT (300x mixed)",
        height=150,
        dxfattribs={
            "layer": "LABELS",
            "insert": (-5_000, 1_400),
        },
    )


# ── MAIN BUILD ─────────────────────────────────────────────────────────────


def build():
    random.seed(SEED)
    doc = create_document()
    msp = doc.modelspace()

    # Layers
    add_layer(doc, "CURB", 8)
    add_layer(doc, "TILE_DARK", 250)
    add_layer(doc, "TILE_MID", 252)
    add_layer(doc, "TILE_LIGHT", 254)
    add_layer(doc, "TILE_POCKET", 253)
    add_layer(doc, "LABELS", 7)

    # Alley boundary (reference outline)
    msp.add_lwpolyline(
        [(0, 0), (ALLEY_LENGTH, 0), (ALLEY_LENGTH, ALLEY_WIDTH), (0, ALLEY_WIDTH)],
        close=True,
        dxfattribs={"layer": "CURB", "const_width": 20},
    )

    # Phase 1: Curbs
    draw_curbs(msp)

    # Phase 2: Tile composition
    draw_tile_bands(msp)

    # Phase 3: Seating pockets
    draw_pockets(msp, doc)

    # Phase 4: Flower beds & shrubs
    draw_flowers(msp, doc)

    # Phase 5: Labels
    draw_labels(msp, doc)

    return doc
