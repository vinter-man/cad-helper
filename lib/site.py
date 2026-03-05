"""Site plan elements — plot boundary, house, fence, gates, compass rose, dimensions."""

import math
import ezdxf
from lib.core import add_layer, draw_rect


# ─── Plot boundary ───────────────────────────────────────────────────────────

def draw_plot(msp, doc, width: float, length: float):
    """Draw the plot boundary as a thick rectangle.

    Origin (0,0) is the south-west corner.
    X = east (width), Y = north (length).
    """
    add_layer(doc, "PLOT_BOUNDARY", color=7)

    msp.add_lwpolyline(
        [(0, 0), (width, 0), (width, length), (0, length)],
        close=True,
        dxfattribs={"layer": "PLOT_BOUNDARY", "const_width": 40},
    )

    # Plot dimensions
    add_layer(doc, "DIMENSIONS", color=8)
    _add_dim_text(msp, width / 2, -600, f"{width / 1000:.0f} m", layer="DIMENSIONS")
    _add_dim_text(msp, -600, length / 2, f"{length / 1000:.0f} m", rotation=90, layer="DIMENSIONS")


# ─── House ───────────────────────────────────────────────────────────────────

def draw_house(msp, doc, x: float, y: float, w: float, h: float,
               label: str = "HOUSE", entrance_side: str = "south",
               entrance_width: float = 1200):
    """Draw house footprint with entrance marker.

    Args:
        x, y: Bottom-left corner position (mm).
        w: Width (X direction) in mm.
        h: Height (Y direction) in mm.
        entrance_side: Which side has the main entrance.
        entrance_width: Entrance door width in mm.
    """
    add_layer(doc, "HOUSE", color=30)
    add_layer(doc, "HOUSE_FILL", color=8)

    # Solid outline
    msp.add_lwpolyline(
        [(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
        close=True,
        dxfattribs={"layer": "HOUSE", "const_width": 30},
    )

    # Hatch fill
    hatch = msp.add_hatch(color=8, dxfattribs={"layer": "HOUSE_FILL"})
    hatch.paths.add_polyline_path(
        [(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
        is_closed=True,
    )
    hatch.set_pattern_fill("ANSI31", scale=50)

    # Label
    _add_dim_text(msp, x + w / 2, y + h / 2, label, height=300, layer="HOUSE")
    _add_dim_text(msp, x + w / 2, y + h / 2 - 400,
                  f"{w / 1000:.0f}x{h / 1000:.0f} m", height=200, layer="HOUSE")

    # Entrance marker
    _draw_entrance(msp, x, y, w, h, entrance_side, entrance_width, layer="HOUSE")


def _draw_entrance(msp, x, y, w, h, side, ew, layer):
    """Draw entrance marker (arc + line) on the specified side."""
    if side == "south":
        cx = x + w / 2
        cy = y
        # Door swing arc
        msp.add_arc(
            center=(cx, cy), radius=ew / 2,
            start_angle=180, end_angle=360,
            dxfattribs={"layer": layer},
        )
        # Entry lines
        msp.add_line((cx - ew / 2, cy), (cx - ew / 2, cy - 300),
                     dxfattribs={"layer": layer})
        msp.add_line((cx + ew / 2, cy), (cx + ew / 2, cy - 300),
                     dxfattribs={"layer": layer})
    elif side == "north":
        cx = x + w / 2
        cy = y + h
        msp.add_arc(center=(cx, cy), radius=ew / 2,
                     start_angle=0, end_angle=180,
                     dxfattribs={"layer": layer})


# ─── Fence ───────────────────────────────────────────────────────────────────

def draw_fence(msp, doc, width: float, length: float,
               gates: list[dict] | None = None):
    """Draw fence around the plot perimeter with gate openings.

    Args:
        width: Plot width (X) in mm.
        length: Plot length (Y) in mm.
        gates: List of gate definitions, each with:
            - side: "south", "north", "east", "west"
            - center: position along the side in mm (from side start)
            - opening: gate width in mm
            - label: optional text label
    """
    add_layer(doc, "FENCE", color=3)
    add_layer(doc, "GATES", color=1)

    if gates is None:
        gates = []

    # Group gates by side
    sides = {
        "south": {"start": (0, 0), "end": (width, 0), "gates": []},
        "east":  {"start": (width, 0), "end": (width, length), "gates": []},
        "north": {"start": (width, length), "end": (0, length), "gates": []},
        "west":  {"start": (0, length), "end": (0, 0), "gates": []},
    }
    for g in gates:
        sides[g["side"]]["gates"].append(g)

    for side_name, side in sides.items():
        sx, sy = side["start"]
        ex, ey = side["end"]
        side_gates = sorted(side["gates"], key=lambda g: g["center"])

        if not side_gates:
            # No gates — draw full line
            msp.add_line((sx, sy), (ex, ey),
                        dxfattribs={"layer": "FENCE", "lineweight": 50})
        else:
            # Draw fence segments between gates
            if side_name in ("south", "north"):
                # Horizontal side
                is_reversed = ex < sx
                positions = sorted(
                    [(sx, ex)] if is_reversed else [(sx, ex)],
                    key=lambda p: p[0],
                )
                # Build fence segments
                segments = _build_fence_segments(
                    sx, ex, sy, side_gates, horizontal=True
                )
                for seg_start, seg_end in segments:
                    msp.add_line(seg_start, seg_end,
                                dxfattribs={"layer": "FENCE", "lineweight": 50})

                # Draw gate symbols
                for g in side_gates:
                    _draw_gate_symbol(msp, g, sy, horizontal=True)
            else:
                # Vertical side
                segments = _build_fence_segments(
                    sy, ey, sx, side_gates, horizontal=False
                )
                for seg_start, seg_end in segments:
                    msp.add_line(seg_start, seg_end,
                                dxfattribs={"layer": "FENCE", "lineweight": 50})

                for g in side_gates:
                    _draw_gate_symbol(msp, g, sx, horizontal=False)


def _build_fence_segments(start, end, fixed_coord, gates, horizontal):
    """Build fence line segments with gaps for gates."""
    segments = []
    direction = 1 if end > start else -1
    current = start

    # Sort gates by position
    sorted_gates = sorted(gates, key=lambda g: g["center"])

    for g in sorted_gates:
        gap_start = g["center"] - g["opening"] / 2
        gap_end = g["center"] + g["opening"] / 2

        if horizontal:
            if abs(current - gap_start) > 10:  # avoid zero-length segments
                segments.append(((current, fixed_coord), (gap_start, fixed_coord)))
            current = gap_end
        else:
            if abs(current - gap_start) > 10:
                segments.append(((fixed_coord, current), (fixed_coord, gap_start)))
            current = gap_end

    # Last segment to end
    if horizontal:
        if abs(current - end) > 10:
            segments.append(((current, fixed_coord), (end, fixed_coord)))
    else:
        if abs(current - end) > 10:
            segments.append(((fixed_coord, current), (fixed_coord, end)))

    return segments


def _draw_gate_symbol(msp, gate, fixed_coord, horizontal):
    """Draw gate opening symbol (two short perpendicular lines + arc)."""
    c = gate["center"]
    o = gate["opening"]
    half = o / 2

    if horizontal:
        p1 = (c - half, fixed_coord)
        p2 = (c + half, fixed_coord)
        # Gate pillars
        msp.add_line((c - half, fixed_coord - 150), (c - half, fixed_coord + 150),
                     dxfattribs={"layer": "GATES", "lineweight": 50})
        msp.add_line((c + half, fixed_coord - 150), (c + half, fixed_coord + 150),
                     dxfattribs={"layer": "GATES", "lineweight": 50})
        # Swing arc
        msp.add_arc(
            center=p1, radius=o,
            start_angle=270, end_angle=360,
            dxfattribs={"layer": "GATES"},
        )
    else:
        p1 = (fixed_coord, c - half)
        p2 = (fixed_coord, c + half)
        msp.add_line((fixed_coord - 150, c - half), (fixed_coord + 150, c - half),
                     dxfattribs={"layer": "GATES", "lineweight": 50})
        msp.add_line((fixed_coord - 150, c + half), (fixed_coord + 150, c + half),
                     dxfattribs={"layer": "GATES", "lineweight": 50})
        msp.add_arc(
            center=p1, radius=o,
            start_angle=0, end_angle=90,
            dxfattribs={"layer": "GATES"},
        )

    # Gate label
    label = gate.get("label", "")
    if label:
        if horizontal:
            _add_dim_text(msp, c, fixed_coord - 500, label, height=200, layer="GATES")
        else:
            _add_dim_text(msp, fixed_coord - 500, c, label, height=200, layer="GATES")


# ─── Compass Rose ────────────────────────────────────────────────────────────

def draw_compass(msp, doc, x: float, y: float, size: float = 1500):
    """Draw a north arrow / compass indicator."""
    add_layer(doc, "COMPASS", color=7)

    # Arrow pointing up (north)
    arrow_len = size
    arrow_w = size * 0.3

    # Filled triangle
    points = [
        (x, y + arrow_len),         # tip (north)
        (x - arrow_w / 2, y),       # bottom left
        (x + arrow_w / 2, y),       # bottom right
    ]
    msp.add_lwpolyline(points, close=True, dxfattribs={"layer": "COMPASS"})

    hatch = msp.add_hatch(dxfattribs={"layer": "COMPASS"})
    hatch.paths.add_polyline_path(points, is_closed=True)

    # "N" label
    msp.add_text("N", height=size * 0.3, dxfattribs={
        "layer": "COMPASS",
        "insert": (x - size * 0.1, y + arrow_len + 200),
    })


# ─── Dimension lines ────────────────────────────────────────────────────────

def draw_distance(msp, doc, p1: tuple, p2: tuple, offset: float = 500,
                  layer: str = "DIMENSIONS"):
    """Draw a simple dimension line between two points."""
    add_layer(doc, layer, color=8)

    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)

    # Perpendicular offset direction
    if abs(dx) > abs(dy):
        # Mostly horizontal
        oy = offset
        msp.add_line((x1, y1 + oy), (x2, y2 + oy), dxfattribs={"layer": layer})
        msp.add_line((x1, y1), (x1, y1 + oy + 100), dxfattribs={"layer": layer})
        msp.add_line((x2, y2), (x2, y2 + oy + 100), dxfattribs={"layer": layer})
        _add_dim_text(msp, (x1 + x2) / 2, y1 + oy + 100,
                      f"{length / 1000:.1f} m", height=200, layer=layer)
    else:
        # Mostly vertical
        ox = offset
        msp.add_line((x1 + ox, y1), (x2 + ox, y2), dxfattribs={"layer": layer})
        msp.add_line((x1, y1), (x1 + ox + 100, y1), dxfattribs={"layer": layer})
        msp.add_line((x2, y2), (x2 + ox + 100, y2), dxfattribs={"layer": layer})
        _add_dim_text(msp, x1 + ox + 100, (y1 + y2) / 2,
                      f"{length / 1000:.1f} m", height=200, rotation=90, layer=layer)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _add_dim_text(msp, x, y, text, height=200, rotation=0, layer="DIMENSIONS"):
    attribs = {"layer": layer, "insert": (x, y), "rotation": rotation}
    msp.add_text(text, height=height, dxfattribs=attribs)
