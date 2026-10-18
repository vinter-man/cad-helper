"""Tile layouts must stay inside the area, never overlap, and count what they draw."""

import ezdxf
import pytest

from cad_helper.patterns import create_border, create_grid, create_herringbone, create_paving

GAP = 5


def tiles(path):
    doc = ezdxf.readfile(path)
    rects = []
    for e in doc.modelspace().query("LWPOLYLINE"):
        if e.dxf.layer.startswith(("TILE", "BORDER_TILES")):
            xs = [p[0] for p in e.get_points("xy")]
            ys = [p[1] for p in e.get_points("xy")]
            rects.append((min(xs), min(ys), max(xs), max(ys)))
    return doc, rects


def assert_inside(rects, length, width):
    for x0, y0, x1, y1 in rects:
        assert x0 >= -1e-6 and y0 >= -1e-6
        assert x1 <= length + 1e-6 and y1 <= width + 1e-6


def assert_no_overlap(rects):
    rects = sorted(rects)
    for i, (ax0, ay0, ax1, ay1) in enumerate(rects):
        for bx0, by0, bx1, by1 in rects[i + 1 :]:
            if bx0 >= ax1:
                break  # sorted by x0: nothing further right can overlap
            overlap_x = min(ax1, bx1) - max(ax0, bx0)
            overlap_y = min(ay1, by1) - max(ay0, by0)
            assert not (overlap_x > 1e-6 and overlap_y > 1e-6), (rects[i], (bx0, by0, bx1, by1))


def coverage(rects, length, width):
    return sum((x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in rects) / (length * width)


LAYOUTS = {
    "stack": lambda out: create_grid(1200, 3000, 600, 300, GAP, output=out),
    "running": lambda out: create_grid(1200, 3000, 600, 300, GAP, offset_rows=True, output=out),
    "herringbone": lambda out: create_herringbone(1500, 2000, 300, 100, GAP, output=out),
    "paving": lambda out: create_paving(2000, 3000, gap=GAP, output=out),
    "border": lambda out: create_border(2000, 3000, 300, 150, GAP, border_rows=2, output=out),
}


@pytest.mark.parametrize("name", LAYOUTS)
def test_layout_is_valid_dxf_inside_and_non_overlapping(name, tmp_path):
    result = LAYOUTS[name](tmp_path / f"{name}.dxf")
    doc, rects = tiles(result.path)
    assert doc.audit().has_errors is False
    width, length = {
        "stack": (1200, 3000),
        "running": (1200, 3000),
        "herringbone": (1500, 2000),
        "paving": (2000, 3000),
        "border": (2000, 3000),
    }[name]
    assert_inside(rects, length, width)
    assert_no_overlap(rects)
    counted = sum(c["full"] + c["cut"] for c in result.counts.values())
    assert counted == len(rects)


@pytest.mark.parametrize("name", ["stack", "running", "herringbone", "paving"])
def test_field_patterns_cover_the_area(name, tmp_path):
    """Tiles plus joints fill the whole area: no holes along the edges."""
    result = LAYOUTS[name](tmp_path / f"{name}.dxf")
    _, rects = tiles(result.path)
    width, length = {
        "stack": (1200, 3000),
        "running": (1200, 3000),
        "herringbone": (1500, 2000),
        "paving": (2000, 3000),
    }[name]
    # 5 mm joints on 100-600 mm tiles take 2-8 % of the area.
    assert 0.90 < coverage(rects, length, width) <= 1.0


def test_running_bond_has_cut_tiles_at_row_ends(tmp_path):
    result = create_grid(1200, 3000, 600, 300, GAP, offset_rows=True, output=tmp_path / "r.dxf")
    assert result.counts["TILE_600x300"]["cut"] > 0


def test_herringbone_needs_oblong_tiles(tmp_path):
    with pytest.raises(ValueError):
        create_herringbone(1000, 1000, 200, 200, output=tmp_path / "h.dxf")


def test_paving_tiles_keep_their_real_size(tmp_path):
    """Regression: 600x600 tiles used to be squashed to the row height (600x300)."""
    result = create_paving(3000, 3000, tiles=[(600, 600), (600, 300)], output=tmp_path / "p.dxf")
    doc = ezdxf.readfile(result.path)
    for e in doc.modelspace().query('LWPOLYLINE[layer=="TILE_600x600"]'):
        ys = [p[1] for p in e.get_points("xy")]
        height = max(ys) - min(ys)
        assert height == pytest.approx(600) or max(ys) == pytest.approx(3000)  # full or cut at top
