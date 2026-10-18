# Review: Playground between apartment blocks, Sofia

Reviewed against `build.py`, the generated `playground.dxf` and `preview.png`.

## Build & automated checks

```
$ uv run cad-helper build playground
Built: projects/playground/playground.dxf
  178 entities on 21 layers in 0.0s
  Preview: projects/playground/preview.png
Checks: all passed
```

The checks cover DXF audit errors, entities on layer 0, empty layers, text too small at the 1:50 print scale, entities outside the site bounds `(0, 0, 8000, 8000)`, and the clearance rules below.

Clearance rules defined in `build.py` (CLEARANCES). The measured value is the smallest distance in the current drawing.

| Rule | Minimum | Measured | Reason |
|------|---------|----------|--------|
| SLIDES to SOUND_BARRIER | 1000 mm | 2200 mm | Run-out clear of the road-side wall |
| CLIMBING to FENCE | 1000 mm | 1100 mm | Fall zone inside the fence |
| BENCHES to ISLAND_* | 300 mm | 386 mm | Parents sit off the play surface |
| SLIDES to BRIDGES | 100 mm | 174 mm | Bridges land on the rubber, not on a slide (added after review) |
| GATES to SHRUBS | 100 mm | 166 mm | Gate leaf swings clear of the shrubs (added after review) |
| GATES to FURNITURE | 100 mm | 250 mm | Bins clear of the open gate leaf (added after review) |

## Defects found and fixed

These were found when the automated checks were introduced. The previous review had marked all of them as passing.

- The shrubs behind the north benches crossed the north fence, reaching y = 8200 on an 8000 mm site.
- The west and east shrubs crossed the side fences.
- The bench next to the climbing island was 215 mm from the play surface.
- The two slides overlapped each other.
- The bridges were attached using parametric instead of polar ellipse angles, so their ends missed the island edges.
- Ground lights overlapped a bench and a bin.

## Fixed after review

- Bridge 2-3 landed on slide 1: its rail and first plank crossed the slide body and platform.
- Both slides stuck out past the edge of island 2 onto gravel.
- The gate leaves swept through the shrubs at (350, 5250) and (7400, 5050). Both bins straddled the line of the open leaf, and two ground lights stood inside the swings.
- The fence and gates were hand-written lines and arcs. They are now drawn by `draw_fence`, which gained a `sides` parameter so the fence can skip the south side where the sound barrier stands (covered by a new test in `tests/test_elements.py`).

Slides are now two 1200 mm slides side by side on island 2, both running south. The bins moved to y = 3500, the gate lights to y = 2800, and the gate shrubs to y = 5550.

The three new rules failed on the old positions and pass on the new ones. Old layout with the new rules:

```
[error] clearance: SLIDES <-> BRIDGES is 0 mm, needs >= 100 mm (bridges land on the rubber, not on a slide)
[error] clearance: GATES <-> SHRUBS is 0 mm, needs >= 100 mm (gate leaf swings clear of the shrubs)
[error] clearance: GATES <-> FURNITURE is 0 mm, needs >= 100 mm (bins clear of the open gate leaf)
```

Limits of the rules: the clearance check measures outline to outline, and a gate swing is an open arc. A light or shrub sitting wholly inside a swing never touches the arc, so a GATES to GROUND_LIGHTS rule did not fail on the old layout and was not added. The same applies to "slides fully on the island" and "slides apart from each other": a rule cannot express containment, and a layer compared with itself always measures 0. These three conditions were checked with a script instead (see below).

## Manual review

Geometry
- [x] Every element is inside the site (automated check). The outermost shrubs stop 50 mm inside the fence.
- [x] The three islands do not overlap; the shortest gap (islands 1 and 3) is 470 mm, spanned by a bridge.
- [x] Every corner of both slides lies inside island 2 (worst point at 0.87 of the ellipse radius).
- [x] The two slides are 385 mm apart, and neither slide label overlaps the other slide or the island label (checked on the preview).
- [x] Each bridge starts and ends on an island edge, and the nearest bridge is 174 mm from a slide.
- [x] Nothing stands in either gate swing. The nearest shrub is 1364 mm from a hinge (radius 1200), the nearest bench corner 1304 mm, and the nearest ground light 900 mm from any gate geometry. The bins are 250 mm south of the open leaves.
- [x] Ground lights are 164 mm from the nearest bench, 350 mm from the nearest bin and 128 mm from the nearest shrub.

Connectivity
- [x] Two gates, west and east, open onto gravel with no equipment in the way.
- [x] All three islands are linked by bridges (1-2, 1-3, 2-3), each 700 mm wide.

Completeness
- [x] Three islands with their equipment: sandbox, two slides, climbing dome.
- [x] Sound barrier on the south side; fence on the north, west and east sides.
- [x] 4 benches, 8 shrubs, 2 bins, 8 ground lights, north arrow.
- [ ] Shrub species are not specified in the brief or the drawing.
- [ ] No dimensions are drawn.

Layers
- [x] 21 layers: BOUNDARY, GRAVEL, SOUND_BARRIER, FENCE, GATES, COMPASS, ISLAND_SANDBOX(_FILL), ISLAND_SLIDES(_FILL), ISLAND_CLIMBING(_FILL), SANDBOX(_FILL), SLIDES, CLIMBING, BRIDGES, BENCHES, SHRUBS, FURNITURE, GROUND_LIGHTS.
- [x] No entities on layer 0 and no empty layers (automated check).
- [x] Fence and gates come from the library. Only the boundary outline is still a direct ezdxf call.

Brief compliance
- [x] Rubber islands, gravel between them, rubber-plank bridges.
- [x] Noise barrier against the road, ground lights, benches around the edge, bins.

## Verdict

Ready to hand over as a layout plan. Shrub species and dimensions are still open.
