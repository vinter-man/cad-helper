"""Japanese garden elements — stone lanterns, zen garden, stepping stones,
tsukubai, torii gate, niwaki (cloud-pruned trees), bamboo fence.
"""

import math
from lib.core import add_layer


# ─── Stone Lantern (Toro) ────────────────────────────────────────────────────

def draw_stone_lantern(msp, doc, cx: float, cy: float, size: float = 600,
                       layer: str = "LANTERNS", color: int = 8):
    """Draw a traditional stone lantern (toro) symbol — top view.

    Concentric shapes: outer octagon (cap), inner square (firebox), center dot.
    """
    add_layer(doc, layer, color=color)
    r = size / 2

    # Outer octagon (cap/roof)
    pts = []
    for i in range(8):
        angle = math.radians(i * 45 + 22.5)
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})

    # Inner square (firebox)
    s = r * 0.5
    msp.add_lwpolyline(
        [(cx - s, cy - s), (cx + s, cy - s), (cx + s, cy + s), (cx - s, cy + s)],
        close=True, dxfattribs={"layer": layer},
    )

    # Center dot
    msp.add_circle((cx, cy), radius=r * 0.12, dxfattribs={"layer": layer})

    # Light rays (subtle cross)
    ray = r * 0.35
    for angle in [0, 90, 180, 270]:
        a = math.radians(angle)
        msp.add_line(
            (cx + ray * 0.4 * math.cos(a), cy + ray * 0.4 * math.sin(a)),
            (cx + ray * math.cos(a), cy + ray * math.sin(a)),
            dxfattribs={"layer": layer},
        )


# ─── Zen Rock Garden (Karesansui) ───────────────────────────────────────────

def draw_zen_garden(msp, doc, points: list[tuple[float, float]],
                    stones: list[dict] | None = None,
                    rake_spacing: float = 150,
                    rake_angle: float = 0,
                    layer: str = "ZEN_GARDEN", color: int = 8):
    """Draw a zen garden area with raked gravel and stones.

    Args:
        points: Boundary vertices.
        stones: List of {"cx", "cy", "rx", "ry", "rotation"} for each stone.
        rake_spacing: Distance between rake lines in mm.
        rake_angle: Angle of rake lines in degrees (0 = horizontal).
    """
    add_layer(doc, layer, color=color)
    add_layer(doc, f"{layer}_GRAVEL", color=253)  # light grey
    add_layer(doc, f"{layer}_STONES", color=8)

    # Boundary
    msp.add_lwpolyline(points, close=True,
                       dxfattribs={"layer": layer, "const_width": 10})

    # Gravel hatch
    hatch = msp.add_hatch(color=253, dxfattribs={"layer": f"{layer}_GRAVEL"})
    hatch.paths.add_polyline_path(points, is_closed=True)
    hatch.set_pattern_fill("AR-SAND", scale=15)

    # Rake lines
    _draw_rake_lines(msp, points, rake_spacing, rake_angle, f"{layer}_GRAVEL")

    # Stones
    if stones:
        for s in stones:
            _draw_stone(msp, s["cx"], s["cy"],
                       s.get("rx", 400), s.get("ry", 300),
                       s.get("rotation", 0),
                       layer=f"{layer}_STONES")
            # Concentric rake lines around stone
            _draw_stone_ripples(msp, s["cx"], s["cy"],
                               s.get("rx", 400), s.get("ry", 300),
                               layer=f"{layer}_GRAVEL")


def _draw_rake_lines(msp, boundary_pts, spacing, angle, layer):
    """Draw parallel rake lines across the garden area."""
    xs = [p[0] for p in boundary_pts]
    ys = [p[1] for p in boundary_pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)

    # Draw lines perpendicular to angle direction
    diag = math.sqrt((max_x - min_x)**2 + (max_y - min_y)**2)
    cx = (min_x + max_x) / 2
    cy = (min_y + max_y) / 2

    n_lines = int(diag / spacing)
    for i in range(-n_lines // 2, n_lines // 2 + 1):
        offset = i * spacing
        # Line perpendicular to rake_angle
        px = cx + offset * (-sin_a)
        py = cy + offset * cos_a
        x1 = px - diag * cos_a
        y1 = py - diag * sin_a
        x2 = px + diag * cos_a
        y2 = py + diag * sin_a
        msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": layer})


def _draw_stone(msp, cx, cy, rx, ry, rotation, layer):
    """Draw a natural stone as an irregular ellipse."""
    pts = []
    for i in range(12):
        angle = math.radians(i * 30)
        # Add slight irregularity
        irregularity = 1.0 + 0.15 * math.sin(angle * 3.7)
        x = rx * irregularity * math.cos(angle)
        y = ry * irregularity * math.sin(angle)
        # Rotate
        rad = math.radians(rotation)
        rx2 = x * math.cos(rad) - y * math.sin(rad)
        ry2 = x * math.sin(rad) + y * math.cos(rad)
        pts.append((cx + rx2, cy + ry2))
    msp.add_lwpolyline(pts, close=True,
                       dxfattribs={"layer": layer, "const_width": 15})

    # Fill
    hatch = msp.add_hatch(color=8, dxfattribs={"layer": layer})
    hatch.paths.add_polyline_path(pts, is_closed=True)


def _draw_stone_ripples(msp, cx, cy, rx, ry, layer, num_ripples=3):
    """Draw concentric elliptical ripples around a stone."""
    for r in range(1, num_ripples + 1):
        scale = 1.0 + r * 0.5
        pts = []
        for i in range(24):
            angle = math.radians(i * 15)
            x = rx * scale * math.cos(angle)
            y = ry * scale * math.sin(angle)
            pts.append((cx + x, cy + y))
        msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})


