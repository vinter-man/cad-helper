"""Playground equipment symbols — sandbox, slides, climbing frames, swings, seesaws.

All symbols are top-view representations for landscape plans.
"""

import math
from lib.core import add_layer


# ─── Sandbox ─────────────────────────────────────────────────────────────────

def draw_sandbox(msp, doc, cx: float, cy: float,
                 rx: float = 1500, ry: float = 1200,
                 layer: str = "SANDBOX", color: int = 2):
    """Draw a sandbox symbol — ellipse with inner dots (sand texture)."""
    add_layer(doc, layer, color=color)

    # Outer border (ellipse)
    msp.add_ellipse(
        center=(cx, cy), major_axis=(rx, 0), ratio=ry / rx,
        dxfattribs={"layer": layer},
    )

    # Sand fill
    add_layer(doc, f"{layer}_FILL", color=2)
    hatch = msp.add_hatch(color=2, dxfattribs={"layer": f"{layer}_FILL"})
    edge_path = hatch.paths.add_edge_path()
    edge_path.add_ellipse(
        center=(cx, cy), major_axis=(rx, 0), ratio=ry / rx,
        start_angle=0, end_angle=360,
    )
    hatch.set_pattern_fill("DOTS", scale=30)

    # Label
    msp.add_text("SANDBOX", height=120, dxfattribs={
        "layer": layer, "insert": (cx - 300, cy - 60),
    })


# ─── Slide ───────────────────────────────────────────────────────────────────

def draw_slide(msp, doc, cx: float, cy: float,
               length: float = 2500, width: float = 600,
               rotation: float = 0,
               layer: str = "SLIDES", color: int = 1):
    """Draw a slide symbol — rectangle with arrow showing slide direction.

    Arrow points in the direction kids slide down.
    """
    add_layer(doc, layer, color=color)
    half_l = length / 2
    half_w = width / 2
    rad = math.radians(rotation)

    def rot(x, y):
        return (cx + x * math.cos(rad) - y * math.sin(rad),
                cy + x * math.sin(rad) + y * math.cos(rad))

    # Slide body
    corners = [rot(-half_l, -half_w), rot(half_l, -half_w),
               rot(half_l, half_w), rot(-half_l, half_w)]
    msp.add_lwpolyline(corners, close=True,
                       dxfattribs={"layer": layer, "const_width": 10})

    # Arrow (slide direction)
    arrow_start = rot(-half_l * 0.3, 0)
    arrow_end = rot(half_l * 0.6, 0)
    msp.add_line(arrow_start, arrow_end, dxfattribs={"layer": layer})
    # Arrowhead
    ah1 = rot(half_l * 0.4, half_w * 0.3)
    ah2 = rot(half_l * 0.4, -half_w * 0.3)
    msp.add_line(arrow_end, ah1, dxfattribs={"layer": layer})
    msp.add_line(arrow_end, ah2, dxfattribs={"layer": layer})

    # Platform (start of slide — wider rectangle)
    platform = [rot(-half_l, -half_w * 1.3), rot(-half_l + width * 0.5, -half_w * 1.3),
                rot(-half_l + width * 0.5, half_w * 1.3), rot(-half_l, half_w * 1.3)]
    msp.add_lwpolyline(platform, close=True, dxfattribs={"layer": layer})

    msp.add_text("SLIDE", height=100, dxfattribs={
        "layer": layer, "insert": rot(-200, -half_w - 200),
    })


# ─── Climbing Frame ─────────────────────────────────────────────────────────

