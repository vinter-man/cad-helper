# Review checklist

`cad-helper build` already verifies the mechanical part on every run:

- the DXF passes ezdxf's audit (AutoCAD will open it without recovery)
- nothing except annotation leaves `BOUNDS`
- every `CLEARANCES` rule holds, measured on the real outlines
- no entities on layer 0, no empty layers, no text below 1.5 mm at `PLOT_SCALE`

What is left is judgement. Open `preview.png` and go through these.

## Circulation
- [ ] A clear route from every gate to the house entrance
- [ ] Every zone can be reached on a path or stepping stones
- [ ] No path ends at nothing; no path runs through a structure, bed or water
- [ ] Widths: main path >= 1200 mm, secondary >= 800 mm, stepping stones >= 600 mm
- [ ] Door and gate swings are not blocked

## Planting
- [ ] Trees are drawn at mature crown size and do not hit the house (>= 2 m small, >= 4 m large)
- [ ] Sun-loving plants are not on the north side of the house; shade plants are not in full sun
- [ ] Species suit the climate in the brief

## Safety
- [ ] Fire (BBQ, fire pit) >= 3 m from trees, pergolas and the house
- [ ] Water is not next to a children's play area
- [ ] Main paths are lit if the brief mentions evening use

## Drawing quality
- [ ] Every element from the plan is drawn
- [ ] Labels are readable and do not sit on top of each other
- [ ] North arrow and overall dimensions are present
- [ ] Layer names say what is on them

## Write-up (`projects/<name>/review.md`)
- Paste the real `cad-helper build` output
- List what you checked by eye and anything you fixed
- List open questions or assumptions for the user
- Verdict: ready, or what is still missing
