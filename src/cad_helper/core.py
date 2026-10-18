"""Shared DXF plumbing: documents, layers, labels and 2D geometry helpers.

All coordinates are millimetres. The origin is the south-west corner of the
site, X points east and Y points north.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Sequence
from pathlib import Path

import ezdxf
from ezdxf import units
from ezdxf.document import Drawing
from ezdxf.entities import Hatch
from ezdxf.enums import TextEntityAlignment
from ezdxf.layouts import Modelspace
from ezdxf.tools.pattern import ISO_PATTERN

Point = tuple[float, float]

BYLAYER = 256  # ACI value meaning "use the layer's colour"

# Colours handed out to tile layers, one per tile size (AutoCAD Color Index).
COLOR_CYCLE = [1, 2, 3, 4, 5, 6, 30, 140, 200, 83, 33, 220]


# ─── Document ────────────────────────────────────────────────────────────────


def create_document() -> Drawing:
    """New R2010 drawing in millimetres, with AutoCAD's standard linetypes and dimstyles."""
    doc = ezdxf.new(dxfversion="R2010", setup=True, units=units.MM)
    doc.header["$MEASUREMENT"] = 1  # metric hatch patterns and linetypes
    return doc


def save(doc: Drawing, filepath: str | Path) -> Path:
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(filepath)
    return filepath


def add_layer(doc: Drawing, name: str, color: int = 7, linetype: str = "Continuous") -> None:
    """Create a layer if it does not exist yet. Safe to call repeatedly."""
    if name not in doc.layers:
        doc.layers.add(name, color=color, linetype=linetype)


def add_layers_for_tiles(doc: Drawing, tile_sizes: Sequence[Point]) -> dict[Point, str]:
    """One layer per tile size (``TILE_600x300``), so quantities can be counted per layer."""
    layer_map = {}
    for i, (w, h) in enumerate(tile_sizes):
        name = f"TILE_{int(w)}x{int(h)}"
        add_layer(doc, name, COLOR_CYCLE[i % len(COLOR_CYCLE)])
        layer_map[(w, h)] = name
    return layer_map


# ─── Text and hatches ────────────────────────────────────────────────────────


def add_label(
    msp: Modelspace,
    text: str,
    at: Point,
    *,
    height: float = 200,
    layer: str = "LABELS",
    rotation: float = 0,
    align: TextEntityAlignment = TextEntityAlignment.MIDDLE_CENTER,
) -> None:
    """Single-line text anchored at ``at`` (centred by default)."""
    entity = msp.add_text(text, height=height, rotation=rotation, dxfattribs={"layer": layer})
    entity.set_placement(at, align=align)


def set_pattern(hatch: Hatch, pattern: str, scale: float) -> None:
    """Apply a standard acad.pat pattern, failing loudly on typos instead of silently drawing ANSI31."""
    if pattern not in ISO_PATTERN:
        raise ValueError(
            f"Unknown hatch pattern {pattern!r}. Use an AutoCAD pattern name "
            "such as ANSI31, ANSI37, AR-SAND, AR-BRSTD, GRASS, DOTS or LINE."
        )
    hatch.set_pattern_fill(pattern, scale=scale)


def add_hatch(
    msp: Modelspace,
    points: Sequence[Point],
    *,
    layer: str,
    color: int | None = None,
    pattern: str | None = None,
    scale: float = 1,
) -> Hatch:
    """Hatch a closed polygon. Solid fill unless ``pattern`` is given."""
    hatch = msp.add_hatch(color=BYLAYER if color is None else color, dxfattribs={"layer": layer})
    hatch.paths.add_polyline_path(points, is_closed=True)
    if pattern:
        set_pattern(hatch, pattern, scale)
    return hatch


def add_circle_hatch(
    msp: Modelspace,
    center: Point,
    radius: float,
    *,
    layer: str,
    color: int | None = None,
    pattern: str | None = None,
    scale: float = 1,
) -> Hatch:
    hatch = msp.add_hatch(color=BYLAYER if color is None else color, dxfattribs={"layer": layer})
    hatch.paths.add_edge_path().add_arc(center=center, radius=radius, start_angle=0, end_angle=360)
    if pattern:
        set_pattern(hatch, pattern, scale)
    return hatch


# ─── Rectangles and tiles ────────────────────────────────────────────────────


def rect_points(x: float, y: float, w: float, h: float) -> list[Point]:
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def draw_rect(msp: Modelspace, x: float, y: float, w: float, h: float, layer: str = "0") -> None:
    msp.add_lwpolyline(rect_points(x, y, w, h), close=True, dxfattribs={"layer": layer})


def draw_tile(
    msp: Modelspace, x: float, y: float, w: float, h: float, layer: str = "0", filled: bool = False
) -> None:
    """Tile outline, optionally with a solid fill for presentation drawings."""
    draw_rect(msp, x, y, w, h, layer=layer)
    if filled:
        add_hatch(msp, rect_points(x, y, w, h), layer=layer)


