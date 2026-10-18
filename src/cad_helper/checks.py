"""Automatic drawing checks run after every build.

They cover what can be measured instead of eyeballed: DXF validity, elements
outside the site, stray entities on layer 0, unreadable text, and minimum
clearances between layers (e.g. pond vs house foundation).
"""

from __future__ import annotations

import fnmatch
import itertools
import math
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cached_property

from ezdxf import bbox, path
from ezdxf.document import Drawing
from ezdxf.entities import DXFGraphic

from cad_helper.core import Point, point_in_polygon

# Layers allowed past the site edge: annotation, north arrow, and the boundary and
# fence lines themselves (their drawn line width straddles the edge).
EXEMPT_LAYERS = ("DIMENSIONS", "COMPASS", "LABELS", "GATES", "PLOT_BOUNDARY", "FENCE")
TEXT_TYPES = ("TEXT", "MTEXT", "DIMENSION")


@dataclass(frozen=True)
class Issue:
    level: str  # "error" or "warning"
    check: str
    message: str

    def __str__(self) -> str:
        return f"[{self.level}] {self.check}: {self.message}"


@dataclass(frozen=True)
class Clearance:
    """Entities on ``a`` must stay at least ``min_mm`` away from entities on ``b``.

    Layer names accept shell wildcards, e.g. ``"STEPPING_STONES*"``.
    """

    a: str
    b: str
    min_mm: float
    reason: str = ""


def check_document(
    doc: Drawing,
    *,
    bounds: tuple[float, float, float, float] | None = None,
    clearances: Sequence[Clearance] = (),
    plot_scale: int = 100,
    min_paper_text_mm: float = 1.5,
    tolerance: float = 25.0,
) -> list[Issue]:
    """Run every check and return the issues found (empty list = clean drawing).

    ``tolerance`` absorbs drawn line widths at the site edge. ``plot_scale`` is the
    intended print scale (100 means 1:100); text smaller than
    ``min_paper_text_mm`` on paper at that scale is reported as unreadable.
    """
    msp = doc.modelspace()
    issues: list[Issue] = []

    auditor = doc.audit()
    issues += [Issue("error", "audit", e.message) for e in auditor.errors]
    issues += [Issue("warning", "audit", f"auto-fixed: {f.message}") for f in auditor.fixes]

    on_zero = sum(1 for e in msp if e.dxf.layer == "0")
    if on_zero:
        issues.append(
            Issue(
                "warning",
                "layers",
                f"{on_zero} entities on layer 0; put every element on a named layer",
            )
        )

    used = {e.dxf.layer for e in msp}
    empty = sorted(
        layer.dxf.name
        for layer in doc.layers
        if layer.dxf.name not in used and layer.dxf.name not in ("0", "Defpoints")
    )
    if empty:
        issues.append(Issue("warning", "layers", f"empty layers: {', '.join(empty)}"))

    min_height = min_paper_text_mm * plot_scale
    small = sorted({e.dxf.text for e in msp.query("TEXT") if e.dxf.height < min_height})
    if small:
        issues.append(
            Issue(
                "warning",
                "text",
                f"{len(small)} labels smaller than {min_paper_text_mm} mm at 1:{plot_scale} "
                f"({min_height:g} mm in model): {', '.join(small[:6])}{' ...' if len(small) > 6 else ''}",
            )
        )

    if bounds is not None:
        issues += _check_bounds(msp, bounds, tolerance)
    for c in clearances:
        issues += _check_clearance(msp, c)
    return issues


def _check_bounds(msp, bounds: tuple[float, float, float, float], tolerance: float) -> list[Issue]:
    x0, y0, x1, y1 = bounds
    outside: dict[str, list[str]] = {}
    for e in msp:
        if e.dxftype() in TEXT_TYPES or e.dxf.layer in EXEMPT_LAYERS:
            continue
        box = bbox.extents([e], fast=True)
        if not box.has_data:
            continue
        if (
            box.extmin.x < x0 - tolerance
            or box.extmin.y < y0 - tolerance
            or box.extmax.x > x1 + tolerance
            or box.extmax.y > y1 + tolerance
        ):
            outside.setdefault(e.dxf.layer, []).append(
                f"({box.extmin.x:.0f},{box.extmin.y:.0f})-({box.extmax.x:.0f},{box.extmax.y:.0f})"
            )
    return [
        Issue(
            "error",
            "bounds",
            f"{len(spans)} entities on {layer} leave the site {bounds}: {spans[0]}",
        )
        for layer, spans in sorted(outside.items())
    ]


