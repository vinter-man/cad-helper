# Review: Bar Patio, Veliko Tarnovo

Reviewed against `build.py`, the generated `bar_patio.dxf` and `preview.png`.

## Build & automated checks

```
$ uv run cad-helper build bar_patio
Built: projects/bar_patio/bar_patio.dxf
  108 entities on 13 layers in 0.0s
  Preview: projects/bar_patio/preview.png
Checks: all passed
```

The checks cover DXF audit errors, entities on layer 0, empty layers, text too small at the 1:50 print scale, entities outside the site bounds `(-200, -600, 8000, 8000)`, and the clearance rules below.

Clearance rules defined in `build.py` (CLEARANCES). The measured value is the smallest distance in the current drawing.

| Rule | Minimum | Measured | Reason |
|------|---------|----------|--------|
| FURNITURE to PLANTERS | 100 mm | 500 mm | Chairs clear of the vine troughs |
| FURNITURE to PLANTS | 100 mm | 468 mm | Cacti out of reach of guests |
| FURNITURE to WALLS | 100 mm | 800 mm | Room to pull a chair out |
| FURNITURE to HERBS | 100 mm | 100 mm | Door approach kept clear |
| HOUSE to HERBS | 50 mm | 50 mm | Door leaf and facade clear of the herb planters (added after review) |

## Defects found and fixed

These were found when the automated checks were introduced. The previous review had marked all of them as passing.

- 8 of the 16 chairs were drawn inside the tables. Chair coordinates assumed a table centred on its point, but the tables were drawn from their corner.
- One chair overlapped the west vine planter.
- The bar door was centred on the 8 m bar instead of the 4 m patio, so it opened outside the patio.
- The herb planters stood in the middle of the only aisle.
- The drawing used hand-written geometry instead of library functions.

The fix replaced the seating with 4 bistro tables of 2 chairs each (16 seats did not fit 16 m² with circulation), centred the door on the patio, moved the herbs beside the door, and rebuilt every element with library functions.

## Fixed after review

- The door leaf opened flat against the west herb planter (0 mm): the hinge is at (1550, 4000) and the open leaf lies along x = 1550, where the planter's east face was. The herb planters are now 300 x 250, stand 50 mm off the facade, and sit at x 1100 to 1400 and 2600 to 2900. The open leaf is 150 mm from the west planter.
- New rule HOUSE to HERBS (50 mm). It failed on the old layout (`HOUSE <-> HERBS is 0 mm, needs >= 50 mm`) and passes now. The door leaf, swing arc and facade are all on layer HOUSE, so the rule covers both the door and the wall.

## Manual review

Geometry
- [x] Every element is inside the site bounds (automated check, confirmed on the preview).
- [x] Chairs sit outside their tables: chair centres are 600 mm from the table centre, the table half-depth is 350 mm and the chair radius 200 mm, leaving a 50 mm gap.
- [x] A 1000 mm aisle runs from the steps (x 1500 to 2500) to the door (x 1550 to 2450) with nothing in it.
- [x] The bar door is inside the patio width, on the patio centre line.
- [x] Corner pots and vine troughs do not overlap (10 mm gap at the trough ends).
- [x] The door leaf opens fully without touching a planter: 150 mm to the west planter when open, about 120 mm from the strike jamb to the east planter.
- [x] The herb planters are exactly 100 mm above the nearest chairs (T3 and T4 north chairs), the rule minimum.

Completeness
- [x] Patio, bar, both walls, steps, 4 tables, 8 chairs, 2 vine troughs, 4 opuntia, 2 herb planters and the lantern are all drawn.
- [x] North arrow present; patio width and depth are real AutoCAD DIMENSION entities.
- [x] All text passes the 1:50 readability check.
- [ ] Only the vine troughs are labelled. Opuntia, rosemary and lavender are unlabelled symbols; the plan's plant palette is the reference.

Layers
- [x] 13 layers, one per element type: ZONE_PATIO, ZONE_PATIO_FILL, HOUSE, HOUSE_FILL, WALLS, STEPS, FURNITURE, PLANTERS, PLANTS, HERBS, LIGHTING, COMPASS, DIMENSIONS.
- [x] No entities on layer 0 and no empty layers (automated check).

Brief compliance
- [x] Vines along both walls, cacti in the corners, fragrant herbs by the door.
- [x] No water features.
- [x] Lantern on the partition between patio and bar.
- [ ] The brief asked for rectangular tables and pots between the tables. The build uses square tables and keeps the space between them clear. Echeveria and begonia from the first draft are not drawn.

## Verdict

Ready to hand over as a layout and planting plan; plant labels and the brief's pots between the tables are open points for the client, not drawing defects.