# ─── 2D geometry ─────────────────────────────────────────────────────────────


def rotate_point(p: Point, center: Point, degrees: float) -> Point:
    a = math.radians(degrees)
    dx, dy = p[0] - center[0], p[1] - center[1]
    return (
        center[0] + dx * math.cos(a) - dy * math.sin(a),
        center[1] + dx * math.sin(a) + dy * math.cos(a),
    )


def offset_polyline(
    points: Sequence[Point], half_width: float, widths: Sequence[float] | None = None
) -> tuple[list[Point], list[Point]]:
    """Left and right edges of a band of ``2 * half_width`` around an open polyline.

    ``widths`` optionally scales the half width per vertex (used for streams).
    """
    left: list[Point] = []
    right: list[Point] = []
    n = len(points)
    for i, (px, py) in enumerate(points):
        ax, ay = points[max(i - 1, 0)]
        bx, by = points[min(i + 1, n - 1)]
        dx, dy = bx - ax, by - ay
        length = math.hypot(dx, dy)
        if length < 1e-6:
            continue
        nx, ny = -dy / length, dx / length
        hw = half_width * (widths[i] if widths else 1.0)
        left.append((px + nx * hw, py + ny * hw))
        right.append((px - nx * hw, py - ny * hw))
    return left, right


def polygon_area(points: Sequence[Point]) -> float:
    return 0.5 * sum(
        x1 * y2 - x2 * y1
        for (x1, y1), (x2, y2) in zip(points, [*points[1:], points[0]], strict=True)
    )


def polygon_centroid(points: Sequence[Point]) -> Point:
    """Area centroid; falls back to the vertex average for degenerate polygons."""
    area = polygon_area(points)
    if abs(area) < 1e-9:
        return (sum(p[0] for p in points) / len(points), sum(p[1] for p in points) / len(points))
    cx = cy = 0.0
    for (x1, y1), (x2, y2) in zip(points, [*points[1:], points[0]], strict=True):
        cross = x1 * y2 - x2 * y1
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    return (cx / (6 * area), cy / (6 * area))


def point_in_polygon(p: Point, polygon: Sequence[Point]) -> bool:
    x, y = p
    inside = False
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def clip_segment(p1: Point, p2: Point, polygon: Sequence[Point]) -> list[tuple[Point, Point]]:
    """Parts of segment p1-p2 that lie inside ``polygon`` (any simple polygon, convex or not)."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    ts = [0.0, 1.0]
    n = len(polygon)
    for i in range(n):
        (ax, ay), (bx, by) = polygon[i], polygon[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        denom = dx * ey - dy * ex
        if abs(denom) < 1e-12:
            continue
        t = ((ax - p1[0]) * ey - (ay - p1[1]) * ex) / denom
        u = ((ax - p1[0]) * dy - (ay - p1[1]) * dx) / denom
        if 0 <= t <= 1 and 0 <= u <= 1:
            ts.append(t)
    ts.sort()
    pieces = []
    for t0, t1 in itertools.pairwise(ts):
        if t1 - t0 < 1e-9:
            continue
        tm = (t0 + t1) / 2
        if point_in_polygon((p1[0] + dx * tm, p1[1] + dy * tm), polygon):
            pieces.append(((p1[0] + dx * t0, p1[1] + dy * t0), (p1[0] + dx * t1, p1[1] + dy * t1)))
    return pieces


def smooth_closed(points: Sequence[Point], samples: int = 8) -> list[Point]:
    """Closed Catmull-Rom curve through ``points``: turns a rough outline into an organic one."""
    n = len(points)
    if n < 3:
        return list(points)
    out = []
    for i in range(n):
        p0, p1, p2, p3 = (points[(i + k) % n] for k in (-1, 0, 1, 2))
        for s in range(samples):
            t = s / samples
            t2, t3 = t * t, t * t * t
            out.append(
                tuple(
                    0.5
                    * (
                        2 * p1[k]
                        + (-p0[k] + p2[k]) * t
                        + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2
                        + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3
                    )
                    for k in (0, 1)
                )
            )
    return out


def walk_polyline(points: Sequence[Point], spacing: float) -> list[tuple[Point, Point]]:
    """Stations every ``spacing`` mm along a polyline, as (position, unit direction) pairs.

    Distance carries over vertices, so spacing stays even around corners.
    """
    if spacing <= 0:
        raise ValueError("spacing must be positive")
    stations: list[tuple[Point, Point]] = []
    next_at = 0.0  # distance from the current segment start to the next station
    for (x1, y1), (x2, y2) in itertools.pairwise(points):
        seg = math.hypot(x2 - x1, y2 - y1)
        if seg < 1e-9:
            continue
        ux, uy = (x2 - x1) / seg, (y2 - y1) / seg
        while next_at <= seg + 1e-9:
            stations.append(((x1 + ux * next_at, y1 + uy * next_at), (ux, uy)))
            next_at += spacing
        next_at -= seg
    return stations
