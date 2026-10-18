"""Backyard: Japanese garden on a 25 x 40 m plot.

Design principles: asymmetry (odd numbers, off-centre placement), layered depth,
wabi-sabi imperfection, ma (intentional empty space), and stone and water as the
core elements. Water rises at a spring by the house, runs south under the bridge
on the tea path and fills the koi pond; the dry garden by the gate stays dry.

Build: uv run cad-helper build backyard
"""

from cad_helper.checks import Clearance
from cad_helper.core import create_document
from cad_helper.furniture import draw_bench, draw_pergola
from cad_helper.japanese import (
    draw_bamboo_fence,
    draw_moss_area,
    draw_niwaki,
    draw_stepping_stones,
    draw_stone_lantern,
    draw_torii,
    draw_tsukubai,
    draw_zen_garden,
)
from cad_helper.lighting import draw_spotlight
from cad_helper.planting import draw_hedge, draw_shrub, draw_tree
from cad_helper.site import draw_compass, draw_fence, draw_house, draw_plot
from cad_helper.water import draw_bridge, draw_pond, draw_stream
from cad_helper.zones import draw_rect_zone, draw_zone

# ─── Configuration (mm; origin = south-west corner, X east, Y north) ────────

PLOT_W = 25_000
PLOT_L = 40_000

# House 10 x 12 m, pushed north-east so the garden opens to the south-west.
HOUSE_X, HOUSE_Y = 9_000, 23_000
HOUSE_W, HOUSE_H = 10_000, 12_000

# One pedestrian gate, deliberately off-centre.
GATE_X = PLOT_W / 2 + 2_000
GATES = [{"side": "south", "center": GATE_X, "opening": 1_500, "label": "MAIN GATE"}]

# Engawa: covered timber veranda along the south facade.
ENGAWA_X, ENGAWA_Y = HOUSE_X - 500, HOUSE_Y - 2_500
ENGAWA_W, ENGAWA_H = HOUSE_W + 1_000, 2_500

# Koi pond, west-centre.
POND_CX, POND_CY = 6_500, 15_000
POND_RX, POND_RY = 3_500, 2_500

# Dry garden (karesansui) in the south-west corner, seen from the gate.
ZEN_X, ZEN_Y = 1_500, 2_500
ZEN_W, ZEN_H = 9_000, 7_000

# Tea garden (roji) in the north-west corner, behind a bamboo fence.
TEA_X, TEA_Y = 1_000, PLOT_L - 8_000
TEA_W, TEA_H = 7_000, 6_000
TEA_GATE = (4_200, 5_400)  # opening in the bamboo fence, x from-to

# Stream: spring by the house -> under the bridge -> into the pond.
STREAM = [(5_800, 27_500), (4_600, 25_200), (4_400, 22_600), (5_300, 18_000), (5_700, 16_600)]
BRIDGE_C = (4_500, 23_900)  # on the stream, where the tea path crosses
BRIDGE_SPAN = 1_800

BOUNDS = (0, 0, PLOT_W, PLOT_L)
CLEARANCES = [
    Clearance("HOUSE", "POND*", 3_000, "water away from foundations"),
    Clearance("HOUSE", "SAKURA", 2_000, "crown clear of the walls"),
    Clearance("STEPPING_STONES*", "POND*", 300, "dry approach path"),
    Clearance("STEPPING_STONES*", "STREAM", 150, "stones stay off the water"),
    Clearance("STEPPING_STONES*", "FUJIDANA", 300, "path passes beside the pergola"),
]


