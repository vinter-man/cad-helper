---
name: landscape-design
description: Design a garden, yard, patio, playground or other landscape plan and deliver it as an AutoCAD DXF. Use when the user describes a site or asks to design, draw, change or review a landscape drawing in this repo, in any language.
---

# Landscape design: brief → plan → build → review

The user describes a site in plain language (often Russian or Bulgarian); you deliver
`projects/<name>/<name>.dxf` that opens cleanly in AutoCAD. Talk to the user in their
language. Everything written to the repo is English.

## Which steps to run

| Request | Steps |
|---|---|
| New project, redesign, change of style | 1 → 2 → 3 → 4 |
| New zone or area in an existing project | 2 → 3 → 4 |
| Add / move / resize / recolour elements | 3 → 4 (short) |
| Paving or tile layout only | `uv run cad-helper tiles ...` |

## 1. Brief

Ask before drawing. One message, numbered questions, so the user can answer in one
reply. Always cover: plot size and where north is, city/climate, style, must-haves,
must-not-haves, who uses it (kids, pets, guests), privacy, maintenance time.
[interview.md](interview.md) has the full question bank; pick what the request needs.
If the user says "just do something nice", still ask the top five.

Save the answers to `projects/<name>/brief.md`.

## 2. Plan

Write `projects/<name>/plan.md` from [plan-template.md](plan-template.md): concept,
zones with positions and sizes in mm, every element with the library function that
draws it, plant palette chosen for the climate, materials, and the clearance rules the
build must satisfy. Show a short summary to the user and wait for approval.

## 3. Build

```bash
uv run cad-helper new <name> --width <mm> --length <mm>   # first time only
# edit projects/<name>/build.py
uv run cad-helper build <name>
```

`build.py` contract: a `build()` function that returns the ezdxf document, plus
`BOUNDS` (site extents), `CLEARANCES` (minimum distances between layers, written from
the plan) and optionally `PLOT_SCALE` (100 = 1:100). Keep every coordinate in the
configuration block at the top. Function signatures and conventions: [api.md](api.md).

`cad-helper build` saves the DXF, renders `preview.png` and runs the checks. It exits
non-zero on any error. Fix errors in the design, not by loosening `BOUNDS` or deleting
clearance rules.

## 4. Review

1. **Look at the drawing.** Open `projects/<name>/preview.png` with the Read tool.
   Check what the automatic checks cannot: labels colliding, paths that lead nowhere,
   a tree in the middle of a lawn you meant to keep open, an awkward composition.
2. Walk through [review-checklist.md](review-checklist.md).
3. Write `projects/<name>/review.md`: the real `cad-helper build` output, what you
   checked by eye, what you fixed. Only tick what you verified.
4. Tell the user where the DXF is, show the preview, and list anything they should
   decide (open questions, assumptions you made).

For a quick change (step 3 → 4), rebuild, look at the preview, and report in two or
three lines. No review file needed.

## Rules

- Millimetres everywhere. "3 m" is `3_000`. Origin is the south-west corner, X east,
  Y north.
- Draw only through `cad_helper` functions. If an element type is missing, add a
  function to the right module in `src/cad_helper/`, with a test in `tests/`.
- One element type per layer, named in CAPS (`POND`, `STEPPING_STONES_TEA`).
- Never deliver a drawing with check errors or one you have not looked at.
