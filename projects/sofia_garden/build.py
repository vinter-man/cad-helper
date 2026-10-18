"""Sofia garden: a small Japanese garden on a 12 x 18 m plot.

Brief: brief.md - plan: plan.md - review: review.md
Build: uv run cad-helper build sofia_garden
"""

import math

from cad_helper.checks import Clearance
from cad_helper.core import create_document
from cad_helper.furniture import draw_bbq_zone, draw_fire_pit
from cad_helper.japanese import (
    draw_moss_area,
    draw_niwaki,
    draw_stepping_stones,
    draw_stone_lantern,
)
from cad_helper.lighting import draw_lights_along_path
from cad_helper.planting import draw_hedge, draw_lawn, draw_tree
from cad_helper.site import draw_compass, draw_fence, draw_house, draw_plot
from cad_helper.water import draw_pond
from cad_helper.zones import draw_rect_zone, draw_zone

# ─── Configuration (mm; origin = south-west corner, X east, Y north) ────────

PLOT_W = 12_000
PLOT_L = 18_000

HOUSE_X, HOUSE_Y, HOUSE_W, HOUSE_H = 1_000, 11_500, 10_000, 6_000
DECK_X, DECK_Y, DECK_W, DECK_H = 1_500, 9_100, 7_000, 2_400  # timber terrace (engawa)
GATE_X = 9_800

POND_C = (4_300, 5_900)
POND_R = (2_600, 1_700)
FIRE_PIT = (2_700, 2_000)

PATH = [(GATE_X, 300), (9_600, 2_500), (8_800, 5_200), (8_300, 7_600), (7_800, 8_900)]

BOUNDS = (0, 0, PLOT_W, PLOT_L)
CLEARANCES = [
    Clearance("HOUSE", "POND*", 3_000, "water away from foundations"),
    Clearance("BBQ", "MAPLE", 3_000, "no branches over the grill"),
    Clearance("BBQ", "NIWAKI", 3_000, "no branches over the grill"),
    Clearance("STEPPING_STONES*", "POND*", 300, "dry path"),
    Clearance("FIRE_PIT", "NIWAKI", 3_000, "sparks vs pine crown"),
    Clearance("FIRE_PIT", "MAPLE", 3_000, "sparks vs maple crown"),
    Clearance("FIRE_PIT", "HOUSE", 4_000, "smoke and sparks away from the house"),
    Clearance("FIRE_PIT_SEATING", "POND*", 300, "bench stays on dry ground"),
    Clearance("LAWN", "POND*", 100, "lawn edge stays dry"),
    Clearance("ZONE_GRAVEL", "POND*", 100, "gravel does not spill into the pond"),
]


def build():
    doc = create_document()
    msp = doc.modelspace()

    # ── 1. Site ──────────────────────────────────────────────────────────
    draw_plot(msp, doc, width=PLOT_W, length=PLOT_L)
    draw_house(msp, doc, x=HOUSE_X, y=HOUSE_Y, w=HOUSE_W, h=HOUSE_H, entrance_width=1_000)
    draw_fence(
        msp,
        doc,
        width=PLOT_W,
        length=PLOT_L,
        gates=[{"side": "south", "center": GATE_X, "opening": 1_200, "label": "GATE"}],
    )
    draw_compass(msp, doc, x=-2_200, y=PLOT_L - 2_500, size=1_200)

    # ── 2. Terrace and grill ─────────────────────────────────────────────
    draw_rect_zone(
        msp,
        doc,
        x=DECK_X,
        y=DECK_Y,
        w=DECK_W,
        h=DECK_H,
        name="DECK",
        color=33,
        hatch_pattern="LINE",
        hatch_scale=25,
    )
    draw_bbq_zone(
        msp,
        doc,
        x=9_000,
        y=9_300,
        grill_w=1_200,
        grill_h=600,
        counter_w=1_900,
        counter_h=600,
        layout="L",
    )

    # ── 3. Water and fire ───────────────────────────────────────────────
    draw_pond(
        msp, doc, cx=POND_C[0], cy=POND_C[1], rx=POND_R[0], ry=POND_R[1], rotation=-8, label="POND"
    )
    # Gravel circle under the fire pit and its bench.
    gravel = [
        (
            FIRE_PIT[0] + 1_980 * math.cos(a / 20 * math.tau),
            FIRE_PIT[1] + 1_980 * math.sin(a / 20 * math.tau),
        )
        for a in range(20)
    ]
    draw_zone(
        msp,
        doc,
        gravel,
        name="GRAVEL",
        color=253,
        hatch_pattern="AR-SAND",
        hatch_scale=6,
        label=False,
    )
    draw_fire_pit(msp, doc, cx=FIRE_PIT[0], cy=FIRE_PIT[1], diameter=1_000, seat_radius=1_500)

    # ── 4. Path and light ────────────────────────────────────────────────
    draw_stepping_stones(msp, doc, PATH, stone_size=450, spacing=250)
    draw_stepping_stones(
        msp,
        doc,
        [(8_200, 4_400), (6_400, 3_200), (5_200, 1_700), (4_400, 1_100)],
        stone_size=400,
        spacing=300,
        layer="STEPPING_STONES_FIRE",
    )
    draw_lights_along_path(msp, doc, [(x + 800, y) for x, y in PATH[1:]], spacing=3_000)
    draw_stone_lantern(msp, doc, cx=6_600, cy=7_000, size=550)

    # ── 5. Planting ──────────────────────────────────────────────────────
    draw_tree(
        msp,
        doc,
        cx=1_600,
        cy=7_800,
        crown_diameter=2_200,
        label="Acer palmatum",
        layer="MAPLE",
        color=1,
    )
    draw_niwaki(msp, doc, cx=7_300, cy=1_800, crown_diameter=1_800, num_clouds=4, label="Pine")
    draw_tree(
        msp,
        doc,
        cx=9_900,
        cy=4_800,
        crown_diameter=2_600,
        label="Prunus serrulata",
        layer="SAKURA",
        color=220,
    )
    draw_hedge(
        msp,
        doc,
        points=[(11_500, 1_200), (11_500, 11_000)],
        hedge_width=600,
        layer="HEDGE_TAXUS",
        color=3,
    )
    draw_lawn(
        msp,
        doc,
        [
            (600, 8_000),
            (2_400, 8_150),
            (4_300, 8_350),
            (6_300, 8_400),
            (7_100, 8_900),
            (600, 8_900),
        ],
    )
    draw_moss_area(msp, doc, [(6_300, 600), (8_300, 600), (8_200, 1_700), (6_200, 1_300)])

    return doc
