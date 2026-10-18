import math

import pytest

from cad_helper.core import (
    clip_segment,
    offset_polyline,
    point_in_polygon,
    polygon_area,
    polygon_centroid,
    rotate_point,
    smooth_closed,
    walk_polyline,
)

SQUARE = [(0, 0), (10, 0), (10, 10), (0, 10)]
# U-shape: concave, so one line can enter and leave twice.
U_SHAPE = [(0, 0), (30, 0), (30, 20), (20, 20), (20, 10), (10, 10), (10, 20), (0, 20)]


def test_rotate_point_quarter_turn():
    x, y = rotate_point((10, 0), (0, 0), 90)
    assert (x, y) == pytest.approx((0, 10))


def test_polygon_area_and_centroid():
    assert polygon_area(SQUARE) == pytest.approx(100)
    assert polygon_centroid(SQUARE) == pytest.approx((5, 5))


def test_point_in_polygon_concave():
    assert point_in_polygon((5, 15), U_SHAPE)
    assert not point_in_polygon((15, 15), U_SHAPE)  # inside the notch


def test_clip_segment_convex():
    pieces = clip_segment((-5, 5), (15, 5), SQUARE)
    assert len(pieces) == 1
    ((a, b),) = pieces
    assert a == pytest.approx((0, 5)) and b == pytest.approx((10, 5))


def test_clip_segment_concave_gives_two_pieces():
    pieces = clip_segment((-5, 15), (35, 15), U_SHAPE)
    spans = sorted((round(a[0]), round(b[0])) for a, b in pieces)
    assert spans == [(0, 10), (20, 30)]


def test_clip_segment_outside():
    assert clip_segment((20, 20), (30, 30), SQUARE) == []


def test_smooth_closed_passes_through_control_points():
    curve = smooth_closed(SQUARE, samples=4)
    assert len(curve) == 16
    for p in SQUARE:
        assert any(math.dist(p, q) < 1e-9 for q in curve)


def test_offset_polyline_width():
    left, right = offset_polyline([(0, 0), (100, 0)], half_width=5)
    assert left == [(0, 5), (100, 5)]
    assert right == [(0, -5), (100, -5)]


def test_walk_polyline_carries_distance_round_corners():
    # 10 + 10 mm L-shape walked every 4 mm: stations at 0, 4, 8, 12, 16, 20 along the path.
    stations = walk_polyline([(0, 0), (10, 0), (10, 10)], 4)
    points = [p for p, _ in stations]
    assert points == pytest.approx([(0, 0), (4, 0), (8, 0), (10, 2), (10, 6), (10, 10)])
    assert stations[3][1] == pytest.approx((0, 1))  # direction on the second leg


def test_walk_polyline_rejects_bad_spacing():
    with pytest.raises(ValueError):
        walk_polyline([(0, 0), (1, 0)], 0)
