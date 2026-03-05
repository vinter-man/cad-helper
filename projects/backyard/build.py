#!/usr/bin/env python3
"""Backyard landscape project — Japanese garden style.

Run from repo root:
    python projects/backyard/build.py

Design principles:
- Asymmetry (odd numbers, off-center placement)
- Borrowed scenery (shakkei) — layers of depth
- Wabi-sabi — natural imperfection
- Ma (negative space) — empty areas are intentional
- Stones and water as core elements
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.core import create_document, save, add_layer
from lib.site import draw_plot, draw_house, draw_fence, draw_compass, draw_distance
from lib.zones import draw_rect_zone, draw_zone
from lib.paths import draw_path
from lib.furniture import draw_pergola, draw_bench, draw_table_with_chairs
from lib.planting import (
    draw_tree, draw_shrub, draw_flower_bed, draw_round_bed,
    draw_lawn, draw_hedge,
)
from lib.lighting import draw_spotlight
from lib.japanese import (
    draw_stone_lantern, draw_zen_garden, draw_stepping_stones,
    draw_tsukubai, draw_torii, draw_niwaki, draw_bamboo_fence,
    draw_moss_area,
)
from lib.water import draw_pond, draw_stream, draw_bridge

OUTPUT = Path(__file__).parent / "backyard.dxf"

# ═══════════════════════════════════════════════════════════════════════════════
# PROJECT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PLOT_W = 25_000   # 25m east-west
PLOT_L = 40_000   # 40m north-south

# House: 10x12m, offset north-east (asymmetric placement)
HOUSE_W = 10_000
HOUSE_H = 12_000
HOUSE_X = 9_000
HOUSE_Y = PLOT_L - 5_000 - HOUSE_H  # 23000

# Single pedestrian gate — no vehicle gate visible from garden
GATES = [
    {
        "side": "south",
        "center": PLOT_W / 2 + 2_000,  # off-center
        "opening": 1_500,
        "label": "MAIN GATE",
    },
]

# ─── Engawa (covered wooden veranda) — south side of house ───
ENGAWA_X = HOUSE_X - 500
ENGAWA_Y = HOUSE_Y - 2_500
ENGAWA_W = HOUSE_W + 1_000
ENGAWA_H = 2_500

# ─── Koi pond — west side, organic shape ───
POND_CX = 6_000
POND_CY = 16_000
POND_RX = 3_500
POND_RY = 2_500

# ─── Zen garden (karesansui) — south-west corner ───
ZEN_X = 1_500
ZEN_Y = 2_500
ZEN_W = 9_000
ZEN_H = 7_000

# ─── Tea garden area — north-west corner ───
TEA_X = 1_000
TEA_Y = PLOT_L - 8_000
TEA_W = 7_000
TEA_H = 6_000


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def build():
    doc = create_document()
    msp = doc.modelspace()

    # ── Phase 1: Site foundation ──────────────────────────────────────────

    draw_plot(msp, doc, width=PLOT_W, length=PLOT_L)

    draw_house(msp, doc,
               x=HOUSE_X, y=HOUSE_Y,
               w=HOUSE_W, h=HOUSE_H,
               entrance_side="south",
               entrance_width=1_800)

    draw_fence(msp, doc, width=PLOT_W, length=PLOT_L, gates=GATES)
    draw_compass(msp, doc, x=-2_000, y=PLOT_L - 2_000)

    # ── Phase 2: Zones ───────────────────────────────────────────────────

    # Engawa (wooden veranda) — transition between house and garden
    draw_rect_zone(msp, doc,
                   x=ENGAWA_X, y=ENGAWA_Y, w=ENGAWA_W, h=ENGAWA_H,
                   name="ENGAWA", color=33, hatch_pattern="LINE", hatch_scale=30)

    # Tea garden zone (roji) — north-west
    draw_zone(msp, doc,
              points=[(TEA_X, TEA_Y),
                      (TEA_X + TEA_W, TEA_Y),
                      (TEA_X + TEA_W - 1_000, TEA_Y + TEA_H),
                      (TEA_X, TEA_Y + TEA_H)],
              name="TEA GARDEN", color=83, hatch_pattern="ANSI37", hatch_scale=120)

    # ── Phase 3: Zen Garden (karesansui) ─────────────────────────────────

    zen_boundary = [
        (ZEN_X, ZEN_Y),
        (ZEN_X + ZEN_W, ZEN_Y),
        (ZEN_X + ZEN_W - 500, ZEN_Y + ZEN_H),  # slight asymmetry
        (ZEN_X + 500, ZEN_Y + ZEN_H),
    ]

    draw_zen_garden(msp, doc, zen_boundary,
                    stones=[
                        # Main stone group (3 stones — heaven, earth, man)
                        {"cx": ZEN_X + 3_000, "cy": ZEN_Y + 4_000,
                         "rx": 500, "ry": 350, "rotation": 15},
                        {"cx": ZEN_X + 3_800, "cy": ZEN_Y + 3_500,
                         "rx": 350, "ry": 250, "rotation": -20},
                        {"cx": ZEN_X + 2_500, "cy": ZEN_Y + 3_200,
                         "rx": 250, "ry": 180, "rotation": 45},
                        # Secondary group (2 stones)
                        {"cx": ZEN_X + 7_000, "cy": ZEN_Y + 5_000,
                         "rx": 400, "ry": 300, "rotation": -10},
                        {"cx": ZEN_X + 7_500, "cy": ZEN_Y + 4_400,
                         "rx": 200, "ry": 150, "rotation": 30},
                    ],
                    rake_spacing=120, rake_angle=0)

    # ── Phase 4: Water ───────────────────────────────────────────────────

    # Koi pond — organic shape, west-center
    draw_pond(msp, doc, cx=POND_CX, cy=POND_CY,
              rx=POND_RX, ry=POND_RY, rotation=15, irregular=True)

    # Stream from pond flowing south towards zen garden
    draw_stream(msp, doc,
                waypoints=[
                    (POND_CX - 1_000, POND_CY - POND_RY),
                    (POND_CX - 2_000, POND_CY - POND_RY - 1_500),
                    (POND_CX - 1_500, POND_CY - POND_RY - 3_000),
                    (ZEN_X + ZEN_W - 500, ZEN_Y + ZEN_H + 500),
                ],
                width=500)

    # Arched bridge over stream
    draw_bridge(msp, doc,
                cx=POND_CX - 1_800, cy=POND_CY - POND_RY - 1_200,
                width=1_800, depth=1_000, arched=True, rotation=30)

    # ── Phase 5: Paths ───────────────────────────────────────────────────

    # Main approach path — stepping stones from gate to house
    gate_x = PLOT_W / 2 + 2_000
    main_stepping = [
        (gate_x, 500),
        (gate_x - 500, 2_000),
        (gate_x - 1_500, 4_500),
        (gate_x - 3_000, 7_000),
        (HOUSE_X + 3_000, 12_000),
        (HOUSE_X + 4_000, 16_000),
        (HOUSE_X + HOUSE_W / 2, ENGAWA_Y - 200),
    ]
    draw_stepping_stones(msp, doc, main_stepping,
                         stone_size=450, spacing=250)

    # Path to tea garden
    tea_stepping = [
        (HOUSE_X, HOUSE_Y + HOUSE_H / 2),
        (HOUSE_X - 2_000, HOUSE_Y + HOUSE_H / 2 + 1_000),
        (HOUSE_X - 4_000, HOUSE_Y + HOUSE_H + 1_000),
        (TEA_X + TEA_W / 2, TEA_Y + 500),
    ]
    draw_stepping_stones(msp, doc, tea_stepping,
                         stone_size=400, spacing=300,
                         layer="STEPPING_STONES_TEA")

    # Path around pond
    pond_stepping = [
        (POND_CX + POND_RX + 800, POND_CY - 1_000),
        (POND_CX + POND_RX + 500, POND_CY),
        (POND_CX + POND_RX + 800, POND_CY + 1_500),
        (POND_CX + 1_000, POND_CY + POND_RY + 800),
        (POND_CX - 1_500, POND_CY + POND_RY + 500),
    ]
    draw_stepping_stones(msp, doc, pond_stepping,
                         stone_size=400, spacing=200,
                         layer="STEPPING_STONES_POND")

    # ── Phase 6: Structures ──────────────────────────────────────────────

    # Torii gate at garden entrance
    draw_torii(msp, doc, cx=gate_x - 500, cy=1_200, width=2_200)

    # Wisteria pergola (fujidana) near pond viewing area
    draw_pergola(msp, doc,
                 x=POND_CX + POND_RX + 500,
                 y=POND_CY - 2_000,
                 w=3_000, h=2_500,
                 layer="FUJIDANA", color=200)

    # Sitting area under pergola
    draw_bench(msp, doc,
               x=POND_CX + POND_RX + 800,
               y=POND_CY - 1_800,
               w=2_000, h=500,
               layer="FURNITURE", color=33)

    # Tsukubai (water basin) in tea garden
    draw_tsukubai(msp, doc,
                  cx=TEA_X + 2_500, cy=TEA_Y + 3_000,
                  diameter=800)

    # ── Phase 7: Planting ────────────────────────────────────────────────

    # Niwaki (cloud-pruned pines) — 3 specimens, asymmetric
    draw_niwaki(msp, doc,
                cx=POND_CX - POND_RX - 1_500, cy=POND_CY + 2_000,
                crown_diameter=3_000, num_clouds=5, label="Black Pine 1")
    draw_niwaki(msp, doc,
                cx=POND_CX + 2_000, cy=POND_CY + POND_RY + 2_000,
                crown_diameter=2_500, num_clouds=4, label="Black Pine 2")
    draw_niwaki(msp, doc,
                cx=TEA_X + TEA_W - 500, cy=TEA_Y + TEA_H - 500,
                crown_diameter=2_000, num_clouds=3, label="Pine 3")

    # Japanese maples (momiji) — smaller, by the pond
    draw_tree(msp, doc,
              cx=POND_CX + POND_RX - 500, cy=POND_CY + POND_RY + 500,
              crown_diameter=2_500, label="Maple 1", layer="MAPLES", color=1)
    draw_tree(msp, doc,
              cx=POND_CX - POND_RX + 1_000, cy=POND_CY - 500,
              crown_diameter=2_000, label="Maple 2", layer="MAPLES", color=1)

    # Cherry trees (sakura) — 3 along east boundary
    for i in range(3):
        draw_tree(msp, doc,
                  cx=PLOT_W - 3_000,
                  cy=8_000 + i * 6_000,
                  crown_diameter=3_500,
                  label=f"Sakura {i + 1}", layer="SAKURA", color=220)

    # Bamboo grove — north-east corner (screen planting)
    for i in range(7):
        bx = PLOT_W - 1_500 + (i % 3) * 500 - 500
        by = PLOT_L - 2_000 - i * 800
        draw_shrub(msp, doc, cx=bx, cy=by, diameter=800,
                   layer="BAMBOO", color=3)

    # Azalea mounds — rounded shrubs, 5 in a group near engawa
    azalea_positions = [
        (ENGAWA_X - 1_500, ENGAWA_Y + 500),
        (ENGAWA_X - 2_200, ENGAWA_Y - 300),
        (ENGAWA_X - 1_000, ENGAWA_Y - 800),
        (ENGAWA_X + ENGAWA_W + 800, ENGAWA_Y + 300),
        (ENGAWA_X + ENGAWA_W + 1_500, ENGAWA_Y - 500),
    ]
    for i, (ax, ay) in enumerate(azalea_positions):
        draw_shrub(msp, doc, cx=ax, cy=ay,
                   diameter=1_200 + (i % 3) * 300,
                   label="" if i > 0 else "Azalea",
                   layer="AZALEAS", color=220)

    # Moss areas — under trees and around pond
    draw_moss_area(msp, doc, [
        (POND_CX - POND_RX - 500, POND_CY - POND_RY + 500),
        (POND_CX - POND_RX - 2_500, POND_CY - 500),
        (POND_CX - POND_RX - 3_000, POND_CY + 2_000),
        (POND_CX - POND_RX - 2_000, POND_CY + 3_500),
        (POND_CX - POND_RX, POND_CY + POND_RY + 500),
    ])

    draw_moss_area(msp, doc, [
        (TEA_X + 500, TEA_Y + 500),
        (TEA_X + TEA_W - 1_500, TEA_Y + 500),
        (TEA_X + TEA_W - 2_000, TEA_Y + 2_000),
        (TEA_X + 1_000, TEA_Y + 2_500),
    ], layer="MOSS_TEA")

    # Hedge along south fence (low, clipped)
    draw_hedge(msp, doc,
               points=[(1_000, 800), (ZEN_X + ZEN_W + 1_000, 800)],
               hedge_width=600, layer="HEDGES", color=83)

    # Bamboo fence sections (takegaki) — screening views
    draw_bamboo_fence(msp, doc,
                      start=(ZEN_X, ZEN_Y + ZEN_H),
                      end=(ZEN_X + ZEN_W, ZEN_Y + ZEN_H))
    draw_bamboo_fence(msp, doc,
                      start=(TEA_X, TEA_Y),
                      end=(TEA_X + TEA_W, TEA_Y))

    # ── Phase 8: Lighting ────────────────────────────────────────────────

    # Stone lanterns (toro) — placed at key viewing points
    draw_stone_lantern(msp, doc,
                       cx=POND_CX + POND_RX + 300, cy=POND_CY + 1_000,
                       size=600)
    draw_stone_lantern(msp, doc,
                       cx=ZEN_X + ZEN_W - 1_000, cy=ZEN_Y + ZEN_H - 500,
                       size=500)
    draw_stone_lantern(msp, doc,
                       cx=TEA_X + 1_500, cy=TEA_Y + TEA_H - 1_000,
                       size=500)
    draw_stone_lantern(msp, doc,
                       cx=main_stepping[2][0] + 800, cy=main_stepping[2][1],
                       size=500)
    draw_stone_lantern(msp, doc,
                       cx=gate_x + 1_500, cy=1_500,
                       size=600)

    # Subtle spotlights — engawa edge only
    for x_pos in range(int(ENGAWA_X), int(ENGAWA_X + ENGAWA_W) + 1, 2_500):
        draw_spotlight(msp, doc, x_pos, ENGAWA_Y, layer="LIGHTING_SUBTLE", color=2)

    # ── Save ─────────────────────────────────────────────────────────────
    path = save(doc, OUTPUT)
    print(f"Built: {path}")

    entities = list(msp)
    layers = [l.dxf.name for l in doc.layers if l.dxf.name not in ('0', 'Defpoints')]
    print(f"  {len(entities)} entities across {len(layers)} layers")
    print(f"  Layers: {', '.join(sorted(layers))}")

    return path


if __name__ == "__main__":
    build()
