#!/usr/bin/env python3
"""Playground project — three elliptical islands connected by rubber bridges.

Run from repo root:
    python projects/playground/build.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from lib.core import create_document, save, add_layer, draw_rect
from lib.site import draw_compass
from lib.planting import draw_shrub
from lib.playground import (
    draw_sandbox, draw_slide, draw_climbing_frame,
    draw_rubber_bridge, draw_ellipse_zone, draw_sound_barrier,
    draw_ground_light, draw_trash_bin,
)
from lib.furniture import draw_bench

OUTPUT = Path(__file__).parent / "playground.dxf"

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

AREA_W = 8_000
AREA_H = 8_000

# Sound barrier takes up y=0..300 on the south side
BARRIER_THICKNESS = 300

# Three islands (centers and radii)
ISLAND_1 = {"cx": 2_500, "cy": 3_500, "rx": 1_400, "ry": 1_100, "name": "SANDBOX ISLAND"}
ISLAND_2 = {"cx": 5_800, "cy": 3_200, "rx": 1_300, "ry": 1_000, "name": "SLIDES ISLAND"}
ISLAND_3 = {"cx": 3_800, "cy": 6_000, "rx": 1_200, "ry": 1_200, "name": "CLIMBING ISLAND"}

# Gates
GATE_W_CENTER = 4_500   # west gate, y position
GATE_E_CENTER = 4_500   # east gate, y position
GATE_WIDTH = 1_200


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def build():
    doc = create_document()
    msp = doc.modelspace()

    # ── Phase 1: Boundaries & ground ─────────────────────────────────────

    # Boundary
    add_layer(doc, "BOUNDARY", color=7)
    msp.add_lwpolyline(
        [(0, BARRIER_THICKNESS), (AREA_W, BARRIER_THICKNESS),
         (AREA_W, AREA_H), (0, AREA_H)],
        close=True,
        dxfattribs={"layer": "BOUNDARY", "const_width": 25},
    )

    # Gravel surface (full area)
    add_layer(doc, "GRAVEL", color=253)
    hatch = msp.add_hatch(color=253, dxfattribs={"layer": "GRAVEL"})
    hatch.paths.add_polyline_path(
        [(0, BARRIER_THICKNESS), (AREA_W, BARRIER_THICKNESS),
         (AREA_W, AREA_H), (0, AREA_H)],
        is_closed=True,
    )
    hatch.set_pattern_fill("AR-SAND", scale=15)

    # Sound barrier (south)
    draw_sound_barrier(msp, doc,
                       start=(0, BARRIER_THICKNESS / 2),
                       end=(AREA_W, BARRIER_THICKNESS / 2),
                       thickness=BARRIER_THICKNESS)

    # Fence (north, west, east) with gate gaps
    add_layer(doc, "FENCE", color=8)
    add_layer(doc, "GATES", color=1)

    # North fence
    msp.add_line((0, AREA_H), (AREA_W, AREA_H),
                 dxfattribs={"layer": "FENCE", "lineweight": 30})

    # West fence with gate
    gate_w_bottom = GATE_W_CENTER - GATE_WIDTH / 2
    gate_w_top = GATE_W_CENTER + GATE_WIDTH / 2
    msp.add_line((0, BARRIER_THICKNESS), (0, gate_w_bottom),
                 dxfattribs={"layer": "FENCE", "lineweight": 30})
    msp.add_line((0, gate_w_top), (0, AREA_H),
                 dxfattribs={"layer": "FENCE", "lineweight": 30})
    # Gate pillars
    msp.add_line((-100, gate_w_bottom), (100, gate_w_bottom),
                 dxfattribs={"layer": "GATES", "lineweight": 50})
    msp.add_line((-100, gate_w_top), (100, gate_w_top),
                 dxfattribs={"layer": "GATES", "lineweight": 50})
    # Gate arc
    msp.add_arc(center=(0, gate_w_bottom), radius=GATE_WIDTH,
                start_angle=0, end_angle=90,
                dxfattribs={"layer": "GATES"})

    # East fence with gate
    gate_e_bottom = GATE_E_CENTER - GATE_WIDTH / 2
    gate_e_top = GATE_E_CENTER + GATE_WIDTH / 2
    msp.add_line((AREA_W, BARRIER_THICKNESS), (AREA_W, gate_e_bottom),
                 dxfattribs={"layer": "FENCE", "lineweight": 30})
    msp.add_line((AREA_W, gate_e_top), (AREA_W, AREA_H),
                 dxfattribs={"layer": "FENCE", "lineweight": 30})
    msp.add_line((AREA_W - 100, gate_e_bottom), (AREA_W + 100, gate_e_bottom),
                 dxfattribs={"layer": "GATES", "lineweight": 50})
    msp.add_line((AREA_W - 100, gate_e_top), (AREA_W + 100, gate_e_top),
                 dxfattribs={"layer": "GATES", "lineweight": 50})
    msp.add_arc(center=(AREA_W, gate_e_bottom), radius=GATE_WIDTH,
                start_angle=90, end_angle=180,
                dxfattribs={"layer": "GATES"})

    # Compass
    draw_compass(msp, doc, x=-1_500, y=AREA_H - 500)

    # ── Phase 2: Islands ─────────────────────────────────────────────────

    # Island 1 — Sandbox (warm yellow)
    draw_ellipse_zone(msp, doc, **ISLAND_1, color=2,
                      hatch_pattern="DOTS", hatch_scale=20,
                      layer="ISLAND_SANDBOX")

    # Island 2 — Slides (warm red)
    draw_ellipse_zone(msp, doc, **ISLAND_2, color=1,
                      hatch_pattern="DOTS", hatch_scale=20,
                      layer="ISLAND_SLIDES")

    # Island 3 — Climbing (cool blue)
    draw_ellipse_zone(msp, doc, **ISLAND_3, color=4,
                      hatch_pattern="DOTS", hatch_scale=20,
                      layer="ISLAND_CLIMBING")

    # ── Phase 3: Equipment ───────────────────────────────────────────────

    # Sandbox inside island 1
    draw_sandbox(msp, doc, cx=ISLAND_1["cx"], cy=ISLAND_1["cy"],
                 rx=1_000, ry=800)

    # Slides inside island 2
    draw_slide(msp, doc, cx=5_500, cy=3_500,
               length=2_000, width=600, rotation=-10)
    draw_slide(msp, doc, cx=6_200, cy=2_800,
               length=1_500, width=500, rotation=20)

    # Climbing dome inside island 3
    draw_climbing_frame(msp, doc, cx=ISLAND_3["cx"], cy=ISLAND_3["cy"],
                        w=1_800, h=1_800, frame_type="dome")

    # ── Phase 4: Bridges ─────────────────────────────────────────────────

    # Calculate edge points of ellipses for bridge connections
    # Bridge 1→2 (sandbox to slides)
    b12_start = _ellipse_edge(ISLAND_1, math.atan2(
        ISLAND_2["cy"] - ISLAND_1["cy"], ISLAND_2["cx"] - ISLAND_1["cx"]))
    b12_end = _ellipse_edge(ISLAND_2, math.atan2(
        ISLAND_1["cy"] - ISLAND_2["cy"], ISLAND_1["cx"] - ISLAND_2["cx"]))
    draw_rubber_bridge(msp, doc, start=b12_start, end=b12_end, width=700)

    # Bridge 1→3 (sandbox to climbing)
    b13_start = _ellipse_edge(ISLAND_1, math.atan2(
        ISLAND_3["cy"] - ISLAND_1["cy"], ISLAND_3["cx"] - ISLAND_1["cx"]))
    b13_end = _ellipse_edge(ISLAND_3, math.atan2(
        ISLAND_1["cy"] - ISLAND_3["cy"], ISLAND_1["cx"] - ISLAND_3["cx"]))
    draw_rubber_bridge(msp, doc, start=b13_start, end=b13_end, width=700)

    # Bridge 2→3 (slides to climbing)
    b23_start = _ellipse_edge(ISLAND_2, math.atan2(
        ISLAND_3["cy"] - ISLAND_2["cy"], ISLAND_3["cx"] - ISLAND_2["cx"]))
    b23_end = _ellipse_edge(ISLAND_3, math.atan2(
        ISLAND_2["cy"] - ISLAND_3["cy"], ISLAND_2["cx"] - ISLAND_3["cx"]))
    draw_rubber_bridge(msp, doc, start=b23_start, end=b23_end, width=700)

    # ── Phase 5: Furniture ───────────────────────────────────────────────

    # Benches — 4 around perimeter
    # NW bench
    draw_bench(msp, doc, x=500, y=7_000, w=1_800, h=500, layer="BENCHES", color=33)
    # NE bench
    draw_bench(msp, doc, x=5_700, y=7_000, w=1_800, h=500, layer="BENCHES", color=33)
    # W bench
    draw_bench(msp, doc, x=500, y=4_800, w=1_800, h=500, layer="BENCHES", color=33)
    # E bench
    draw_bench(msp, doc, x=5_700, y=4_800, w=1_800, h=500, layer="BENCHES", color=33)

    # Shrubs behind benches (for parents' comfort)
    shrub_positions = [
        (500 + 900, 7_700),     # behind NW bench
        (5_700 + 900, 7_700),   # behind NE bench
        (200, 5_050),           # behind W bench (left side)
        (7_800, 5_050),         # behind E bench (right side)
    ]
    for sx, sy in shrub_positions:
        draw_shrub(msp, doc, cx=sx, cy=sy, diameter=1_000,
                   layer="SHRUBS", color=3)

    # Extra shrubs at corners for coziness
    corner_shrubs = [
        (600, 7_600),
        (1_800, 7_600),
        (6_200, 7_600),
        (7_400, 7_600),
    ]
    for sx, sy in corner_shrubs:
        draw_shrub(msp, doc, cx=sx, cy=sy, diameter=700,
                   layer="SHRUBS", color=83)

    # Trash bins
    draw_trash_bin(msp, doc, cx=300, cy=3_800)
    draw_trash_bin(msp, doc, cx=7_700, cy=3_800)

    # ── Phase 6: Lighting ────────────────────────────────────────────────

    # Ground lights around perimeter
    light_positions = [
        (500, 1_000),       # SW
        (7_500, 1_000),     # SE
        (500, 4_000),       # W
        (7_500, 4_000),     # E
        (500, 6_500),       # NW lower
        (7_500, 6_500),     # NE lower
        (2_500, 7_800),     # N left
        (5_500, 7_800),     # N right
    ]
    for lx, ly in light_positions:
        draw_ground_light(msp, doc, cx=lx, cy=ly)

    # ── Save ─────────────────────────────────────────────────────────────
    path = save(doc, OUTPUT)
    print(f"Built: {path}")

    entities = list(msp)
    layers = [l.dxf.name for l in doc.layers if l.dxf.name not in ('0', 'Defpoints')]
    print(f"  {len(entities)} entities across {len(layers)} layers")

    return path


def _ellipse_edge(island: dict, angle: float) -> tuple[float, float]:
    """Get the point on the ellipse edge at the given angle."""
    rx = island["rx"]
    ry = island["ry"]
    # Parametric ellipse point
    x = rx * math.cos(angle)
    y = ry * math.sin(angle)
    return (island["cx"] + x, island["cy"] + y)


if __name__ == "__main__":
    build()