@dataclass(frozen=True)
class Shape:
    points: list[Point]
    closed: bool

    @cached_property
    def box(self) -> tuple[float, float, float, float]:
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        return min(xs), min(ys), max(xs), max(ys)

    def box_gap(self, other: Shape) -> float:
        """Distance between the two bounding boxes (0 if they overlap): a lower bound."""
        ax0, ay0, ax1, ay1 = self.box
        bx0, by0, bx1, by1 = other.box
        return math.hypot(max(bx0 - ax1, ax0 - bx1, 0), max(by0 - ay1, ay0 - by1, 0))

    def segments(self) -> list[tuple[Point, Point]]:
        pts = self.points
        segs = list(itertools.pairwise(pts))
        if self.closed and len(pts) > 2:
            segs.append((pts[-1], pts[0]))
        return segs


def layer_shapes(msp, pattern: str) -> list[Shape]:
    """Every entity on layers matching ``pattern``, flattened to 2D outlines."""
    shapes = []
    for e in msp:
        if e.dxftype() in TEXT_TYPES or not fnmatch.fnmatchcase(e.dxf.layer, pattern):
            continue
        shapes += _flatten(e)
    return shapes


def _flatten(e: DXFGraphic) -> list[Shape]:
    try:
        paths = path.from_hatch(e) if e.dxftype() == "HATCH" else [path.make_path(e)]
    except TypeError:  # entity type without a geometric path
        return []
    shapes = []
    for p in paths:
        pts = [(v.x, v.y) for v in p.flattening(distance=20)]
        if len(pts) < 2:
            continue
        closed = p.is_closed or e.dxftype() in ("HATCH", "CIRCLE")
        shapes.append(Shape(pts, closed))
    return shapes


def clearance(a: Shape, b: Shape) -> float:
    """Smallest distance between two outlines; 0 if they touch, cross or one contains the other."""
    if a.closed and len(a.points) > 2 and point_in_polygon(b.points[0], a.points):
        return 0.0
    if b.closed and len(b.points) > 2 and point_in_polygon(a.points[0], b.points):
        return 0.0
    best = math.inf
    segs_b = b.segments()
    for p, q in a.segments():
        for r, s in segs_b:
            best = min(best, _segment_distance(p, q, r, s))
            if best == 0:
                return 0.0
    return best


def _check_clearance(msp, c: Clearance) -> list[Issue]:
    a_shapes, b_shapes = layer_shapes(msp, c.a), layer_shapes(msp, c.b)
    if not a_shapes or not b_shapes:
        missing = c.a if not a_shapes else c.b
        return [
            Issue("warning", "clearance", f"no geometry on {missing}; rule {c.a} <-> {c.b} skipped")
        ]
    # Only pairs whose bounding boxes are closer than the limit can violate it.
    worst = min(
        (clearance(a, b) for a in a_shapes for b in b_shapes if a.box_gap(b) < c.min_mm),
        default=math.inf,
    )
    if worst < c.min_mm:
        why = f" ({c.reason})" if c.reason else ""
        return [
            Issue(
                "error",
                "clearance",
                f"{c.a} <-> {c.b} is {worst:.0f} mm, needs >= {c.min_mm:.0f} mm{why}",
            )
        ]
    return []


def _segment_distance(p: Point, q: Point, r: Point, s: Point) -> float:
    if _segments_cross(p, q, r, s):
        return 0.0
    return min(
        _point_segment(p, r, s),
        _point_segment(q, r, s),
        _point_segment(r, p, q),
        _point_segment(s, p, q),
    )


def _point_segment(p: Point, a: Point, b: Point) -> float:
    dx, dy = b[0] - a[0], b[1] - a[1]
    length2 = dx * dx + dy * dy
    t = (
        0.0
        if length2 == 0
        else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / length2))
    )
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def _segments_cross(p: Point, q: Point, r: Point, s: Point) -> bool:
    def orient(a: Point, b: Point, c: Point) -> float:
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    d1, d2 = orient(r, s, p), orient(r, s, q)
    d3, d4 = orient(p, q, r), orient(p, q, s)
    return (d1 > 0) != (d2 > 0) and (d3 > 0) != (d4 > 0)
