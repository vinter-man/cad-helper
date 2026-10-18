# Plan: Playground between apartment blocks, Sofia

Source of truth: `build.py`. Build with `uv run cad-helper build playground`.

## Design concept

Three elliptical islands of rubber surfacing sit in a sea of gravel and are joined by rubber-plank bridges. Each island serves one age group: toddlers at the sandbox, middle children at the slides, older children at the climbing dome. Parents sit on benches around the edge, and a sound barrier shields the site from the road to the south.

## Site summary

- Site 8000 x 8000 mm, origin (0, 0) at the south-west corner; X = east, Y = north
- Sound barrier occupies the southern 300 mm (y 0 to 300); the playground surface runs from y = 300 to 8000
- Sofia: continental climate, hot summers, cold winters down to about -15 °C
- Style: modern, organic shapes
- Key constraint: road along the south side, so a fence with noise protection is required
- Key wish: three themed islands connected by bridges
- Printed at 1:50

## Zone layout

```
                 N (apartment blocks)
  +--------------------------------------+  y = 8000
  | shrubs                       shrubs  |
  | [bench NW]   ( ISLAND 3 )  [bench NE]|
  | shrub        ( climbing )      shrub |
  | [bench W]       /    \     [bench E] |
  =gate W       /      \          gate E=   y 3900-5100
  | bin   ( ISLAND 1 )--( ISLAND 2 )  bin|
  | light ( sandbox  )  (  slides  ) light
  |                                      |
  |######## SOUND BARRIER ###############|  y = 0-300
  +--------------------------------------+
                 S (road)
```

| Zone | Centre (x, y) | Radii rx x ry (mm) | Purpose |
|------|---------------|--------------------|---------|
| Island 1, SANDBOX ISLAND | (2500, 3500) | 1400 x 1100 | Toddlers 0-3: sandbox |
| Island 2, SLIDES ISLAND | (5800, 3200) | 1300 x 1000 | Ages 3-7: two slides |
| Island 3, CLIMBING ISLAND | (3800, 6000) | 1200 x 1200 | Ages 7-12: climbing dome |
| Gravel | whole site above the barrier | 8000 x 7700 | Loose fill between islands |
| Sound barrier | y 0 to 300 | 8000 x 300 | Noise protection from the road |

## Elements

| # | Element | Position (x, y) mm | Size (mm) | Function | Layer |
|---|---------|--------------------|-----------|----------|-------|
| 1 | Site boundary | (0, 300) to (8000, 8000) | 8000 x 7700 | `msp.add_lwpolyline` in build.py | BOUNDARY |
| 2 | Gravel surface | same as boundary | AR-SAND hatch, scale 15 | `add_hatch` | GRAVEL |
| 3 | Sound barrier | (0, 150) to (8000, 150) | 300 thick | `draw_sound_barrier` | SOUND_BARRIER |
| 4 | Fence, north, west and east | site edges; no fence on the south side | lines | `draw_fence(sides=("east", "north", "west"))` | FENCE |
| 5 | West gate | x = 0, opening y 3900 to 5100 | 1200 leaf, hinged at (0, 3900), opens inward | `draw_fence` (gate) | GATES |
| 6 | East gate | x = 8000, opening y 3900 to 5100 | 1200 leaf, hinged at (8000, 3900), opens inward | `draw_fence` (gate) | GATES |
| 7 | Island 1 | centre (2500, 3500) | rx 1400, ry 1100 | `draw_ellipse_zone` | ISLAND_SANDBOX, ISLAND_SANDBOX_FILL |
| 8 | Sandbox | centre (2500, 3500) | rx 1000, ry 800 | `draw_sandbox` | SANDBOX, SANDBOX_FILL |
| 9 | Island 2 | centre (5800, 3200) | rx 1300, ry 1000 | `draw_ellipse_zone` | ISLAND_SLIDES, ISLAND_SLIDES_FILL |
| 10 | Slide 1 | centre (5300, 3100), rotated -90° (runs south) | 1200 x 600 | `draw_slide` | SLIDES |
| 11 | Slide 2 | centre (6400, 3150), rotated -90° (runs south) | 1200 x 500 | `draw_slide` | SLIDES |
| 12 | Island 3 | centre (3800, 6000) | rx 1200, ry 1200 | `draw_ellipse_zone` | ISLAND_CLIMBING, ISLAND_CLIMBING_FILL |
| 13 | Climbing dome | centre (3800, 6000) | Ø1800 | `draw_climbing_frame` (dome) | CLIMBING |
| 14 | Bridge 1-2 | (3891, 3374) to (4509, 3317) | 700 wide, 621 long | `draw_rubber_bridge` | BRIDGES |
| 15 | Bridge 1-3 | (3030, 4518) to (3246, 4935) | 700 wide, 470 long | `draw_rubber_bridge` | BRIDGES |
| 16 | Bridge 2-3 | (5174, 4076) to (4497, 5024) | 700 wide, 1164 long | `draw_rubber_bridge` | BRIDGES |
| 17 | Bench NW | SW corner (500, 6500) | 1800 x 500 | `draw_bench` | BENCHES |
| 18 | Bench NE | SW corner (5700, 6500) | 1800 x 500 | `draw_bench` | BENCHES |
| 19 | Bench W | SW corner (700, 5000) | 1500 x 500 | `draw_bench` | BENCHES |
| 20 | Bench E | SW corner (5300, 4800) | 1500 x 500 | `draw_bench` | BENCHES |
| 21-28 | Shrubs (8) | see plant palette | Ø600 to Ø900 | `draw_shrub` | SHRUBS |
| 29 | Bin W | centre (300, 3500) | 300 x 300 | `draw_trash_bin` | FURNITURE |
| 30 | Bin E | centre (7700, 3500) | 300 x 300 | `draw_trash_bin` | FURNITURE |
| 31-38 | Ground lights (8) | (500, 1000), (7500, 1000), (300, 2800), (7700, 2800), (300, 6200), (7700, 6200), (2900, 7800), (5300, 7800) | 400 ring | `draw_ground_light` | GROUND_LIGHTS |
| 39 | North arrow | (-1200, 7000) | 800 | `draw_compass` | COMPASS |

