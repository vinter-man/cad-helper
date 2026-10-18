"""Library drawing functions: layers, geometry and the bugs they used to have."""

import pytest
from ezdxf import bbox

from cad_helper.core import create_document
from cad_helper.japanese import draw_stepping_stones, draw_zen_garden
from cad_helper.lighting import draw_lights_along_path
from cad_helper.site import draw_fence, draw_house
from cad_helper.zones import draw_zone


@pytest.fixture
def drawing():
    doc = create_document()
    return doc, doc.modelspace()


@pytest.mark.parametrize("side", ["south", "north", "east", "west"])
def test_fence_leaves_gate_open_on_every_side(drawing, side):
    """Regression: on the north and west sides the fence used to be drawn across the gate."""
    doc, msp = drawing
    draw_fence(
        msp,
        doc,
        width=10_000,
        length=8_000,
        gates=[{"side": side, "center": 3_000, "opening": 1_000}],
    )
    horizontal = side in ("south", "north")
    for line in msp.query('LINE[layer=="FENCE"]'):
        s, e = line.dxf.start, line.dxf.end
        lo, hi = sorted((s.x, e.x) if horizontal else (s.y, e.y))
        fixed = s.y if horizontal else s.x
        on_side = {
            "south": fixed == 0,
            "north": fixed == 8_000,
            "west": fixed == 0,
            "east": fixed == 10_000,
        }[side]
        if on_side:
            assert hi <= 2_500 or lo >= 3_500, f"fence crosses the gate: {lo}-{hi}"


def test_fence_only_on_requested_sides(drawing):
    """A wall closes the south side, so the fence and its gate go on the other three."""
    doc, msp = drawing
    draw_fence(
        msp,
        doc,
        width=8_000,
        length=8_000,
        gates=[{"side": "west", "center": 4_000, "opening": 1_000}],
        sides=("east", "north", "west"),
    )
    lines = list(msp.query('LINE[layer=="FENCE"]'))
    assert lines
    assert not any(ln.dxf.start.y == 0 and ln.dxf.end.y == 0 for ln in lines)
    assert len(msp.query('ARC[layer=="GATES"]')) == 1
    with pytest.raises(ValueError):
        draw_fence(
            msp,
            doc,
            8_000,
            8_000,
            gates=[{"side": "south", "center": 1, "opening": 1}],
            sides=("north",),
        )
    with pytest.raises(ValueError):
        draw_fence(msp, doc, 8_000, 8_000, sides=("up",))


@pytest.mark.parametrize("side", ["south", "north", "east", "west"])
def test_house_entrance_on_every_side(drawing, side):
    """Regression: east and west entrances used to be silently skipped."""
    doc, msp = drawing
    draw_house(msp, doc, x=0, y=0, w=10_000, h=8_000, entrance_side=side)
    assert len(msp.query('ARC[layer=="HOUSE"]')) == 1


def test_house_rejects_unknown_side(drawing):
    doc, msp = drawing
    with pytest.raises(ValueError):
        draw_house(msp, doc, x=0, y=0, w=1, h=1, entrance_side="up")


def test_zone_rejects_unknown_hatch_pattern(drawing):
    """Typos used to fall back silently to ANSI31."""
    doc, msp = drawing
    with pytest.raises(ValueError, match="Unknown hatch pattern"):
        draw_zone(msp, doc, [(0, 0), (1, 0), (1, 1)], "X", hatch_pattern="GRAS")


def test_zen_rake_lines_stay_inside_the_garden(drawing):
    """Regression: rake lines used to run across the whole bounding box."""
    doc, msp = drawing
    boundary = [(0, 0), (4_000, 0), (3_500, 3_000), (500, 3_000)]  # trapezoid
    draw_zen_garden(msp, doc, boundary, stones=[{"cx": 2_000, "cy": 1_500}], rake_spacing=200)
    lines = msp.query('LINE[layer=="ZEN_GARDEN_GRAVEL"]')
    assert len(lines) > 10
    box = bbox.extents(lines)
    assert box.extmin.x >= -1e-6 and box.extmax.x <= 4_000 + 1e-6
    assert box.extmin.y >= -1e-6 and box.extmax.y <= 3_000 + 1e-6
    # No rake line passes through the stone's ripple rings (rx 400 * 2.5 = 1000).
    for line in lines:
        s, e = line.dxf.start, line.dxf.end
        if abs(s.y - 1_500) < 1:
            assert max(s.x, e.x) <= 1_000 + 1 or min(s.x, e.x) >= 3_000 - 1


def test_stepping_stones_are_evenly_spaced_round_corners(drawing):
    """Regression: spacing restarted at every waypoint, bunching stones at corners."""
    doc, msp = drawing
    draw_stepping_stones(
        msp, doc, [(0, 0), (1_300, 0), (1_300, 1_300)], stone_size=400, spacing=250
    )
    assert len(msp.query('LWPOLYLINE[layer=="STEPPING_STONES"]')) == 5  # 0, 650, ..., 2600


def test_lights_along_path(drawing):
    doc, msp = drawing
    draw_lights_along_path(msp, doc, [(0, 0), (6_000, 0), (6_000, 3_000)], spacing=3_000)
    centres = sorted(
        (round(c.dxf.center.x), round(c.dxf.center.y))
        for c in msp.query("CIRCLE")
        if c.dxf.radius == 150
    )
    assert centres == [(0, 0), (3_000, 0), (6_000, 0), (6_000, 3_000)]
