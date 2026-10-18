# Review: School Alley, Sofia

Reviewed against `build.py`, the generated `school_alley.dxf` and `preview.png`.

## Build & automated checks

```
$ uv run cad-helper build school_alley
Built: projects/school_alley/school_alley.dxf
  4864 entities on 15 layers in 0.5s
  Preview: projects/school_alley/preview.png
Checks: all passed
```

The checks cover DXF audit errors, entities on layer 0, empty layers, text too small at the 1:100 print scale, entities outside the site bounds `(-6000, -5000, 50000, 13500)`, and the clearance rules below. The east bound of 50000 is the school building at the end of the alley.

Clearance rules defined in `build.py` (CLEARANCES). The measured value is the smallest distance in the current drawing.

| Rule | Minimum | Measured | Reason |
|------|---------|----------|--------|
| FLOWER_BEDS to TILE_* | 150 mm | 225 mm | Beds stay off the paving |
| SHRUBS to TILE_POCKET | 100 mm | 200 mm | Shrubs outside the seating pockets |
| SHRUBS to CURB | 50 mm | 50 mm | Shrubs planted off the curbs (added after review) |
| SHRUBS to FLOWER_BEDS | 100 mm | 540 mm | Shrubs and beds kept apart (added after review) |
| FLOWER_BED_ROUND to FLOWER_BEDS | 100 mm | 168 mm | Accent bed clear of the mixborder (added after review) |

## Defects found and fixed

These were found when the automated checks were introduced. The previous review had marked them as passing.

- The east Spiraea extended 200 mm past the end of the alley into the school building.
- The old review claimed a "brick offset" row pattern and "3 rows of transition tiles". The code never drew either. The plan now describes what the code draws: columns across the alley and one row of transition tiles per side.
- Dimension text was free text instead of real AutoCAD dimensions. Both dimensions are now DIMENSION entities from `draw_distance`.

## Fixed after review

- The Spiraea at (5700, -1750) overlapped the LAVANDULA bed. The bed moved east to x 7500 to 10500.
- The round accent bed overlapped the north MIXBORDER by about 140 mm. It moved north to (25000, 5800) and got its own layer, FLOWER_BED_ROUND, so a rule can check it against the other beds.
- Both Berberis and the east-end Spiraea overhung the pocket curbs by 50 mm. The Berberis moved 150 mm away from their pockets. The east-end Spiraea is now Ø600 at (49600, 4750).
- The paving stopped short at the east end: 290 mm in the centre band, 95 mm in the transition bands and 25 mm in the edge bands. Each centre column also stopped 80 to 95 mm short of the north transition band. This gap was not in the first review. The pocket grids left 40 mm and 150 mm unpaved strips. `fill_grid` and `fill_center_zone` now add a cut tile wherever at least 20 mm is left (`tile_runs`, `MIN_CUT = 20`).
- No north arrow. Added with `draw_compass` at (-3000, 4500).

The three new rules failed on the old layout and pass now. Old layout with the new rules:

```
[error] clearance: SHRUBS <-> CURB is 0 mm, needs >= 50 mm (shrubs planted off the curbs)
[error] clearance: SHRUBS <-> FLOWER_BEDS is 0 mm, needs >= 100 mm (shrubs and beds kept apart)
[error] clearance: FLOWER_BED_ROUND <-> FLOWER_BEDS is 0 mm, needs >= 100 mm (accent bed clear of the mixborder)
```

Paving coverage cannot be written as a clearance rule. It was checked with a script that reads the tile extents from the DXF (see below).

## Manual review

Geometry
- [x] Every element is inside the site bounds; nothing crosses x = 50000 (automated check, confirmed on the preview).
- [x] Pockets sit at opposite ends and on opposite sides: west pocket south of the alley, east pocket north of it.
- [x] Pergolas and benches are inside their pockets; the benches sit under the pergolas.
- [x] All flower beds are outside the curbs, at least 225 mm from the paving and 540 mm from the nearest shrub.
- [x] The accent bed is 168 mm from the north MIXBORDER.
- [x] No shrub touches a curb. The closest are the two Spiraea per pocket, 50 mm off the pocket side curbs.

Paving
- [x] All five bands run from x = 0 to x = 50000 exactly. Every one of the 164 centre columns runs from y = 620 to 2380 with no gap larger than a 5 mm joint.
- [x] Both pockets are paved edge to edge: x 1000 to 5000, y -3500 to 0 (west) and x 45000 to 49000, y 3000 to 6500 (east).
- [x] All five tile sizes are used: 100 x 100, 300 x 150, 300 x 300, 300 x 450 and 300 x 600. There are 4521 whole tiles and 227 cut tiles (counts in the plan).
- [x] Dark edges, mid transitions, light centre, by layer colour (ACI 250, 252, 254).
- [x] The centre band is identical on every build (`SEED = 42`).
- [ ] The narrowest cut tiles are 20 mm (east end of the edge bands) and 35 mm (pocket edges). That is legal under `MIN_CUT`, but a contractor would usually shift the grid to avoid slivers. Open point.

Completeness
- [x] Two pockets, each with a pergola, two benches and three shrubs.
- [x] Five flower beds: LAVANDULA, two MIXBORDER beds, ROSES & GRASSES and the accent bed.
- [x] North arrow, width and length dimensions, title, band labels.
- [ ] The Spiraea labels west of each pocket run into the pocket paving, because `draw_shrub` always places the label to the right of the shrub. Cosmetic only.

Layers
- [x] 15 layers: CURB, TILE_DARK, TILE_MID, TILE_LIGHT, TILE_POCKET, PERGOLA, FURNITURE, SHRUBS, FLOWER_BEDS, FLOWER_BEDS_FILL, FLOWER_BED_ROUND, FLOWER_BED_ROUND_FILL, COMPASS, DIMENSIONS, LABELS.
- [x] No entities on layer 0 and no empty layers (automated check).

Brief compliance
- [x] 3 x 50 m alley with 150 mm curbs, light centre grading to dark edges.
- [x] Seating pockets at both ends, benches only, combined timber and metal pergolas, shrubs by the benches.
- [ ] Pocket depth is 3500 mm; the brief says up to 3000 mm. This needs a decision from the client.

## Verdict

Ready to hand over as a concept plan. The 3500 mm pocket depth against the brief's 3000 mm and the narrow cut tiles at the edges are the open points.
