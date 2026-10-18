#!/usr/bin/env python3
"""Playground between apartment blocks, Sofia: three islands joined by rubber bridges.

Build: uv run cad-helper build playground
"""

import math

from cad_helper.checks import Clearance
from cad_helper.core import add_hatch, add_layer, create_document
from cad_helper.furniture import draw_bench
from cad_helper.planting import draw_shrub
from cad_helper.playground import (
    draw_climbing_frame,
    draw_ellipse_zone,
    draw_ground_light,
    draw_rubber_bridge,
    draw_sandbox,
    draw_slide,
    draw_sound_barrier,
    draw_trash_bin,
)
from cad_helper.site import draw_compass, draw_fence

# ─── Configuration (mm) ──────────────────────────────────────────────────────

AREA_W = 8_000
AREA_H = 8_000

# Sound barrier takes up y=0..300 on the south side
BARRIER_THICKNESS = 300

# Three islands (centers and radii)
ISLAND_1 = {"cx": 2_500, "cy": 3_500, "rx": 1_400, "ry": 1_100, "name": "SANDBOX ISLAND"}
ISLAND_2 = {"cx": 5_800, "cy": 3_200, "rx": 1_300, "ry": 1_000, "name": "SLIDES ISLAND"}
ISLAND_3 = {"cx": 3_800, "cy": 6_000, "rx": 1_200, "ry": 1_200, "name": "CLIMBING ISLAND"}

# Gates: one in the west fence, one in the east fence. Each leaf is hinged at the
# south post and swings 1200 mm into the playground, so nothing stands in the
# quarter circle north of y = GATE_CENTER - GATE_WIDTH / 2.
GATE_CENTER = 4_500  # y position, both gates
GATE_WIDTH = 1_200

# Slides (cx, cy, length, width, rotation): side by side on island 2, both running
# south, fully on the rubber and clear of the bridges and of each other's labels.
SLIDES = [
    (5_300, 3_100, 1_200, 600, -90),
    (6_400, 3_150, 1_200, 500, -90),
]

# Benches for parents (x, y, length): two along the north fence, one by each gate.
BENCHES = [
    (500, 6_500, 1_800),
    (5_700, 6_500, 1_800),
    (700, 5_000, 1_500),
    (5_300, 4_800, 1_500),
]

# Shrubs (cx, cy, diameter, colour) screen the bench backs; all stay inside the
# fence and outside the gate swings.
SHRUBS = [
    (1_400, 7_480, 900, 3),
    (6_600, 7_480, 900, 3),
    (350, 5_550, 600, 3),
    (7_550, 5_550, 700, 3),
    (600, 7_600, 700, 83),
    (1_800, 7_600, 700, 83),
    (6_200, 7_600, 700, 83),
    (7_400, 7_600, 700, 83),
]

# Bins and ground lights sit south of the gate leaves.
BINS = [(300, 3_500), (7_700, 3_500)]
LIGHTS = [
    (500, 1_000),
    (7_500, 1_000),
    (300, 2_800),
    (7_700, 2_800),
    (300, 6_200),
    (7_700, 6_200),
    (2_900, 7_800),
    (5_300, 7_800),
]

PLOT_SCALE = 50  # small site, printed at 1:50
BOUNDS = (0, 0, AREA_W, AREA_H)
CLEARANCES = [
    Clearance("SLIDES", "SOUND_BARRIER", 1_000, "run-out clear of the road-side wall"),
    Clearance("CLIMBING", "FENCE", 1_000, "fall zone inside the fence"),
    Clearance("BENCHES", "ISLAND_*", 300, "parents sit off the play surface"),
    Clearance("SLIDES", "BRIDGES", 100, "bridges land on the rubber, not on a slide"),
    Clearance("GATES", "SHRUBS", 100, "gate leaf swings clear of the shrubs"),
    Clearance("GATES", "FURNITURE", 100, "bins clear of the open gate leaf"),
]


