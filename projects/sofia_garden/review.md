# Review: Sofia garden (revision 2)

## Build and automated checks

```
$ uv run cad-helper build sofia_garden
Built: projects/sofia_garden/sofia_garden.dxf
  149 entities on 26 layers in 0.0s
  Preview: projects/sofia_garden/preview.png
Checks: all passed
```

The first revision-2 build did not pass:

```
Checks: 2 error(s), 0 warning(s)
  [error] clearance: FIRE_PIT <-> NIWAKI is 1549 mm, needs >= 3000 mm (sparks vs pine crown)
  [error] clearance: FIRE_PIT_SEATING <-> POND* is 0 mm, needs >= 300 mm (bench stays on dry ground)
```

Fixed by moving the pine 1.4 m east and the fire pit 0.5 m south-west.

## Found by looking at preview.png

- The revision-1 lawn outline ran under the enlarged pond. Redrawn north of the pond, and
  a `LAWN <-> POND*` rule added so it cannot happen again.
- The pine label ran into the main path stones. Shortened to "Pine".
- The fire circle had no path to it. Added a branch that arrives at the open side of the bench.

## Manual checklist

- [x] Gate → deck → house door is one continuous path
- [x] Every zone is reachable: deck, grill (from the deck), pond edge, fire circle
- [x] Door swing (1000 mm) lands on the deck, not on planting
- [x] Fire pit 3+ m from all tree crowns and 4+ m from the house (rule-checked)
- [x] Grill is 3+ m from the trees; it sits 300 mm from the house wall, which assumes
      a gas or electric grill. Open charcoal needs the counter turned away from the wall.
- [x] Hedge on the east side, as asked
- [x] Labels readable at 1:100, none overlapping after the fix above
- [ ] Pond depth and edge detail: not part of this plan drawing

## Open questions for the client

- Grill fuel type (affects the distance to the house wall).
- Whether the dog needs a fenced-off area away from the pond.

Verdict: ready to send as a concept plan.
