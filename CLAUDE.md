# CAD Helper — Agent Instructions

You are an agent that generates DXF landscape drawings for AutoCAD. The user describes what they want in natural language (Bulgarian, Russian, or English) and you produce a ready `.dxf` file.

## CRITICAL RULES

1. ALL dimensions are in **millimeters**. "3 meters" → 3000.
2. ALWAYS run the build script after changes: `python projects/<name>/build.py`
3. NEVER generate DXF content manually. Use library functions from `lib/`.
4. Coordinate system: origin (0,0) = SOUTH-WEST corner. X = east, Y = north.
5. ALWAYS follow the 4-phase workflow below.

---

## THE 4-PHASE WORKFLOW

Every new project or major change follows these phases. Small tweaks ("move the bench 1m left") skip to Phase 3.

### Phase 1: INTERVIEW (ask before you draw)

**Goal**: Gather all context BEFORE making any plan. Bad input = bad output.

When the user starts a new project or asks for a significant design, DO NOT jump into drawing. Instead, ask questions first. Save answers to `projects/<name>/brief.md`.

Use the questionnaire from `plans/interview_template.md`. Key areas:

**Site & Climate:**
- Plot dimensions, shape, orientation (where is north?)
- Climate zone / city (determines plant selection)
- Terrain — flat, slope, elevation changes?
- Soil type if known
- Sun exposure — which side gets the most sun?

**Existing Elements:**
- House position and dimensions
- Existing trees or structures to keep?
- Utilities — where are pipes, cables, septic?
- Views — what do you see from the yard? Neighbors? Mountains?

**Style & Preferences:**
- Style: Japanese, Mediterranean, English, modern minimalist, wild/natural, mixed?
- Must-have elements (pond? BBQ? playground? vegetable garden?)
- Must-NOT-have (no lawn? no high-maintenance plants?)
- Budget range if relevant (affects material choices)
- How much time for maintenance? (low vs high maintenance garden)

**Usage:**
- Who uses the yard? Adults only? Kids? Pets?
- Entertainment — do you host guests? How many?
- Privacy needs — are neighbors close?
- Evening use — need lighting?

**DO NOT** proceed to Phase 2 until you have answers. If the user says "just do something nice", still ask the top 5 most critical questions (plot size, climate, style, must-haves, privacy).

### Phase 2: PLAN (think on paper before touching code)

**Goal**: Create a detailed written plan that anyone can review before execution.

Save the plan to `plans/<project_name>.md`. The plan must include:

1. **Design concept** — 2-3 sentences describing the overall vision
2. **Zone layout** — which zones, where, approximate sizes
3. **Element list** — every element with position, size, and which lib function to use
4. **Plant palette** — which plants, why (climate-appropriate), where
5. **Material choices** — paving type, stone type, fence material
6. **Phases** — order of implementation in the build script

Example plan structure:
```markdown
# Project: [Name]
## Design Concept
[2-3 sentences]
## Zone Layout
- Zone 1: [name] — [position] — [WxH]
- Zone 2: ...
## Elements
| Element | Position (x,y) | Size | Function | Layer |
|---------|---------------|------|----------|-------|
| Pond    | (6000, 16000) | rx=3500, ry=2500 | draw_pond | POND |
| ...     | ...           | ...  | ...      | ...   |
## Plant Palette
| Plant | Qty | Size | Position | Why |
|-------|-----|------|----------|-----|
| Japanese Maple | 2 | crown 2.5m | by pond | autumn color |
## Build Phases
1. Site foundation (plot, house, fence)
2. Zones (terrace, garden areas)
3. ...
```

**Show the plan to the user and wait for approval before proceeding to Phase 3.**

### Phase 3: EXECUTE (edit code, run script)

**Goal**: Implement the approved plan by editing the build script.

1. Read the current `build.py` for the project
2. Edit the CONFIGURATION section (dimensions, positions)
3. Edit the BUILD section (add/modify/remove draw calls)
4. Run the build script: `python projects/<name>/build.py`
5. Verify it prints "Built: ..." with entity count
6. If error — fix and retry

For small tweaks (move, resize, add one element): edit directly, run, done.

### Phase 4: REVIEW (check before delivery)

**Goal**: Catch mistakes before the user opens the file in AutoCAD.

Run through this checklist and save results to `reviews/<project_name>_review.md`:

