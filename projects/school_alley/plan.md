# Plan: School Alley, Sofia

Source of truth: `build.py`. Build with `uv run cad-helper build school_alley`.

## Design concept

A modern pedestrian alley, 3 x 50 m, between two schools. The paving grades from light tiles in the centre to dark tiles at the edges using all five tile sizes from the brief. A seating pocket with a pergola and two benches opens off each end of the alley, on opposite sides, with flower beds and shrubs along the walk.

## Site summary

- Alley 50000 mm long (X, west to east) and 3000 mm wide (Y, south to north)
- Origin (0, 0) is the south-west corner of the paving
- Curbs 150 mm wide: south curb y -150 to 0, north curb y 3000 to 3150
- Flat; lawns and trees on both sides; school buildings at both ends
- Sofia
- Printed at 1:100

## Zone layout

```
                                   N (+Y)
                                                      +-----------+ y = 6500
                 [accent bed]                         | EAST      |
                [MIXBORDER N]       [ROSES & GRASSES] | POCKET    |
  +===================================================+           +===+ y = 3000
  |  DARK  100x100, 3 rows                                            |
  |  MID   150x300, 1 row                                             |
  |  LIGHT 300-wide columns, 300/450/600 long                         |
  |  MID   150x300, 1 row                                             |
  |  DARK  100x100, 3 rows                                            |
  +====+           +==================================================+ y = 0
       | WEST      |  [LAVANDULA]       [MIXBORDER S]
       | POCKET    |
       +-----------+ y = -3500
  x=0  1000     5000                                 45000     49000  50000
```

A north arrow stands west of the alley, at (-3000, 4500).

### Tile composition, cross-section (3000 mm)

Five bands from south to north, symmetric about the centre line. Joints are 5 mm everywhere, including between bands. Each band has its own column grid; columns run across the alley (along Y).

| Band | Y range (mm) | Tiles | Layer (ACI) |
|------|--------------|-------|-------------|
| Edge S | 0 to 310 | 100 x 100, 3 rows | TILE_DARK (250) |
| Transition S | 315 to 615 | 150 x 300 (300 x 150 tile, long side across the alley), 1 row | TILE_MID (252) |
| Centre | 620 to 2380 | 300-wide columns of 300 x 600, 300 x 450 and 300 x 300 tiles | TILE_LIGHT (254), fillers on TILE_MID |
| Transition N | 2385 to 2685 | 150 x 300, 1 row | TILE_MID (252) |
| Edge N | 2690 to 3000 | 100 x 100, 3 rows | TILE_DARK (250) |

Centre band rules (`fill_center_zone`): each column picks tile lengths at random from 600, 450 and 300 with weights 3:3:4. Odd columns start with a 300 x 150 tile so joints stagger between columns. The space left at the top of a column is filled with a 300 x 150 tile, then a cut tile up to the transition band. `SEED = 42` makes every build identical.

Cut tiles (`tile_runs`): every band, and the pocket grids, runs edge to edge. Whole tiles are laid from the west (or south) edge; if at least `MIN_CUT = 20` mm is left at the far edge, a tile is cut to fit it. The last centre column at the east end is 285 mm wide, the last transition tile 90 mm and the last edge tile 20 mm.

Tile counts in the current build:

| Tile | Count |
|------|-------|
| 100 x 100 (edge bands) | 2856 |
| 150 x 300 (transition bands) | 644 |
| 300 x 150 (centre fillers) | 136 |
| 300 x 300 (centre) | 293 |
| 300 x 450 (centre) | 153 |
| 300 x 600 (centre) | 153 |
| 300 x 300 (pockets) | 286 |
| Cut tiles, alley (east end and top of each centre column) | 177 |
| Cut tiles, pockets (far edges) | 50 |
| Total | 4748 |

## Seating pockets

Each pocket is 4000 x 3500 mm, paved edge to edge with 300 x 300 tiles on a plain grid: 13 x 11 whole tiles plus a 35 mm cut column on the east side and a 145 mm cut row on the north side (168 tiles, layer TILE_POCKET, ACI 253). In the west pocket the cut row meets the alley; in the east pocket it is at the back. The alley curb is left out across the pocket opening; the other three sides have their own 150 mm curb.

