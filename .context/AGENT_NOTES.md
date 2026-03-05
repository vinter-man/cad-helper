# Agent Notes

Accumulated knowledge about this project and user preferences.

## User profile
- Speaks Russian, Bulgarian, and English
- Works with AutoCAD 2021
- Prefers Japanese garden aesthetic (asymmetry, stones, water, niwaki, moss)
- Prefers concise interactions — short requests, fast results
- Cares about token/credit efficiency

## Workflow patterns (user-specified)
- **Opus plans, Sonnet executes** — stronger model creates the MD plan, cheaper model implements it
- **Agent must self-test** — always run the build script before delivering
- **Mandatory review phase** — run through checklist in `plans/review_template.md` before delivery
- **Interview first** — ask maximum questions before starting (climate, style, must-haves, etc.)
- 4-phase workflow: Interview → Plan → Execute → Review
- Small tweaks skip directly to Execute phase

## Architecture decisions
- ezdxf library (Python) for DXF generation — well-documented, AutoCAD-compatible
- DXF R2010 format — maximum compatibility with AutoCAD 2010+
- All coordinates in mm, origin at south-west (0,0)
- Each visual element on its own AutoCAD layer for easy toggling
- Build script pattern: config at top, draw calls at bottom, one `build()` function
- `sys.path.insert(0, ...)` at top of build scripts to resolve lib imports

## What works well
- add_layer() is idempotent — safe to call multiple times with same name
- Hatch patterns: "AR-SAND" for gravel, "ANSI37" for vegetation, "GRASS" for lawn, "DOTS" for moss, "LINE" for wood
- B-spline paths via ezdxf.math.BSpline for smooth curves
- Irregular organic shapes: base ellipse + sine wave modulation

## Known issues
- Some hatch patterns may not exist in all DXF viewers — the code has try/except fallbacks
- Stepping stone "randomness" uses deterministic sin(seed) — looks natural enough
- Zen garden rake lines are drawn across full bounding box, may extend beyond boundary
- Stream width wobble is subtle (15%) — increase for more dramatic effect

## Current project state
- `projects/backyard/` = Japanese garden, 604 entities, 36 layers
- All lib modules tested and working
- Tile pattern generators (generate.py) also working independently