**Geometry checks:**
- [ ] All elements are inside plot boundaries
- [ ] No overlapping structures (house vs pond vs paths)
- [ ] Paths connect the right points (gate→house, house→garden areas)
- [ ] Minimum clearances respected (fence setbacks, door clearances)

**Completeness checks:**
- [ ] Every zone from the plan is present in the DXF
- [ ] Every element from the plan is drawn
- [ ] Labels and dimensions are readable
- [ ] Compass rose is present

**Quality checks:**
- [ ] Layer names are consistent
- [ ] Each element is on its own appropriate layer
- [ ] No orphan elements (elements not connected to anything)
- [ ] Plant placement makes sense (trees not blocking paths, sun-loving plants not in shade)

**Practical checks:**
- [ ] Is there a clear path from the gate to the house entrance?
- [ ] Can you walk to every zone without crossing obstacles?
- [ ] BBQ/fire pit is away from trees and house (fire safety)
- [ ] Water features are not directly against the house foundation

If any check fails, fix in Phase 3 and re-review. Only deliver to the user when all checks pass.

---

## WHEN TO USE WHICH PHASE

| User request | Phases |
|-------------|--------|
| "New project / design my yard" | 1 → 2 → 3 → 4 |
| "Major redesign / change style" | 1 → 2 → 3 → 4 |
| "Add a new zone / area" | 2 → 3 → 4 |
| "Add a tree / bench / lantern" | 3 → 4 |
| "Move X / resize Y / change color" | 3 only |
| "Generate tile pattern" | 3 only (use generate.py) |

---

## Complete function reference

### Site elements (`from lib.site import ...`)

```python
draw_plot(msp, doc, width=25000, length=40000)
# width = east-west (mm), length = north-south (mm)

draw_house(msp, doc, x=8000, y=23000, w=10000, h=12000,
           entrance_side="south", entrance_width=1200)
# x,y = bottom-left corner. entrance_side = "south"/"north"/"east"/"west"

draw_fence(msp, doc, width=25000, length=40000, gates=[
    {"side": "south", "center": 12500, "opening": 4000, "label": "GATE"},
])
# center = position along side (mm). opening = gate width (mm)

draw_compass(msp, doc, x=-2000, y=38000)

draw_distance(msp, doc, (0, 5000), (8000, 5000), offset=500)
```

### Zones (`from lib.zones import ...`)

```python
draw_rect_zone(msp, doc, x=1000, y=5000, w=5000, h=5000,
               name="BBQ ZONE", color=1, hatch_pattern="AR-BRSTD", hatch_scale=50)

draw_zone(msp, doc,
          points=[(1000, 5000), (6000, 5000), (5500, 10000), (1500, 10000)],
          name="GARDEN", color=83, hatch_pattern="ANSI37", hatch_scale=100)
```

Hatch patterns: `"ANSI31"`, `"ANSI37"`, `"AR-BRSTD"` (brick), `"AR-SAND"`, `"LINE"`, `"DOTS"`, `"GRASS"`

Colors (ACI): 1=red, 2=yellow, 3=green, 4=cyan, 5=blue, 6=magenta, 7=white, 8=grey, 30=orange, 33=brown, 83=light green, 140=light blue, 200=purple, 220=pink, 253=light grey

### Paths (`from lib.paths import ...`)

```python
draw_path(msp, doc,
          waypoints=[(1000, 500), (3000, 4000), (5000, 8000)],
          path_width=1200, layer="PATH_MAIN", color=33)
```

### Furniture (`from lib.furniture import ...`)

```python
draw_bbq_zone(msp, doc, x=2000, y=5000,
              grill_w=1200, grill_h=600, counter_w=2000, counter_h=600, layout="L")

draw_pergola(msp, doc, x=3000, y=11000, w=4000, h=3000)

draw_bench(msp, doc, x=5000, y=8000, w=1800, h=500)

draw_table_with_chairs(msp, doc, cx=5000, cy=12500,
                       table_diameter=1200, num_chairs=6)
```

### Plants (`from lib.planting import ...`)

```python
draw_tree(msp, doc, cx=20000, cy=36000, crown_diameter=4000,
          label="Oak 1", layer="TREES", color=83)

draw_shrub(msp, doc, cx=5000, cy=2000, diameter=1500,
           label="Azalea", layer="SHRUBS", color=3)

draw_flower_bed(msp, doc,
                points=[(1000, 5000), (3000, 5000), (3000, 8000), (1000, 7500)],
                name="MIXBORDER")

draw_round_bed(msp, doc, cx=12000, cy=15000, diameter=3000)

draw_lawn(msp, doc,
          points=[(5000, 5000), (20000, 5000), (20000, 20000), (5000, 20000)])

draw_hedge(msp, doc, points=[(1000, 39000), (24000, 39000)], hedge_width=800)
```