### West pocket (south side)

- Paved area x 1000 to 5000, y -3500 to 0
- Pergola 3500 x 3000 at (1250, -3250), combined timber and metal
- Two benches 1800 x 500 under the pergola, SW corners at (1600, -2800) and (1600, -1700)
- Spiraea Ø1000 at (300, -1750) and (5700, -1750); Berberis Ø1200 at (3000, -4350), 100 mm off the pocket curb

### East pocket (north side)

- Paved area x 45000 to 49000, y 3000 to 6500
- Pergola 3500 x 3000 at (45250, 3250)
- Two benches 1800 x 500, SW corners at (45600, 3700) and (45600, 4800)
- Spiraea Ø1000 at (44300, 4750) and Ø600 at (49600, 4750); Berberis Ø1200 at (47000, 7350), 100 mm off the pocket curb

## Elements

| Element | Position (x, y) | Size (mm) | Function | Layer |
|---------|-----------------|-----------|----------|-------|
| Alley outline | (0, 0) to (50000, 3000) | 50000 x 3000 | `msp.add_lwpolyline` in build.py | CURB |
| South curb | y -150 to 0; x 0 to 1000 and 5000 to 50000 | 150 wide | `draw_rect` | CURB |
| North curb | y 3000 to 3150; x 0 to 45000 and 49000 to 50000 | 150 wide | `draw_rect` | CURB |
| Pocket curbs | three outer sides of each pocket | 150 wide | `draw_rect` | CURB |
| Alley paving | five bands, see above | 4412 tiles | `fill_grid`, `fill_center_zone` (build.py) using `draw_rect` | TILE_DARK, TILE_MID, TILE_LIGHT |
| Pocket paving | both pockets | 336 tiles | `fill_pocket` (build.py) | TILE_POCKET |
| Pergolas (2) | (1250, -3250), (45250, 3250) | 3500 x 3000 | `draw_pergola` | PERGOLA |
| Benches (4) | see pockets | 1800 x 500 | `draw_bench` | FURNITURE |
| Shrubs (6) | see pockets | Ø600 to Ø1200 | `draw_shrub` | SHRUBS |
| LAVANDULA bed | corners (7500, -1800) to (10500, -400) | 3000 x 1400 | `draw_flower_bed` | FLOWER_BEDS |
| MIXBORDER south | corners (21000, -1500) to (26000, -400) | 5000 x 1100 | `draw_flower_bed` | FLOWER_BEDS |
| MIXBORDER north | corners (23000, 3400) to (28000, 4500) | 5000 x 1100 | `draw_flower_bed` | FLOWER_BEDS |
| ROSES & GRASSES bed | corners (40000, 3400) to (43000, 4800) | 3000 x 1400 | `draw_flower_bed` | FLOWER_BEDS |
| Accent bed | centre (25000, 5800), label "ACCENT BED" | Ø2000 | `draw_round_bed` | FLOWER_BED_ROUND, FLOWER_BED_ROUND_FILL |
| North arrow | (-3000, 4500) | 1500 | `draw_compass` | COMPASS |
| Width dimension | (0, 3000) to (0, 0) | 3 m | `draw_distance` | DIMENSIONS |
| Length dimension | (0, -3650) to (50000, -3650) | 50 m | `draw_distance` | DIMENSIONS |
| Title | (18000, 9000) | "SCHOOL ALLEY", 600 high | `msp.add_text` | LABELS |
| Subtitle | (15000, 8200) | "Gradient Tile Composition — 3m x 50m", 300 high | `msp.add_text` | LABELS |
| Band labels | x = -5000; y 80, 350, 1400 | DARK, MID, LIGHT, 150 high | `msp.add_text` | LABELS |

`draw_flower_bed` rounds the outline through the given corners, so the drawn beds are larger than the corner box. The LAVANDULA bed, for example, spans x 7125 to 10875 and y -1975 to -225; the north MIXBORDER reaches y = 4638. All beds sit at least 225 mm from the paving, 540 mm from the nearest shrub, and the accent bed is 168 mm from the north MIXBORDER.

