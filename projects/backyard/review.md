# Review: Japanese backyard

## Build and automated checks

```
$ uv run cad-helper build backyard
Built: projects/backyard/backyard.dxf
  562 entities on 36 layers in 0.1s
  Preview: projects/backyard/preview.png
Checks: all passed
```

## Defects found and fixed

Found when the automated checks and rendered previews were introduced. The earlier
version of this design had none of them recorded.

- A moss area and the west pine crossed the west fence (x down to -503 mm).
- Maple 2 stood in the middle of the pond.
- The stream ran out of the pond into the dry garden, which defeats the point of a
  dry garden. It now runs from a spring by the house into the pond.
- The tea path crossed the bamboo fence where it had no opening. The fence now has a
  1.2 m gap and the path goes through it to the tsukubai.
- The main path ran through the pergola and over its bench. The pergola moved to the
  east shore and the path passes beside it (rule `STEPPING_STONES* <-> FUJIDANA`).
- Library bugs this design exposed: rake lines in the dry garden ran past its outline
  and through the stones; stepping stones bunched at every path corner; pond and
  stream fills were drawn white instead of water blue. All fixed in `src/cad_helper`
  with regression tests.

## Manual checklist (from preview.png)

- [x] Gate → torii → engawa is one continuous path
- [x] Tea garden reachable over the bridge and through the fence gap
- [x] Pond reachable along its north shore; pergola bench faces the water
- [x] No tree inside water or a structure; pines in three different sizes, not aligned
- [x] Lanterns at the viewpoints, not on the paths
- [x] Labels legible at 1:100; the engawa label sits under the door swing but stays readable
- [ ] Planting distances from the boundary are not set by local rules in this drawing

Verdict: ready as a concept plan.
