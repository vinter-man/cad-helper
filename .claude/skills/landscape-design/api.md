# cad_helper API reference

Every drawing function takes `(msp, doc, ...)` first: the model space and the
document from `create_document()`. All lengths in mm. Points are `(x, y)` tuples.
Functions create their own layers; the layer name is the `layer=` default unless noted.

```python
from cad_helper.core import create_document
doc = create_document()        # R2010, mm units, AutoCAD linetypes and dimstyles loaded
msp = doc.modelspace()
```

## Site — `cad_helper.site`

```python
draw_plot(msp, doc, width, length)                    # boundary + overall dimensions; width = X, length = Y
draw_house(msp, doc, x, y, w, h, label="HOUSE",
           entrance_side="south", entrance_width=1200,
           entrance_center=None)                      # (x, y) = SW corner; door anywhere along a side
draw_fence(msp, doc, width, length, gates=[
    {"side": "south", "center": 12_500, "opening": 1_500, "label": "GATE"},
])                                                    # center measured from the W (or S) end of the side
draw_wall(msp, doc, start, end, thickness=200, label="")
draw_steps(msp, doc, x, y, w, tread=300, count=2, label="")   # rises northwards
draw_compass(msp, doc, x, y, size=1500)
draw_distance(msp, doc, p1, p2, offset=500, text_height=250)  # real AutoCAD dimension, in metres
```

## Zones — `cad_helper.zones`

```python
draw_zone(msp, doc, points, name, color=3, hatch_pattern="ANSI31", hatch_scale=100)
draw_rect_zone(msp, doc, x, y, w, h, name, color=3, hatch_pattern="ANSI31", hatch_scale=100)
```

Layers `ZONE_<NAME>` and `ZONE_<NAME>_FILL`. Hatch patterns are AutoCAD `acad.pat`
names; an unknown name raises `ValueError`. Useful ones: `ANSI31` (diagonal),
`ANSI37` (cross), `AR-SAND` (gravel, sand), `AR-BRSTD` (brick), `AR-CONC` (concrete),
`GRASS`, `DOTS`, `LINE` (decking), `EARTH`.

## Paths — `cad_helper.paths`

```python
draw_path(msp, doc, waypoints, path_width=1200, layer="PATHS", color=33)
draw_straight_path(msp, doc, start, end, path_width=1200)
```

Waypoints are B-spline control points: the path starts and ends on the first and last
and is pulled towards the others.

## Furniture — `cad_helper.furniture`

```python
draw_bench(msp, doc, x, y, w=1800, h=500, rotation=0)          # backrest on the north edge
draw_pergola(msp, doc, x, y, w, h)
draw_table_with_chairs(msp, doc, cx, cy, table_diameter=1200, num_chairs=6)
draw_rect_table(msp, doc, cx, cy, w=800, h=600, chairs="NS", chair_diameter=450, label="")
draw_bbq_zone(msp, doc, x, y, grill_w=1200, grill_h=600, counter_w=2000, counter_h=600, layout="L")
draw_fire_pit(msp, doc, cx, cy, diameter=1000, seat_radius=1800, seat_arc=240)  # bench open to the south
```

## Planting — `cad_helper.planting`

```python
draw_tree(msp, doc, cx, cy, crown_diameter=4000, label="", layer="TREES", color=83)
draw_shrub(msp, doc, cx, cy, diameter=1500, label="", layer="SHRUBS", color=3)
draw_hedge(msp, doc, points, hedge_width=800)
draw_flower_bed(msp, doc, points, name="FLOWER BED", smooth=True)   # smooth rounds the corners
draw_round_bed(msp, doc, cx, cy, diameter=3000, name="FLOWER BED")
draw_lawn(msp, doc, points)
draw_planter(msp, doc, x, y, w, h, label="")                      # trough or pot, (x, y) = SW corner
```

Size trees at their mature crown diameter. Give each species its own `layer=` so it
can be counted and switched off in AutoCAD.

## Japanese garden — `cad_helper.japanese`

```python
draw_zen_garden(msp, doc, points, stones=[
    {"cx": 4_500, "cy": 6_500, "rx": 500, "ry": 350, "rotation": 15, "ripples": 3},
], rake_spacing=150, rake_angle=0)        # rake lines clipped to the outline, stop at ripples
draw_stepping_stones(msp, doc, waypoints, stone_size=400, spacing=200, layer="STEPPING_STONES")
draw_stone_lantern(msp, doc, cx, cy, size=600)
draw_tsukubai(msp, doc, cx, cy, diameter=800)
draw_torii(msp, doc, cx, cy, width=2000)
draw_niwaki(msp, doc, cx, cy, crown_diameter=3000, num_clouds=5, label="")
draw_bamboo_fence(msp, doc, start, end)
draw_moss_area(msp, doc, points)
```

## Water — `cad_helper.water`

```python
draw_pond(msp, doc, cx, cy, rx=3000, ry=2000, rotation=0, irregular=True, label="POND")
draw_stream(msp, doc, waypoints, width=600)
draw_bridge(msp, doc, cx, cy, width=2000, depth=1200, arched=True, rotation=0)  # width = span
```

## Lighting — `cad_helper.lighting`

```python
draw_path_light(msp, doc, cx, cy)
draw_spotlight(msp, doc, cx, cy)
draw_lights_along_path(msp, doc, waypoints, spacing=3000)
```

## Playground — `cad_helper.playground`

```python
draw_ellipse_zone(msp, doc, cx, cy, rx, ry, name="", color=3, hatch_pattern="DOTS", layer=None)
draw_sandbox(msp, doc, cx, cy, rx=1500, ry=1200)
draw_slide(msp, doc, cx, cy, length=2500, width=600, rotation=0)
draw_climbing_frame(msp, doc, cx, cy, w=2000, h=2000, frame_type="net")   # or "dome"
draw_swing(msp, doc, cx, cy, width=2500, depth=1200, num_seats=2)
draw_seesaw(msp, doc, cx, cy, length=2500, rotation=0)
draw_rubber_bridge(msp, doc, start, end, width=800)
draw_sound_barrier(msp, doc, start, end, thickness=300)
draw_ground_light(msp, doc, cx, cy)
draw_curved_bench(msp, doc, cx, cy, arc_radius=1500, arc_angle=60, start_angle=0)
draw_trash_bin(msp, doc, cx, cy)
```

## Checks — `cad_helper.checks`

```python
from cad_helper.checks import Clearance
CLEARANCES = [
    Clearance("HOUSE", "POND*", 3_000, "water away from foundations"),
    Clearance("BBQ", "TREES", 3_000, "no branches over the grill"),
]
```

Layer names accept shell wildcards. Distances are measured between the real outlines
(circles, polylines, hatches), not bounding boxes. Other automatic checks: ezdxf audit,
entities outside `BOUNDS`, entities on layer 0, empty layers, text smaller than 1.5 mm
at `PLOT_SCALE`.

## Colours (AutoCAD Color Index)

1 red · 2 yellow · 3 green · 4 cyan · 5 blue · 6 magenta · 7 white/black · 8 grey ·
30 orange · 33 brown · 83 light green · 140 light blue · 200 purple · 220 pink ·
250–254 greys, dark to light.