Bridge ends are where the line between two island centres crosses each island's edge, computed in `_ellipse_edge` with the polar angle of that line.

The slides stand side by side, 385 mm apart, with their platforms at the north end and run-outs at the south end. Every corner of both slides is on the rubber of island 2, and the nearest bridge is 174 mm away.

Each gate leaf sweeps a 1200 mm quarter circle north of its south post. Nothing stands in it: the bins and the ground lights by the gates are south of the leaf, and the shrubs by the gates are north of the swing.

## Plant palette

The brief does not name species. The build draws eight shrubs to screen the bench backs.

| Plant | Qty | Size | Position | Why |
|-------|-----|------|----------|-----|
| Shrub (species not specified) | 2 | Ø900 | (1400, 7480), (6600, 7480) | Behind the north benches |
| Shrub (species not specified) | 4 | Ø700 | (600, 7600), (1800, 7600), (6200, 7600), (7400, 7600) | North corners, along the fence |
| Shrub (species not specified) | 1 | Ø600 | (350, 5550) | Beside bench W, north of the west gate swing |
| Shrub (species not specified) | 1 | Ø700 | (7550, 5550) | Beside bench E, north of the east gate swing |

## Materials

| Surface | Material | Hatch | Colour (ACI) |
|---------|----------|-------|--------------|
| Islands | EPDM rubber | DOTS, scale 45 | 2 yellow (sandbox), 1 red (slides), 4 cyan (climbing) |
| Between islands | Loose gravel | AR-SAND, scale 15 | 253 grey |
| Bridges | Rubber planks | rails and plank lines every 150 mm | 33 brown |
| Sound barrier | Concrete with acoustic insulation | solid | 8 grey |

## Build phases

1. Boundaries and ground: boundary, gravel, sound barrier, fence with two gates, north arrow
2. Islands: three ellipses with rubber surfacing
3. Equipment: sandbox, two slides, climbing dome
4. Bridges: three rubber bridges between island edges
5. Furniture: four benches, eight shrubs, two bins
6. Lighting: eight ground lights

## Changes from the first draft

- Open questions resolved: gates on both the west and east sides (opening y 3900 to 5100), and shrubs added behind and beside the benches.
- Slides: the first draft had a 2000 x 600 slide at (5500, 3500) and a 1500 x 500 slide at (6200, 2800), which overlapped. They are now two 1200 mm slides side by side, both running south, fully on island 2.
- Bridges: narrowed from 800 to 700 mm and attached at the island edges instead of running centre to centre.
- Benches: the north benches are straight 1800 x 500 benches at (500, 6500) and (5700, 6500) instead of curved benches near the corners. The side benches are 1500 long, at (700, 5000) and (5300, 4800), so they stay at least 300 mm off the island surfacing.
- Fence and gates: drawn with `draw_fence` on three sides instead of hand-written lines and arcs.
- Bins, ground lights and the two shrubs by the gates: moved out of the gate swings. Bins went from (500, 4000) to (300, 3500) and (7700, 3500).
