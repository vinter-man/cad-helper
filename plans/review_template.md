# Review Template — Phase 4 Checklist

Use this for every project delivery. Save to `reviews/<project_name>_review.md`.

---

# Review: [Project Name]

Date: [date]
Build output: [entity count] entities, [layer count] layers

## Geometry

- [ ] All elements are inside plot boundaries
- [ ] House is inside plot with correct setbacks
- [ ] No structures overlap each other
- [ ] No structures overlap paths
- [ ] No trees directly on top of structures
- [ ] Paths don't cross through buildings or water features
- [ ] Gate positions are accessible (not blocked)

## Connectivity

- [ ] There is a clear path from the gate to the house entrance
- [ ] Every major zone is reachable by path or stepping stones
- [ ] No dead-end paths that lead nowhere
- [ ] Paths are wide enough (min 600mm for stepping stones, 800mm for secondary, 1200mm for main)

## Completeness

- [ ] Every element from the plan is present
- [ ] Every zone from the plan is drawn
- [ ] Compass rose is present
- [ ] Key dimensions are labeled
- [ ] Text labels are readable (not too small, not overlapping)

## Layers

- [ ] Every element is on its own appropriate layer
- [ ] Layer names follow the convention (see CLAUDE.md)
- [ ] No elements on layer "0" (except defaults)

## Landscape Logic

- [ ] Trees are not too close to the house foundation (min 2m for small trees, 4m for large)
- [ ] BBQ / fire pit is away from overhanging branches (min 3m)
- [ ] Water features are not directly against the house wall
- [ ] Sun-loving plants are not in permanent shade (north side of house)
- [ ] Shade plants are not in full south exposure
- [ ] Spacing between trees allows for mature crown diameter

## Safety

- [ ] Pond is not adjacent to children's play area (if applicable)
- [ ] No trip hazards on main paths
- [ ] Adequate lighting on primary paths (if night use)
- [ ] Fire features have clearance from structures and plants

## Build Verification

- [ ] `python projects/<name>/build.py` runs without errors
- [ ] Output file exists and has expected entity count
- [ ] File size is reasonable (not 0 bytes, not unexpectedly huge)

## Issues Found

| # | Issue | Severity | Fixed? |
|---|-------|----------|--------|
| 1 | [description] | [critical/warning/minor] | [ ] |
| ... | ... | ... | ... |

## Verdict

- [ ] PASS — ready for delivery
- [ ] FAIL — needs fixes (return to Phase 3)