## Plant palette

| Plant | Qty | Size | Position | Why |
|-------|-----|------|----------|-----|
| Spiraea | 4 | Ø1000 (3), Ø600 (1) | Flanking both pockets | Suits the Sofia climate; shrubs by the benches give a sense of shelter (brief) |
| Berberis | 2 | Ø1200 | Behind each pocket | Suits the Sofia climate; encloses the back of the pocket |
| Lavender (*Lavandula*) with "shapcheta" | 1 bed | 3000 x 1400 | South side, x 7500 to 10500 | Named in the first draft; "shapcheta" is the original Bulgarian term, species to be confirmed |
| Mixed border | 2 beds | 5000 x 1100 | Centre, south and north | Flower compositions along the alley (brief) |
| Roses and ornamental grasses | 1 bed | 3000 x 1400 | North side, x 40000 to 43000 | Flower compositions along the alley (brief) |
| Accent bed | 1 | Ø2000 | North of the centre, (25000, 5800) | Focal point; planting not specified |

## Materials

- Paving: tiles in five sizes, one thickness, 5 mm joints; dark (ACI 250), medium (252) and light (254) tones; pocket tiles in a medium tone (253)
- Curbs: 150 mm
- Pergolas: combined timber and metal, four 200 mm posts each
- Benches: no tables

## Layers

| Layer | ACI | Content |
|-------|-----|---------|
| CURB | 8 | Curbs and alley outline |
| TILE_DARK | 250 | 100 x 100 edge tiles |
| TILE_MID | 252 | 150 x 300 transition tiles, 300 x 150 centre fillers and centre cut tiles |
| TILE_LIGHT | 254 | Large centre tiles |
| TILE_POCKET | 253 | Pocket paving |
| PERGOLA | 33 | Pergolas |
| FURNITURE | 6 | Benches |
| SHRUBS | 3 | Shrubs |
| FLOWER_BEDS | 200 | Bed outlines and labels |
| FLOWER_BEDS_FILL | 200 | Bed hatches |
| FLOWER_BED_ROUND | 200 | Accent bed outline and label |
| FLOWER_BED_ROUND_FILL | 200 | Accent bed hatch |
| COMPASS | 7 | North arrow |
| DIMENSIONS | 8 | Dimensions |
| LABELS | 7 | Title and band labels |

## Build phases

1. Alley outline and curbs
2. Tile composition (five bands)
3. Seating pockets: paving, pergolas, benches, shrubs
4. Flower beds
5. North arrow, labels and dimensions

## Changes from the first draft

- Band widths: the first draft used 300 / 450 / 1500 / 450 / 300 mm bands with tiles laid in rows along the alley and a brick offset. The build uses 310 / 300 / 1760 / 300 / 310 mm bands with tiles in columns across the alley and no brick offset. Each transition band is one row of 150 x 300 tiles, not three rows.
- East-end Spiraea: reduced from Ø1000 to Ø600 and moved to (49600, 4750), so it ends at x = 49900 and stays 150 mm off the pocket curb. Before, it extended 200 mm past the end of the alley into the school building.
- Dimensions: real AutoCAD DIMENSION entities from `draw_distance`, not free text.
- Layers: the rectangular beds are on FLOWER_BEDS (ACI 200) instead of FLOWERS (83); the accent bed has its own FLOWER_BED_ROUND layer so a clearance rule can check it against the other beds.
- Paving: every band and both pockets now run edge to edge with cut tiles. Before, the paving stopped 25 to 290 mm short of the east end, each centre column stopped 80 to 95 mm short of the north transition band, and the pockets had 40 mm and 150 mm unpaved strips.
- LAVANDULA bed: moved east from x 6000-9000 to x 7500-10500, clear of the Spiraea and its label.
- Accent bed: moved north from y = 5500 to 5800, clear of the north MIXBORDER.
- Berberis: moved 150 mm further from each pocket so they no longer overhang the curbs.
- North arrow added.