def build():
    doc = create_document()
    msp = doc.modelspace()

    # ── Phase 1: Boundaries & ground ─────────────────────────────────────

    play_area = [
        (0, BARRIER_THICKNESS),
        (AREA_W, BARRIER_THICKNESS),
        (AREA_W, AREA_H),
        (0, AREA_H),
    ]
    add_layer(doc, "BOUNDARY", color=7)
    msp.add_lwpolyline(play_area, close=True, dxfattribs={"layer": "BOUNDARY", "const_width": 25})
    add_layer(doc, "GRAVEL", color=253)
    add_hatch(msp, play_area, layer="GRAVEL", color=253, pattern="AR-SAND", scale=15)

    # Sound barrier closes the south side; the fence runs round the other three.
    draw_sound_barrier(
        msp,
        doc,
        start=(0, BARRIER_THICKNESS / 2),
        end=(AREA_W, BARRIER_THICKNESS / 2),
        thickness=BARRIER_THICKNESS,
    )
    draw_fence(
        msp,
        doc,
        width=AREA_W,
        length=AREA_H,
        gates=[
            {"side": "west", "center": GATE_CENTER, "opening": GATE_WIDTH},
            {"side": "east", "center": GATE_CENTER, "opening": GATE_WIDTH},
        ],
        sides=("east", "north", "west"),
    )

    draw_compass(msp, doc, x=-1_200, y=AREA_H - 1_000, size=800)

    # ── Phase 2: Islands ─────────────────────────────────────────────────

    # Island 1 — Sandbox (warm yellow)
    draw_ellipse_zone(
        msp, doc, **ISLAND_1, color=2, hatch_pattern="DOTS", hatch_scale=45, layer="ISLAND_SANDBOX"
    )

    # Island 2 — Slides (warm red)
    draw_ellipse_zone(
        msp, doc, **ISLAND_2, color=1, hatch_pattern="DOTS", hatch_scale=45, layer="ISLAND_SLIDES"
    )

    # Island 3 — Climbing (cool blue)
    draw_ellipse_zone(
        msp, doc, **ISLAND_3, color=4, hatch_pattern="DOTS", hatch_scale=45, layer="ISLAND_CLIMBING"
    )

    # ── Phase 3: Equipment ───────────────────────────────────────────────

    draw_sandbox(msp, doc, cx=ISLAND_1["cx"], cy=ISLAND_1["cy"], rx=1_000, ry=800)
    for cx, cy, length, width, rotation in SLIDES:
        draw_slide(msp, doc, cx=cx, cy=cy, length=length, width=width, rotation=rotation)
    draw_climbing_frame(
        msp, doc, cx=ISLAND_3["cx"], cy=ISLAND_3["cy"], w=1_800, h=1_800, frame_type="dome"
    )

    # ── Phase 4: Bridges between facing island edges ─────────────────────

    for a, b in [(ISLAND_1, ISLAND_2), (ISLAND_1, ISLAND_3), (ISLAND_2, ISLAND_3)]:
        start = _ellipse_edge(a, math.atan2(b["cy"] - a["cy"], b["cx"] - a["cx"]))
        end = _ellipse_edge(b, math.atan2(a["cy"] - b["cy"], a["cx"] - b["cx"]))
        draw_rubber_bridge(msp, doc, start=start, end=end, width=700)

    # ── Phase 5: Furniture ───────────────────────────────────────────────

    for x, y, w in BENCHES:
        draw_bench(msp, doc, x=x, y=y, w=w, h=500, layer="BENCHES", color=33)
    for sx, sy, d, color in SHRUBS:
        draw_shrub(msp, doc, cx=sx, cy=sy, diameter=d, layer="SHRUBS", color=color)
    for bx, by in BINS:
        draw_trash_bin(msp, doc, cx=bx, cy=by)

    # ── Phase 6: Lighting ────────────────────────────────────────────────
    for lx, ly in LIGHTS:
        draw_ground_light(msp, doc, cx=lx, cy=ly)

    return doc


def _ellipse_edge(island: dict, angle: float) -> tuple[float, float]:
    """Point where a ray from the island centre at ``angle`` (radians) meets its edge."""
    c, s_ = math.cos(angle), math.sin(angle)
    r = 1 / math.sqrt((c / island["rx"]) ** 2 + (s_ / island["ry"]) ** 2)
    return (island["cx"] + r * c, island["cy"] + r * s_)
