# AGENTS.md

cad-helper turns a plain-language description of a garden into a layered AutoCAD DXF.
The agent does the design work; the Python package in `src/cad_helper` does the
drawing, renders a preview and checks the result.

## Commands

```bash
uv sync                                        # install (Python 3.11+)
uv run cad-helper new <name> --width 20000 --length 30000
uv run cad-helper build <name>                 # DXF + preview.png + checks; exit 1 on errors
uv run cad-helper render <file.dxf> -o out.png
uv run cad-helper check <file.dxf> --bounds 0,0,20000,30000
uv run cad-helper tiles herringbone --width 3000 --length 12000 --tile 300x100 --preview
uv run pytest                                  # tests
uv run ruff check . && uv run ruff format .    # lint, format
```

## Layout

- `src/cad_helper/` — drawing library (`site`, `zones`, `paths`, `furniture`,
  `planting`, `japanese`, `water`, `lighting`, `playground`), `patterns/` for tile
  layouts, `render.py`, `checks.py`, `cli.py`
- `projects/<name>/` — one folder per design: `brief.md`, `plan.md`, `build.py`,
  `review.md`, `preview.png` (committed) and `<name>.dxf` (generated, git-ignored)
- `.claude/skills/landscape-design/` — the design workflow and API reference
- `tests/` — pytest; `tests/test_projects.py` builds every project

## Conventions

- Millimetres everywhere. Origin is the south-west corner; X east, Y north.
- A project's `build.py` defines `build()` returning the ezdxf document, plus `BOUNDS`,
  `CLEARANCES` and optionally `PLOT_SCALE`. All coordinates live in its configuration
  block.
- Draw only through `cad_helper` functions. New element types go into the matching
  module with a test.
- Each element type has its own CAPS layer.
- Repository text is English, even when the conversation is not.

## Definition of done for a drawing

`uv run cad-helper build <name>` prints `Checks: all passed`, you have looked at
`preview.png`, and `review.md` records what was checked. For library changes:
`uv run pytest` and `uv run ruff check .` are clean.