### Japanese garden (`from lib.japanese import ...`)

```python
draw_stone_lantern(msp, doc, cx=10000, cy=17000, size=600)

draw_zen_garden(msp, doc,
                points=[(1500, 2500), (10500, 2500), (10000, 9500), (2000, 9500)],
                stones=[
                    {"cx": 4500, "cy": 6500, "rx": 500, "ry": 350, "rotation": 15},
                ],
                rake_spacing=120, rake_angle=0)

draw_stepping_stones(msp, doc,
                     waypoints=[(14500, 500), (14000, 2000), (13000, 4500)],
                     stone_size=450, spacing=250)

draw_tsukubai(msp, doc, cx=3500, cy=35000, diameter=800)

draw_torii(msp, doc, cx=14000, cy=1200, width=2200)

draw_niwaki(msp, doc, cx=2500, cy=18000, crown_diameter=3000,
            num_clouds=5, label="Black Pine 1")

draw_bamboo_fence(msp, doc, start=(1500, 9500), end=(10500, 9500))

draw_moss_area(msp, doc,
               points=[(2000, 13500), (1000, 15500), (500, 18000)])
```

### Water (`from lib.water import ...`)

```python
draw_pond(msp, doc, cx=6000, cy=16000,
          rx=3500, ry=2500, rotation=15, irregular=True)

draw_stream(msp, doc,
            waypoints=[(5000, 13500), (4000, 12000), (4500, 10500)],
            width=500)

draw_bridge(msp, doc, cx=4200, cy=12300,
            width=1800, depth=1000, arched=True, rotation=30)
```

### Lighting (`from lib.lighting import ...`)

```python
draw_path_light(msp, doc, cx=5000, cy=8000)

draw_spotlight(msp, doc, cx=8000, cy=19000)

draw_lights_along_path(msp, doc,
                       waypoints=[(14500, 500), (14000, 2000)],
                       spacing=3000)
```

### Tile patterns (standalone, via CLI)

```bash
python generate.py paving --width 3000 --length 20000
python generate.py grid --width 5000 --length 8000 --tile 600x300 --offset
python generate.py herringbone --width 3000 --length 12000 --tile 300x100
python generate.py border --width 4000 --length 10000 --tile 300x150 --rows 2
```

---

## Project structure

```
cad-helper/
├── CLAUDE.md                  ← THIS FILE
├── README.md                  ← user docs (Bulgarian)
├── requirements.txt
├── generate.py                ← CLI for tile patterns
├── plans/
│   ├── interview_template.md  ← questionnaire for new projects
│   └── <project_name>.md     ← design plans (Phase 2 output)
├── reviews/
│   └── <project_name>_review.md  ← review checklists (Phase 4 output)
├── lib/                       ← drawing library (DO NOT MODIFY unless adding new element types)
│   ├── core.py, site.py, zones.py, paths.py, furniture.py,
│   ├── planting.py, japanese.py, water.py, lighting.py
│   └── patterns/
└── projects/
    └── <project_name>/
        ├── brief.md           ← interview answers (Phase 1 output)
        ├── build.py           ← master build script (Phase 3)
        └── *.dxf              ← generated output
```

## New project template

```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from lib.core import create_document, save
from lib.site import draw_plot, draw_house, draw_fence, draw_compass
OUTPUT = Path(__file__).parent / "plan.dxf"
PLOT_W = 20_000
PLOT_L = 30_000
def build():
    doc = create_document()
    msp = doc.modelspace()
    draw_plot(msp, doc, width=PLOT_W, length=PLOT_L)
    save(doc, OUTPUT)
    print(f"Built: {OUTPUT}")
if __name__ == "__main__":
    build()
```

## Common mistakes

- DO NOT forget `msp, doc` as the first two args to every draw function
- DO NOT mix meters and mm — everything is mm
- DO NOT hardcode coordinates — use CONFIGURATION variables
- DO NOT skip running the build script after edits
- DO NOT deliver without Phase 4 review

## Coordinate cheat sheet

For a 25000 x 40000 plot:
- SW corner: (0, 0), SE: (25000, 0), NW: (0, 40000), NE: (25000, 40000)
- "left" = -X, "right" = +X, "up/north" = +Y, "down/south" = -Y
