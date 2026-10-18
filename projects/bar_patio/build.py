"""Bar patio, Veliko Tarnovo: a 4 x 4 m evening terrace in front of a bar.

Old-Mexico-meets-90s-Bulgaria planting in containers: grape vines in troughs hide
the low concrete walls, opuntia in terracotta pots hold the corners, rosemary and
lavender flank the bar door. A 1 m aisle runs from the entrance steps to the door.

Build: uv run cad-helper build bar_patio
"""

from cad_helper.checks import Clearance
from cad_helper.core import create_document
from cad_helper.furniture import draw_rect_table
from cad_helper.lighting import draw_path_light
from cad_helper.planting import draw_planter, draw_shrub
from cad_helper.site import draw_compass, draw_distance, draw_house, draw_steps, draw_wall
from cad_helper.zones import draw_rect_zone

# ─── Configuration (mm; origin = south-west corner of the patio) ────────────

PATIO_W, PATIO_L = 4_000, 4_000
BAR_W, BAR_L = 8_000, 4_000  # bar interior, north of the patio
DOOR_X = PATIO_W / 2  # bar door, on the patio's centre line
WALL_T = 200  # low concrete side walls, ~800 mm high

# Steps: two treads up from the street, centred on the aisle.
STEPS_W, TREAD = 1_000, 300

# Square bistro tables, two chairs each (north and south).
TABLE = 700
CHAIR_D = 400
TABLE_COLS = (1_150, 2_850)  # x centres, leaving a 1 m aisle between
TABLE_ROWS = (820, 2_800)  # y centres

VINE_TROUGH_W = 300  # troughs along both walls
VINE_TROUGH = (400, PATIO_L - 400)  # y from-to

# Herb planters either side of the door: 50 mm off the facade, clear of the
# outward-opening door leaf (hinged at DOOR_X - 450) and of the chairs below.
HERB_W, HERB_D = 300, 250
HERB_X = (DOOR_X - 900, DOOR_X + 600)  # west edges
HERB_Y = PATIO_L - 50 - HERB_D

BOUNDS = (-WALL_T, -2 * TREAD, BAR_W, PATIO_L + BAR_L)
PLOT_SCALE = 50
CLEARANCES = [
    Clearance("FURNITURE", "PLANTERS", 100, "chairs clear of the troughs"),
    Clearance("FURNITURE", "PLANTS", 100, "cacti out of reach of guests"),
    Clearance("FURNITURE", "WALLS", 100, "room to pull a chair out"),
    Clearance("FURNITURE", "HERBS", 100, "door approach kept clear"),
    Clearance("HOUSE", "HERBS", 50, "door leaf and facade clear of the herb planters"),
]


def build():
    doc = create_document()
    msp = doc.modelspace()

    # ── 1. Site ──────────────────────────────────────────────────────────
    draw_rect_zone(
        msp,
        doc,
        x=0,
        y=0,
        w=PATIO_W,
        h=PATIO_L,
        name="PATIO",
        color=253,
        hatch_pattern="AR-SAND",
        hatch_scale=8,
    )
    draw_house(
        msp,
        doc,
        x=0,
        y=PATIO_L,
        w=BAR_W,
        h=BAR_L,
        label="BAR",
        entrance_side="south",
        entrance_width=900,
        entrance_center=DOOR_X,
    )
    draw_wall(
        msp,
        doc,
        (-WALL_T / 2, 0),
        (-WALL_T / 2, PATIO_L),
        thickness=WALL_T,
        label="CONCRETE WALL h=800",
    )
    draw_wall(
        msp, doc, (PATIO_W + WALL_T / 2, 0), (PATIO_W + WALL_T / 2, PATIO_L), thickness=WALL_T
    )
    draw_steps(
        msp,
        doc,
        x=DOOR_X - STEPS_W / 2,
        y=-2 * TREAD,
        w=STEPS_W,
        tread=TREAD,
        count=2,
        label="2 STEPS FROM STREET",
    )
    draw_compass(msp, doc, x=PATIO_W + 1_200, y=PATIO_L - 1_500, size=800)
    draw_distance(msp, doc, (0, 0), (PATIO_W, 0), offset=-1_000, text_height=150)
    draw_distance(
        msp, doc, (PATIO_W + WALL_T, 0), (PATIO_W + WALL_T, PATIO_L), offset=-600, text_height=150
    )

    # ── 2. Furniture ─────────────────────────────────────────────────────
    n = 0
    for cy in TABLE_ROWS:
        for cx in TABLE_COLS:
            n += 1
            draw_rect_table(
                msp,
                doc,
                cx,
                cy,
                w=TABLE,
                h=TABLE,
                chairs="NS",
                chair_diameter=CHAIR_D,
                label=f"T{n}",
            )

    # ── 3. Planting ──────────────────────────────────────────────────────
    y0, y1 = VINE_TROUGH
    draw_planter(msp, doc, 0, y0, VINE_TROUGH_W, y1 - y0, label="VITIS VINIFERA")
    draw_planter(
        msp, doc, PATIO_W - VINE_TROUGH_W, y0, VINE_TROUGH_W, y1 - y0, label="VITIS VINIFERA"
    )
    for cx, cy in [
        (200, 200),
        (PATIO_W - 200, 200),
        (200, PATIO_L - 200),
        (PATIO_W - 200, PATIO_L - 200),
    ]:
        draw_shrub(msp, doc, cx=cx, cy=cy, diameter=380, layer="PLANTS", color=3)
    for hx in HERB_X:
        draw_planter(msp, doc, hx, HERB_Y, HERB_W, HERB_D, layer="HERBS", color=200)
        draw_shrub(msp, doc, hx + HERB_W / 2, HERB_Y + HERB_D / 2, 250, layer="HERBS", color=200)

    # ── 4. Lighting: one lantern over the door ──────────────────────────
    draw_path_light(msp, doc, cx=DOOR_X, cy=PATIO_L + 250)

    return doc