def draw_climbing_frame(msp, doc, cx: float, cy: float,
                        w: float = 2000, h: float = 2000,
                        frame_type: str = "net",
                        layer: str = "CLIMBING", color: int = 4):
    """Draw a climbing frame symbol.

    frame_type: "net" (grid pattern), "dome" (circle with radial lines)
    """
    add_layer(doc, layer, color=color)

    if frame_type == "dome":
        r = min(w, h) / 2
        # Outer circle
        msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})
        # Concentric rings
        for ring in [0.33, 0.66]:
            msp.add_circle((cx, cy), radius=r * ring, dxfattribs={"layer": layer})
        # Radial lines
        for angle_deg in range(0, 360, 30):
            angle = math.radians(angle_deg)
            msp.add_line(
                (cx, cy),
                (cx + r * math.cos(angle), cy + r * math.sin(angle)),
                dxfattribs={"layer": layer},
            )
        label = "CLIMBING DOME"
    else:
        # Net frame — rectangle with grid
        x = cx - w / 2
        y = cy - h / 2
        msp.add_lwpolyline(
            [(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
            close=True, dxfattribs={"layer": layer, "const_width": 10},
        )
        # Grid lines
        grid_spacing = 400
        gx = x + grid_spacing
        while gx < x + w:
            msp.add_line((gx, y), (gx, y + h), dxfattribs={"layer": layer})
            gx += grid_spacing
        gy = y + grid_spacing
        while gy < y + h:
            msp.add_line((x, gy), (x + w, gy), dxfattribs={"layer": layer})
            gy += grid_spacing
        label = "CLIMBING NET"

    msp.add_text(label, height=100, dxfattribs={
        "layer": layer, "insert": (cx - len(label) * 30, cy - min(w, h) / 2 - 250),
    })


# ─── Swing ───────────────────────────────────────────────────────────────────

def draw_swing(msp, doc, cx: float, cy: float,
               width: float = 2500, depth: float = 1200,
               num_seats: int = 2,
               layer: str = "SWINGS", color: int = 6):
    """Draw a swing set — top view (rectangle frame + seat arcs)."""
    add_layer(doc, layer, color=color)

    x = cx - width / 2
    y = cy - depth / 2

    # Frame rectangle
    msp.add_lwpolyline(
        [(x, y), (x + width, y), (x + width, y + depth), (x, y + depth)],
        close=True, dxfattribs={"layer": layer, "const_width": 10},
    )

    # Seat positions — arcs showing swing range
    seat_spacing = width / (num_seats + 1)
    for i in range(num_seats):
        seat_x = x + seat_spacing * (i + 1)
        # Swing arc
        msp.add_arc(
            center=(seat_x, cy), radius=depth * 0.4,
            start_angle=60, end_angle=120,
            dxfattribs={"layer": layer},
        )
        # Seat (small rectangle)
        sw = 200
        msp.add_lwpolyline(
            [(seat_x - sw, cy - sw / 2), (seat_x + sw, cy - sw / 2),
             (seat_x + sw, cy + sw / 2), (seat_x - sw, cy + sw / 2)],
            close=True, dxfattribs={"layer": layer},
        )

    msp.add_text("SWINGS", height=100, dxfattribs={
        "layer": layer, "insert": (cx - 200, y - 250),
    })


# ─── Seesaw ─────────────────────────────────────────────────────────────────

def draw_seesaw(msp, doc, cx: float, cy: float,
                length: float = 2500, rotation: float = 0,
                layer: str = "SEESAW", color: int = 6):
    """Draw a seesaw — top view (line with circles at ends, triangle at center)."""
    add_layer(doc, layer, color=color)
    half = length / 2
    rad = math.radians(rotation)

    def rot(x, y):
        return (cx + x * math.cos(rad) - y * math.sin(rad),
                cy + x * math.sin(rad) + y * math.cos(rad))

    # Beam
    msp.add_line(rot(-half, 0), rot(half, 0),
                 dxfattribs={"layer": layer, "lineweight": 30})

    # Seats at ends
    msp.add_circle(rot(-half, 0), radius=150, dxfattribs={"layer": layer})
    msp.add_circle(rot(half, 0), radius=150, dxfattribs={"layer": layer})

    # Pivot triangle at center
    t = 200
    msp.add_lwpolyline(
        [rot(0, -t), rot(t * 0.7, t * 0.5), rot(-t * 0.7, t * 0.5)],
        close=True, dxfattribs={"layer": layer},
    )


# ─── Rubber Bridge / Walkway ────────────────────────────────────────────────

def draw_rubber_bridge(msp, doc, start: tuple, end: tuple,
                       width: float = 800, plank_spacing: float = 150,
                       layer: str = "BRIDGES", color: int = 33):
    """Draw a rubber plank bridge between two points.

    Parallel lines with perpendicular plank lines.
    """
    add_layer(doc, layer, color=color)

    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    if length < 1:
        return

    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux
    half_w = width / 2

    # Side rails
    msp.add_lwpolyline(
        [(x1 + nx * half_w, y1 + ny * half_w),
         (x2 + nx * half_w, y2 + ny * half_w)],
        dxfattribs={"layer": layer, "const_width": 10})
    msp.add_lwpolyline(
        [(x1 - nx * half_w, y1 - ny * half_w),
         (x2 - nx * half_w, y2 - ny * half_w)],
        dxfattribs={"layer": layer, "const_width": 10})

    # Planks
    n_planks = int(length / plank_spacing)
    for i in range(n_planks + 1):
        t = i / max(n_planks, 1)
        px = x1 + dx * t
        py = y1 + dy * t
        msp.add_line(
            (px + nx * half_w, py + ny * half_w),
            (px - nx * half_w, py - ny * half_w),
            dxfattribs={"layer": layer},
        )


# ─── Elliptical Zone ────────────────────────────────────────────────────────

def draw_ellipse_zone(msp, doc, cx: float, cy: float,
                      rx: float, ry: float,
                      name: str = "", color: int = 3,
                      hatch_pattern: str = "DOTS", hatch_scale: float = 30,
                      layer: str | None = None):
    """Draw an elliptical zone with fill and label."""
    if layer is None:
        layer = f"ZONE_{name.upper().replace(' ', '_')}"
    fill_layer = f"{layer}_FILL"

    add_layer(doc, layer, color=color)
    add_layer(doc, fill_layer, color=color)

    # Outline
    msp.add_ellipse(
        center=(cx, cy), major_axis=(rx, 0), ratio=ry / rx,
        dxfattribs={"layer": layer},
    )

    # Fill
    hatch = msp.add_hatch(color=color, dxfattribs={"layer": fill_layer})
    edge_path = hatch.paths.add_edge_path()
    edge_path.add_ellipse(
        center=(cx, cy), major_axis=(rx, 0), ratio=ry / rx,
        start_angle=0, end_angle=360,
    )
    try:
        hatch.set_pattern_fill(hatch_pattern, scale=hatch_scale)
    except Exception:
        pass

    if name:
        msp.add_text(name, height=150, dxfattribs={
            "layer": layer, "insert": (cx - len(name) * 40, cy - 75),
        })


# ─── Sound Barrier Fence ────────────────────────────────────────────────────

def draw_sound_barrier(msp, doc, start: tuple, end: tuple,
                       thickness: float = 300,
                       layer: str = "SOUND_BARRIER", color: int = 8):
    """Draw a sound barrier fence — thick filled wall."""
    add_layer(doc, layer, color=color)

    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    if length < 1:
        return

    nx = -dy / length
    ny = dx / length
    half_t = thickness / 2

    corners = [
        (x1 + nx * half_t, y1 + ny * half_t),
        (x2 + nx * half_t, y2 + ny * half_t),
        (x2 - nx * half_t, y2 - ny * half_t),
        (x1 - nx * half_t, y1 - ny * half_t),
    ]

    msp.add_lwpolyline(corners, close=True,
                       dxfattribs={"layer": layer, "const_width": 15})

    # Fill
    hatch = msp.add_hatch(color=color, dxfattribs={"layer": layer})
    hatch.paths.add_polyline_path(corners, is_closed=True)

    # Label
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    msp.add_text("SOUND BARRIER", height=100, dxfattribs={
        "layer": layer, "insert": (mx - 500, my + half_t + 150),
    })


# ─── Ground Light ────────────────────────────────────────────────────────────

def draw_ground_light(msp, doc, cx: float, cy: float,
                      size: float = 200,
                      layer: str = "GROUND_LIGHTS", color: int = 2):
    """Draw a ground-level light fixture — small filled circle with glow ring."""
    add_layer(doc, layer, color=color)

    # Inner dot (fixture)
    msp.add_circle((cx, cy), radius=size * 0.3, dxfattribs={"layer": layer})
    hatch = msp.add_hatch(color=color, dxfattribs={"layer": layer})
    ep = hatch.paths.add_edge_path()
    ep.add_arc(center=(cx, cy), radius=size * 0.3, start_angle=0, end_angle=360)

    # Glow ring
    msp.add_circle((cx, cy), radius=size, dxfattribs={"layer": layer})


# ─── Bench (curved, for perimeter placement) ────────────────────────────────

def draw_curved_bench(msp, doc, cx: float, cy: float,
                      arc_radius: float = 1500,
                      arc_angle: float = 60,
                      start_angle: float = 0,
                      bench_width: float = 500,
                      layer: str = "BENCHES", color: int = 33):
    """Draw a curved bench as two concentric arcs (seat and backrest)."""
    add_layer(doc, layer, color=color)

    # Seat arc
    msp.add_arc(
        center=(cx, cy), radius=arc_radius,
        start_angle=start_angle, end_angle=start_angle + arc_angle,
        dxfattribs={"layer": layer, "lineweight": 30},
    )

    # Backrest arc (outer)
    msp.add_arc(
        center=(cx, cy), radius=arc_radius + bench_width,
        start_angle=start_angle, end_angle=start_angle + arc_angle,
        dxfattribs={"layer": layer, "lineweight": 15},
    )

    # End caps
    for a in [start_angle, start_angle + arc_angle]:
        rad = math.radians(a)
        inner = (cx + arc_radius * math.cos(rad), cy + arc_radius * math.sin(rad))
        outer = (cx + (arc_radius + bench_width) * math.cos(rad),
                 cy + (arc_radius + bench_width) * math.sin(rad))
        msp.add_line(inner, outer, dxfattribs={"layer": layer})


# ─── Trash Bin ───────────────────────────────────────────────────────────────

def draw_trash_bin(msp, doc, cx: float, cy: float,
                   size: float = 300,
                   layer: str = "FURNITURE", color: int = 8):
    """Draw a trash bin symbol — small square with X."""
    add_layer(doc, layer, color=color)

    half = size / 2
    corners = [(cx - half, cy - half), (cx + half, cy - half),
               (cx + half, cy + half), (cx - half, cy + half)]
    msp.add_lwpolyline(corners, close=True, dxfattribs={"layer": layer})
    msp.add_line(corners[0], corners[2], dxfattribs={"layer": layer})
    msp.add_line(corners[1], corners[3], dxfattribs={"layer": layer})