# ─── Stepping Stones (Tobi-ishi) ────────────────────────────────────────────

def draw_stepping_stones(msp, doc, waypoints: list[tuple[float, float]],
                         stone_size: float = 400,
                         spacing: float = 200,
                         layer: str = "STEPPING_STONES", color: int = 8):
    """Draw stepping stones along a path.

    Stones are placed alternately left and right of centerline
    for the classic tobi-ishi look.
    """
    add_layer(doc, layer, color=color)

    if len(waypoints) < 2:
        return

    # Walk along waypoints and place stones
    step = stone_size + spacing
    stone_idx = 0

    for seg in range(len(waypoints) - 1):
        x1, y1 = waypoints[seg]
        x2, y2 = waypoints[seg + 1]
        dx = x2 - x1
        dy = y2 - y1
        seg_len = math.sqrt(dx * dx + dy * dy)
        if seg_len < 1:
            continue

        # Direction and normal
        ux, uy = dx / seg_len, dy / seg_len
        nx, ny = -uy, ux

        dist = 0
        while dist < seg_len:
            px = x1 + ux * dist
            py = y1 + uy * dist

            # Alternate left-right offset
            side = 1 if stone_idx % 2 == 0 else -1
            offset = stone_size * 0.3
            sx = px + nx * offset * side
            sy = py + ny * offset * side

            # Draw irregular stone
            _draw_stepping_stone(msp, sx, sy, stone_size, stone_idx * 37, layer)

            dist += step
            stone_idx += 1


def _draw_stepping_stone(msp, cx, cy, size, seed, layer):
    """Draw a single irregular stepping stone."""
    r = size / 2
    pts = []
    for i in range(8):
        angle = math.radians(i * 45)
        # Pseudo-random irregularity based on seed
        irregularity = 0.85 + 0.3 * abs(math.sin(seed + i * 1.7))
        pts.append((cx + r * irregularity * math.cos(angle),
                    cy + r * irregularity * math.sin(angle)))
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer, "const_width": 8})

    hatch = msp.add_hatch(color=253, dxfattribs={"layer": layer})
    hatch.paths.add_polyline_path(pts, is_closed=True)


# ─── Tsukubai (Stone Water Basin) ───────────────────────────────────────────

def draw_tsukubai(msp, doc, cx: float, cy: float, diameter: float = 800,
                  layer: str = "TSUKUBAI", color: int = 140):
    """Draw a tsukubai (stone water basin) — top view.

    Circle with inner water circle and bamboo spout line.
    """
    add_layer(doc, layer, color=color)
    r = diameter / 2

    # Outer stone rim
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})
    msp.add_circle((cx, cy), radius=r * 0.7, dxfattribs={"layer": layer})

    # Water fill
    hatch = msp.add_hatch(color=140, dxfattribs={"layer": layer})
    edge_path = hatch.paths.add_edge_path()
    edge_path.add_arc(center=(cx, cy), radius=r * 0.7,
                      start_angle=0, end_angle=360)

    # Bamboo spout (line extending out)
    msp.add_line((cx + r, cy), (cx + r * 1.8, cy),
                 dxfattribs={"layer": layer, "lineweight": 30})

    # Label
    msp.add_text("TSUKUBAI", height=100, dxfattribs={
        "layer": layer, "insert": (cx - 250, cy - r - 250),
    })


# ─── Torii Gate ──────────────────────────────────────────────────────────────