def build():
    doc = create_document()
    msp = doc.modelspace()

    # ── 1. Site ──────────────────────────────────────────────────────────
    draw_plot(msp, doc, width=PLOT_W, length=PLOT_L)
    draw_house(
        msp,
        doc,
        x=HOUSE_X,
        y=HOUSE_Y,
        w=HOUSE_W,
        h=HOUSE_H,
        entrance_side="south",
        entrance_width=1_800,
    )
    draw_fence(msp, doc, width=PLOT_W, length=PLOT_L, gates=GATES)
    draw_compass(msp, doc, x=-2_500, y=PLOT_L - 2_000)

    # ── 2. Zones ─────────────────────────────────────────────────────────
    draw_rect_zone(
        msp,
        doc,
        x=ENGAWA_X,
        y=ENGAWA_Y,
        w=ENGAWA_W,
        h=ENGAWA_H,
        name="ENGAWA",
        color=33,
        hatch_pattern="LINE",
        hatch_scale=30,
    )
    draw_zone(
        msp,
        doc,
        points=[
            (TEA_X, TEA_Y),
            (TEA_X + TEA_W, TEA_Y),
            (TEA_X + TEA_W - 1_000, TEA_Y + TEA_H),
            (TEA_X, TEA_Y + TEA_H),
        ],
        name="TEA GARDEN",
        color=83,
        hatch_pattern="ANSI37",
        hatch_scale=120,
    )

    # ── 3. Dry garden: a 3-stone group (heaven, earth, man) and a pair ──
    draw_zen_garden(
        msp,
        doc,
        [
            (ZEN_X, ZEN_Y),
            (ZEN_X + ZEN_W, ZEN_Y),
            (ZEN_X + ZEN_W - 500, ZEN_Y + ZEN_H),
            (ZEN_X + 500, ZEN_Y + ZEN_H),
        ],
        stones=[
            {"cx": ZEN_X + 3_000, "cy": ZEN_Y + 3_900, "rx": 500, "ry": 350, "rotation": 15},
            {
                "cx": ZEN_X + 3_750,
                "cy": ZEN_Y + 3_350,
                "rx": 330,
                "ry": 240,
                "rotation": -20,
                "ripples": 0,
            },
            {
                "cx": ZEN_X + 2_420,
                "cy": ZEN_Y + 3_300,
                "rx": 240,
                "ry": 170,
                "rotation": 45,
                "ripples": 0,
            },
            {
                "cx": ZEN_X + 6_800,
                "cy": ZEN_Y + 4_800,
                "rx": 420,
                "ry": 300,
                "rotation": -10,
                "ripples": 2,
            },
            {
                "cx": ZEN_X + 7_350,
                "cy": ZEN_Y + 4_350,
                "rx": 200,
                "ry": 150,
                "rotation": 30,
                "ripples": 0,
            },
        ],
        rake_spacing=120,
        rake_angle=0,
    )

    # ── 4. Water ─────────────────────────────────────────────────────────
    draw_pond(
        msp,
        doc,
        cx=POND_CX,
        cy=POND_CY,
        rx=POND_RX,
        ry=POND_RY,
        rotation=15,
        irregular=True,
        label="KOI POND",
    )
    draw_stream(msp, doc, waypoints=STREAM, width=550)
    draw_bridge(
        msp,
        doc,
        cx=BRIDGE_C[0],
        cy=BRIDGE_C[1],
        width=BRIDGE_SPAN,
        depth=1_000,
        arched=True,
        rotation=0,
    )

    # ── 5. Paths (stepping stones) ───────────────────────────────────────
    bridge_w = (BRIDGE_C[0] - BRIDGE_SPAN / 2 - 200, BRIDGE_C[1])
    bridge_e = (BRIDGE_C[0] + BRIDGE_SPAN / 2 + 200, BRIDGE_C[1])

    # Gate -> torii -> past the dry garden -> engawa steps.
    main_path = [
        (GATE_X, 300),
        (GATE_X + 300, 3_000),
        (GATE_X + 1_000, 7_000),
        (GATE_X + 800, 12_000),
        (GATE_X + 300, 16_500),
        (HOUSE_X + 5_000, ENGAWA_Y - 300),
    ]
    draw_stepping_stones(msp, doc, main_path, stone_size=450, spacing=250)

    # Engawa -> bridge -> round the spring -> through the bamboo fence to the tsukubai.
    tea_path_east = [(ENGAWA_X - 200, ENGAWA_Y + 1_200), (6_900, 23_300), bridge_e]
    tea_path_west = [
        bridge_w,
        (2_700, 25_200),
        (2_800, 28_500),
        (3_900, 30_700),
        (sum(TEA_GATE) / 2, TEA_Y - 200),
        (sum(TEA_GATE) / 2 - 200, TEA_Y + 1_600),
    ]
    draw_stepping_stones(
        msp, doc, tea_path_east, stone_size=400, spacing=300, layer="STEPPING_STONES_TEA"
    )
    draw_stepping_stones(
        msp, doc, tea_path_west, stone_size=400, spacing=300, layer="STEPPING_STONES_TEA"
    )

    # Main path -> along the north shore of the pond -> engawa.
    pond_path = [(GATE_X + 300, 17_200), (12_800, 18_000), (10_500, 18_700), (8_700, 19_700)]
    draw_stepping_stones(
        msp, doc, pond_path, stone_size=400, spacing=250, layer="STEPPING_STONES_POND"
    )

    # ── 6. Structures ────────────────────────────────────────────────────
    draw_torii(msp, doc, cx=GATE_X + 100, cy=1_800, width=2_200)

    # Wisteria pergola (fujidana) on the east shore, bench facing the water.
    draw_pergola(msp, doc, x=10_800, y=12_300, w=3_000, h=2_600, layer="FUJIDANA", color=200)
    draw_bench(
        msp, doc, x=11_300, y=13_000, w=2_000, h=500, rotation=90, layer="FURNITURE", color=33
    )

    draw_tsukubai(msp, doc, cx=TEA_X + 2_200, cy=TEA_Y + 3_200, diameter=800)

    # ── 7. Planting ──────────────────────────────────────────────────────
    # Niwaki pines: three specimens of different size, never in a row.
    draw_niwaki(
        msp, doc, cx=1_900, cy=19_600, crown_diameter=3_000, num_clouds=5, label="Black Pine 1"
    )
    draw_niwaki(
        msp, doc, cx=8_200, cy=10_900, crown_diameter=2_500, num_clouds=4, label="Black Pine 2"
    )
    draw_niwaki(
        msp,
        doc,
        cx=TEA_X + TEA_W - 1_300,
        cy=TEA_Y + TEA_H - 900,
        crown_diameter=2_000,
        num_clouds=3,
        label="Pine 3",
    )

    # Japanese maples leaning over the water.
    draw_tree(
        msp,
        doc,
        cx=10_300,
        cy=16_900,
        crown_diameter=2_500,
        label="Maple 1",
        layer="MAPLES",
        color=1,
    )
    draw_tree(
        msp,
        doc,
        cx=2_400,
        cy=13_300,
        crown_diameter=2_000,
        label="Maple 2",
        layer="MAPLES",
        color=1,
    )

    # Sakura along the east fence.
    for i in range(3):
        draw_tree(
            msp,
            doc,
            cx=PLOT_W - 3_000,
            cy=8_000 + i * 6_000,
            crown_diameter=3_500,
            label=f"Sakura {i + 1}",
            layer="SAKURA",
            color=220,
        )

    # Bamboo grove screening the north-east corner.
    for i in range(7):
        draw_shrub(
            msp,
            doc,
            cx=PLOT_W - 2_000 + (i % 3) * 500,
            cy=PLOT_L - 2_000 - i * 800,
            diameter=800,
            layer="BAMBOO",
            color=3,
        )

    # Azalea mounds at both ends of the engawa (3 + 2).
    azaleas = [
        (7_300, 21_300),
        (6_400, 22_100),
        (7_600, 22_500),
        (ENGAWA_X + ENGAWA_W + 900, ENGAWA_Y + 600),
        (ENGAWA_X + ENGAWA_W + 1_900, ENGAWA_Y - 200),
    ]
    for i, (ax, ay) in enumerate(azaleas):
        draw_shrub(
            msp,
            doc,
            cx=ax,
            cy=ay,
            diameter=1_000 + (i % 3) * 250,
            label="Azalea" if i == 0 else "",
            layer="AZALEAS",
            color=220,
        )

    # Moss under the west pine and inside the roji.
    draw_moss_area(
        msp, doc, [(600, 17_600), (3_100, 18_000), (3_600, 20_400), (2_600, 21_700), (700, 21_500)]
    )
    draw_moss_area(
        msp,
        doc,
        [
            (TEA_X + 500, TEA_Y + 500),
            (TEA_X + 2_600, TEA_Y + 500),
            (TEA_X + 2_900, TEA_Y + 2_300),
            (TEA_X + 700, TEA_Y + 2_600),
        ],
        layer="MOSS_TEA",
    )

    # Low clipped hedge inside the south fence, west of the gate.
    draw_hedge(
        msp, doc, points=[(1_000, 900), (ZEN_X + ZEN_W + 1_000, 900)], hedge_width=600, color=83
    )

    # Bamboo screens: behind the dry garden and round the roji, with a gap for the path.
    draw_bamboo_fence(
        msp,
        doc,
        start=(ZEN_X + 500, ZEN_Y + ZEN_H + 400),
        end=(ZEN_X + ZEN_W - 500, ZEN_Y + ZEN_H + 400),
    )
    draw_bamboo_fence(msp, doc, start=(TEA_X, TEA_Y), end=(TEA_GATE[0], TEA_Y))
    draw_bamboo_fence(msp, doc, start=(TEA_GATE[1], TEA_Y), end=(TEA_X + TEA_W, TEA_Y))

    # ── 8. Lighting: stone lanterns at viewpoints, a few low spots ──────
    for cx, cy, size in [
        (10_200, 11_400, 600),  # pond, by the pergola
        (ZEN_X + ZEN_W - 1_200, ZEN_Y + ZEN_H - 900, 500),
        (TEA_X + 1_100, TEA_Y + 4_600, 500),
        (GATE_X + 2_100, 7_400, 500),  # half-way up the main path
        (GATE_X + 1_600, 1_500, 600),  # gate
        (3_600, 25_900, 500),
    ]:  # spring
        draw_stone_lantern(msp, doc, cx=cx, cy=cy, size=size)
    for x in range(int(ENGAWA_X) + 500, int(ENGAWA_X + ENGAWA_W), 2_500):
        draw_spotlight(msp, doc, x, ENGAWA_Y, layer="LIGHTING_SUBTLE", color=2)

    return doc
