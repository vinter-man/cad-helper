#!/usr/bin/env python3
"""
Bar Patio Landscaping - Велико Търново
4x4m patio with Mexican-Bulgarian fusion style
Vines + cacti + herbs for evening bar atmosphere
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.core import create_document, save
from lib.site import draw_compass
from lib.zones import draw_rect_zone
from lib.planting import draw_shrub
from lib.lighting import draw_path_light

# Output file
OUTPUT = Path(__file__).parent / "plan.dxf"

# ============================================================================
# CONFIGURATION
# ============================================================================

# Site dimensions (mm)
PATIO_W = 4000  # 4m width (east-west)
PATIO_L = 4000  # 4m length (north-south)
BAR_W = 8000    # 8m bar interior width
BAR_L = 4000    # 4m bar interior length

# Stairs
STAIRS_X = 1500
STAIRS_Y = -600
STAIRS_W = 1000
STAIRS_H = 300  # Each step height

# Fences
FENCE_WEST_X = -200
FENCE_EAST_X = 4200
FENCE_HEIGHT = 800  # Not drawn in plan view, just noted

# Tables (800x600mm each)
TABLE_W = 800
TABLE_H = 600
TABLES = [
    {"x": 800, "y": 600},    # Table 1
    {"x": 2400, "y": 600},   # Table 2
    {"x": 800, "y": 2200},   # Table 3
    {"x": 2400, "y": 2200},  # Table 4
]

# Chairs (Ø450mm around tables)
CHAIR_R = 225  # radius
CHAIRS = [
    # Table 1
    {"cx": 600, "cy": 600}, {"cx": 1000, "cy": 400}, {"cx": 1400, "cy": 600}, {"cx": 1000, "cy": 800},
    # Table 2
    {"cx": 2200, "cy": 600}, {"cx": 2600, "cy": 400}, {"cx": 3000, "cy": 600}, {"cx": 2600, "cy": 800},
    # Table 3
    {"cx": 600, "cy": 2200}, {"cx": 1000, "cy": 2000}, {"cx": 1400, "cy": 2200}, {"cx": 1000, "cy": 2400},
    # Table 4
    {"cx": 2200, "cy": 2200}, {"cx": 2600, "cy": 2000}, {"cx": 3000, "cy": 2200}, {"cx": 2600, "cy": 2400},
]

# Vine planters (long troughs along fences)
VINE_PLANTER_W = 600
VINE_PLANTER_L = 3000
VINE_WEST = {"x": 100, "y": 500}
VINE_EAST = {"x": 3300, "y": 500}

# Cacti (4 corners)
CACTUS_D = 400
CACTI = [
    {"cx": 200, "cy": 200, "label": "Opuntia 1"},
    {"cx": 3600, "cy": 200, "label": "Opuntia 2"},
    {"cx": 200, "cy": 3600, "label": "Opuntia 3"},
    {"cx": 3600, "cy": 3600, "label": "Opuntia 4"},
]

# Herb planters (central)
HERB_SIZE = 300
HERBS = [
    {"x": 1800, "y": 1400, "label": "Rosemary"},
    {"x": 1800, "y": 2600, "label": "Lavender"},
]

# Lighting
LANTERN_X = 1800
LANTERN_Y = 4000

# Compass
COMPASS_X = 4500
COMPASS_Y = 4500


# ============================================================================
# BUILD FUNCTIONS
# ============================================================================

def draw_patio_zone(msp, doc):
    """Draw patio area with hatch"""
    draw_rect_zone(
        msp, doc,
        x=0, y=0,
        w=PATIO_W, h=PATIO_L,
        name="PATIO",
        color=253,  # light grey
        hatch_pattern="AR-SAND",
        hatch_scale=50
    )


def draw_bar_interior(msp, doc):
    """Draw bar building outline"""
    # Bar is north of patio (y=4000 and up)
    if "BUILDING" not in doc.layers:
        doc.layers.add("BUILDING")
    
    msp.add_lwpolyline(
        [(0, PATIO_L), (BAR_W, PATIO_L), (BAR_W, PATIO_L + BAR_L), (0, PATIO_L + BAR_L), (0, PATIO_L)],
        dxfattribs={"layer": "BUILDING", "color": 8}  # grey
    )
    
    # Label
    msp.add_text(
        "BAR INTERIOR",
        height=300,
        dxfattribs={"layer": "BUILDING", "insert": (BAR_W/2, PATIO_L + BAR_L/2), "color": 8}
    )


def draw_stairs(msp, doc):
    """Draw entrance stairs (2 steps)"""
    if "STAIRS" not in doc.layers:
        doc.layers.add("STAIRS")
    
    # Step 1
    msp.add_lwpolyline(
        [(STAIRS_X, STAIRS_Y), (STAIRS_X + STAIRS_W, STAIRS_Y),
         (STAIRS_X + STAIRS_W, STAIRS_Y + STAIRS_H), (STAIRS_X, STAIRS_Y + STAIRS_H),
         (STAIRS_X, STAIRS_Y)],
        dxfattribs={"layer": "STAIRS", "color": 33}  # brown
    )
    
    # Step 2
    msp.add_lwpolyline(
        [(STAIRS_X, STAIRS_Y + STAIRS_H), (STAIRS_X + STAIRS_W, STAIRS_Y + STAIRS_H),
         (STAIRS_X + STAIRS_W, STAIRS_Y + 2*STAIRS_H), (STAIRS_X, STAIRS_Y + 2*STAIRS_H),
         (STAIRS_X, STAIRS_Y + STAIRS_H)],
        dxfattribs={"layer": "STAIRS", "color": 33}
    )
    
    # Label
    msp.add_text(
        "STAIRS",
        height=200,
        dxfattribs={"layer": "STAIRS", "insert": (STAIRS_X + STAIRS_W/2, STAIRS_Y + STAIRS_H), "color": 33}
    )


def draw_fences(msp, doc):
    """Draw west and east fences"""
    if "FENCE" not in doc.layers:
        doc.layers.add("FENCE")
    
    # West fence (thick line)
    msp.add_line(
        (FENCE_WEST_X, 0), (FENCE_WEST_X, PATIO_L),
        dxfattribs={"layer": "FENCE", "color": 8, "lineweight": 50}
    )
    
    # East fence (thick line)
    msp.add_line(
        (FENCE_EAST_X, 0), (FENCE_EAST_X, PATIO_L),
        dxfattribs={"layer": "FENCE", "color": 8, "lineweight": 50}
    )
    
    # Labels
    msp.add_text(
        "FENCE",
        height=150,
        dxfattribs={"layer": "FENCE", "insert": (FENCE_WEST_X - 300, PATIO_L/2), "color": 8, "rotation": 90}
    )
    msp.add_text(
        "FENCE",
        height=150,
        dxfattribs={"layer": "FENCE", "insert": (FENCE_EAST_X + 300, PATIO_L/2), "color": 8, "rotation": 90}
    )


def draw_tables(msp, doc):
    """Draw rectangular tables"""
    if "FURNITURE" not in doc.layers:
        doc.layers.add("FURNITURE")
    
    for i, table in enumerate(TABLES, 1):
        x, y = table["x"], table["y"]
        msp.add_lwpolyline(
            [(x, y), (x + TABLE_W, y), (x + TABLE_W, y + TABLE_H), (x, y + TABLE_H), (x, y)],
            dxfattribs={"layer": "FURNITURE", "color": 33}  # brown
        )
        
        # Label
        msp.add_text(
            f"T{i}",
            height=150,
            dxfattribs={"layer": "FURNITURE", "insert": (x + TABLE_W/2, y + TABLE_H/2), "color": 33}
        )


def draw_chairs(msp, doc):
    """Draw chairs as circles"""
    if "FURNITURE" not in doc.layers:
        doc.layers.add("FURNITURE")
    
    for chair in CHAIRS:
        msp.add_circle(
            (chair["cx"], chair["cy"]),
            radius=CHAIR_R,
            dxfattribs={"layer": "FURNITURE", "color": 33}
        )


def draw_vine_planters(msp, doc):
    """Draw long planters for vines along fences"""
    if "PLANTERS" not in doc.layers:
        doc.layers.add("PLANTERS")
    
    # West planter
    x, y = VINE_WEST["x"], VINE_WEST["y"]
    msp.add_lwpolyline(
        [(x, y), (x + VINE_PLANTER_W, y), (x + VINE_PLANTER_W, y + VINE_PLANTER_L),
         (x, y + VINE_PLANTER_L), (x, y)],
        dxfattribs={"layer": "PLANTERS", "color": 30}  # orange/terracotta
    )
    msp.add_text(
        "VINE PLANTER",
        height=120,
        dxfattribs={"layer": "PLANTERS", "insert": (x + VINE_PLANTER_W/2, y + VINE_PLANTER_L/2), "color": 30, "rotation": 90}
    )
    
    # East planter
    x, y = VINE_EAST["x"], VINE_EAST["y"]
    msp.add_lwpolyline(
        [(x, y), (x + VINE_PLANTER_W, y), (x + VINE_PLANTER_W, y + VINE_PLANTER_L),
         (x, y + VINE_PLANTER_L), (x, y)],
        dxfattribs={"layer": "PLANTERS", "color": 30}
    )
    msp.add_text(
        "VINE PLANTER",
        height=120,
        dxfattribs={"layer": "PLANTERS", "insert": (x + VINE_PLANTER_W/2, y + VINE_PLANTER_L/2), "color": 30, "rotation": 90}
    )


def draw_cacti(msp, doc):
    """Draw cacti in 4 corners using shrub symbols"""
    for cactus in CACTI:
        draw_shrub(
            msp, doc,
            cx=cactus["cx"],
            cy=cactus["cy"],
            diameter=CACTUS_D,
            label=cactus["label"],
            layer="PLANTS",
            color=3  # green
        )


def draw_herb_planters(msp, doc):
    """Draw small square planters for herbs"""
    if "PLANTERS" not in doc.layers:
        doc.layers.add("PLANTERS")
    
    for herb in HERBS:
        x, y = herb["x"], herb["y"]
        msp.add_lwpolyline(
            [(x, y), (x + HERB_SIZE, y), (x + HERB_SIZE, y + HERB_SIZE),
             (x, y + HERB_SIZE), (x, y)],
            dxfattribs={"layer": "PLANTERS", "color": 30}
        )
        
        # Label
        msp.add_text(
            herb["label"],
            height=80,
            dxfattribs={"layer": "PLANTERS", "insert": (x + HERB_SIZE/2, y + HERB_SIZE/2), "color": 30}
        )


def draw_lighting(msp, doc):
    """Draw lantern on partition wall"""
    draw_path_light(msp, doc, cx=LANTERN_X, cy=LANTERN_Y)
    
    # Add label
    if "LIGHTING" not in doc.layers:
        doc.layers.add("LIGHTING")
    
    msp.add_text(
        "LANTERN",
        height=150,
        dxfattribs={"layer": "LIGHTING", "insert": (LANTERN_X, LANTERN_Y - 300), "color": 2}
    )


# ============================================================================
# MAIN BUILD
# ============================================================================

def build():
    """Main build function"""
    doc = create_document()
    msp = doc.modelspace()
    
    # Phase 1: Site foundation
    draw_patio_zone(msp, doc)
    draw_bar_interior(msp, doc)
    draw_stairs(msp, doc)
    draw_fences(msp, doc)
    draw_compass(msp, doc, x=COMPASS_X, y=COMPASS_Y)
    
    # Phase 2: Furniture
    draw_tables(msp, doc)
    draw_chairs(msp, doc)
    
    # Phase 3: Planters and plants
    draw_vine_planters(msp, doc)
    draw_cacti(msp, doc)
    draw_herb_planters(msp, doc)
    
    # Phase 4: Lighting
    draw_lighting(msp, doc)
    
    # Save
    save(doc, OUTPUT)
    
    # Count entities
    entity_count = len(list(msp))
    print(f"✓ Built: {OUTPUT}")
    print(f"✓ Entities: {entity_count}")
    print(f"✓ Layers: {len(doc.layers)}")


if __name__ == "__main__":
    build()