def draw_torii(msp, doc, cx: float, cy: float, width: float = 2000,
               depth: float = 400,
               layer: str = "TORII", color: int = 1):
    """Draw a torii gate symbol — top view (two pillars + crossbeam)."""
    add_layer(doc, layer, color=color)
    half_w = width / 2
    pillar = 200

    # Two pillars
    for side in [-1, 1]:
        px = cx + side * (half_w - pillar / 2)
        msp.add_circle((px, cy), radius=pillar / 2,
                       dxfattribs={"layer": layer})
        h = msp.add_hatch(color=color, dxfattribs={"layer": layer})
        ep = h.paths.add_edge_path()
        ep.add_arc(center=(px, cy), radius=pillar / 2,
                   start_angle=0, end_angle=360)

    # Crossbeam (top view = rectangle)
    beam_y = cy - depth / 2
    msp.add_lwpolyline(
        [(cx - half_w * 1.1, beam_y),
         (cx + half_w * 1.1, beam_y),
         (cx + half_w * 1.1, beam_y + depth),
         (cx - half_w * 1.1, beam_y + depth)],
        close=True,
        dxfattribs={"layer": layer, "const_width": 10},
    )

    msp.add_text("TORII", height=120, dxfattribs={
        "layer": layer, "insert": (cx - 180, cy + depth),
    })


# ─── Niwaki (Cloud-Pruned Tree) ─────────────────────────────────────────────

def draw_niwaki(msp, doc, cx: float, cy: float, crown_diameter: float = 3000,
                num_clouds: int = 5, label: str = "",
                layer: str = "NIWAKI", color: int = 83):
    """Draw a niwaki (cloud-pruned tree) — overlapping circles representing cloud pads."""
    add_layer(doc, layer, color=color)
    r = crown_diameter / 2

    # Trunk (center dot)
    msp.add_circle((cx, cy), radius=r * 0.08, dxfattribs={"layer": layer})
    h = msp.add_hatch(color=33, dxfattribs={"layer": layer})
    ep = h.paths.add_edge_path()
    ep.add_arc(center=(cx, cy), radius=r * 0.08,
               start_angle=0, end_angle=360)

    # Cloud pads — asymmetric arrangement
    cloud_r = r * 0.4
    for i in range(num_clouds):
        # Spread clouds unevenly (golden angle)
        angle = i * 137.5 * math.pi / 180
        dist = r * (0.3 + 0.4 * (i / num_clouds))
        cloud_cx = cx + dist * math.cos(angle)
        cloud_cy = cy + dist * math.sin(angle)
        # Varying cloud sizes
        cr = cloud_r * (0.7 + 0.6 * abs(math.sin(i * 1.3)))
        msp.add_circle((cloud_cx, cloud_cy), radius=cr,
                       dxfattribs={"layer": layer})

    # Outer boundary hint
    msp.add_circle((cx, cy), radius=r, dxfattribs={"layer": layer})

    if label:
        msp.add_text(label, height=150, dxfattribs={
            "layer": layer, "insert": (cx + r + 100, cy - 75),
        })


# ─── Bamboo Fence Section (Takegaki) ────────────────────────────────────────

def draw_bamboo_fence(msp, doc, start: tuple[float, float],
                      end: tuple[float, float],
                      height_symbol: float = 300,
                      layer: str = "BAMBOO_FENCE", color: int = 33):
    """Draw a bamboo fence section — top view with cross-hatching."""
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
    half_h = height_symbol / 2

    # Main rectangle
    corners = [
        (x1 + nx * half_h, y1 + ny * half_h),
        (x2 + nx * half_h, y2 + ny * half_h),
        (x2 - nx * half_h, y2 - ny * half_h),
        (x1 - nx * half_h, y1 - ny * half_h),
    ]
    msp.add_lwpolyline(corners, close=True, dxfattribs={"layer": layer})

    # Cross-hatch lines (bamboo slats)
    slat_spacing = 200
    n_slats = int(length / slat_spacing)
    for i in range(1, n_slats):
        t = i / n_slats
        px = x1 + dx * t
        py = y1 + dy * t
        msp.add_line(
            (px + nx * half_h, py + ny * half_h),
            (px - nx * half_h, py - ny * half_h),
            dxfattribs={"layer": layer},
        )


# ─── Moss Area ───────────────────────────────────────────────────────────────

def draw_moss_area(msp, doc, points: list[tuple[float, float]],
                   layer: str = "MOSS", color: int = 83):
    """Draw a moss-covered area with dense stippling pattern."""
    add_layer(doc, layer, color=color)

    msp.add_lwpolyline(points, close=True,
                       dxfattribs={"layer": layer, "const_width": 5})

    hatch = msp.add_hatch(color=color, dxfattribs={"layer": layer})
    hatch.paths.add_polyline_path(points, is_closed=True)
    hatch.set_pattern_fill("DOTS", scale=40)
