# Plan: Bar Patio, Veliko Tarnovo

Source of truth: `build.py`. Build with `uv run cad-helper build bar_patio`.

## Design concept

A small evening terrace in front of a bar, planted like a hidden Mexican garden in an old Bulgarian courtyard. Grape vines in troughs cover the low concrete walls, opuntia in terracotta pots hold the four corners, and rosemary and lavender flank the bar door. Four bistro tables sit either side of a 1 m aisle that runs straight from the street steps to the door.

## Site summary

- Patio 4000 x 4000 mm; bar interior 8000 x 4000 mm directly north of it
- Origin (0, 0) is the south-west corner of the patio; X = east, Y = north
- Low concrete walls (about 800 mm high, drawn 200 mm thick) on the west and east sides
- Two steps up from the street on the south side
- Veliko Tarnovo, USDA zone 6b-7a, full sun, no shade structure
- Used in the evenings only; all planting in containers
- Printed at 1:50

## Zone layout

| Zone | Position (x, y) | Size (mm) |
|------|-----------------|-----------|
| Patio | (0, 0) | 4000 x 4000 |
| Bar interior | (0, 4000) | 8000 x 4000 |
| Street steps | (1500, -600) | 1000 x 600, 2 treads of 300 |
| West wall | x = -200 to 0, y = 0 to 4000 | 200 thick |
| East wall | x = 4000 to 4200, y = 0 to 4000 | 200 thick |
| Central aisle | x = 1500 to 2500, y = 0 to 4000 | 1000 wide |

```
              N
  +-------------------------------+
  |  BAR  8 x 4 m                 |
  |      lantern                  |
  +--[H]--door--[H]---------------+   y = 4000
  |C              C|
  |V  T3      T4  V|   V = vine trough
  |V              V|   C = opuntia pot
  |V     aisle    V|   H = herb planter
  |V  T1      T2  V|   T = table, chairs N and S
  |C              C|
  +-----[steps]----+                  y = 0
  x=0            x=4000
```

## Elements

| Element | Position (x, y) | Size (mm) | Function | Layer |
|---------|-----------------|-----------|----------|-------|
| Patio surface | (0, 0) | 4000 x 4000, AR-SAND hatch | `draw_rect_zone` | ZONE_PATIO, ZONE_PATIO_FILL |
| Bar | (0, 4000) | 8000 x 4000, label "BAR" | `draw_house` | HOUSE, HOUSE_FILL |
| Bar door | centred on x = 2000, south wall | 900 opening (x 1550 to 2450), outward swing | `draw_house` (entrance) | HOUSE |
| West wall | centreline x = -100, y 0 to 4000 | 200 thick, label "CONCRETE WALL h=800" | `draw_wall` | WALLS |
| East wall | centreline x = 4100, y 0 to 4000 | 200 thick | `draw_wall` | WALLS |
| Steps | (1500, -600) | 1000 wide, 2 x 300 treads | `draw_steps` | STEPS |
| Table T1 | centre (1150, 820) | 700 x 700 | `draw_rect_table` | FURNITURE |
| Table T2 | centre (2850, 820) | 700 x 700 | `draw_rect_table` | FURNITURE |
| Table T3 | centre (1150, 2800) | 700 x 700 | `draw_rect_table` | FURNITURE |
| Table T4 | centre (2850, 2800) | 700 x 700 | `draw_rect_table` | FURNITURE |
| Chairs (8) | north and south of each table, centres at y = 220, 1420, 2200, 3400 | Ø400 | `draw_rect_table` (chairs="NS") | FURNITURE |
| Vine trough W | (0, 400) | 300 x 3200 | `draw_planter` | PLANTERS |
| Vine trough E | (3700, 400) | 300 x 3200 | `draw_planter` | PLANTERS |
| Opuntia pots (4) | (200, 200), (3800, 200), (200, 3800), (3800, 3800) | Ø380 | `draw_shrub` | PLANTS |
| Herb planter W | (1100, 3700) | 300 x 250, 50 mm off the facade | `draw_planter` | HERBS |
| Herb planter E | (2600, 3700) | 300 x 250, 50 mm off the facade | `draw_planter` | HERBS |
| Herb plants (2) | (1250, 3825), (2750, 3825) | Ø250 | `draw_shrub` | HERBS |
| Lantern | (2000, 4250), over the door | 300 ring | `draw_path_light` | LIGHTING |
| North arrow | (5200, 2500) | 800 | `draw_compass` | COMPASS |
| Dimension, patio width | south edge, 0 to 4000 | 4 m | `draw_distance` | DIMENSIONS |
| Dimension, patio depth | east side, 0 to 4000 | 4 m | `draw_distance` | DIMENSIONS |

Circulation: the aisle between table edges is 1000 mm (x 1500 to 2500). Between the chair columns it is 1300 mm. The herb planters stand outside the aisle, 600 to 900 mm either side of the door centre. The door leaf opens outward, hinged at x = 1550; when fully open it is 150 mm from the west herb planter, and the strike jamb is about 120 mm from the east one. Table edges are 500 mm from the vine troughs.

## Plant palette

| Plant | Qty | Size | Position | Why |
|-------|-----|------|----------|-----|
| Grape vine (*Vitis vinifera*) | 2 troughs | 300 x 3200 mm trough | Along the west and east walls | Bulgarian tradition, covers the walls quickly |
| Opuntia | 4 | Ø380 pot | Patio corners | Mexican accent, drought-tolerant |
| Rosemary (*Rosmarinus officinalis*) | 1 | 300 x 250 planter | Beside the bar door | Fragrant, blue flowers, culinary |
| Lavender (*Lavandula*) | 1 | 300 x 250 planter | Beside the bar door | Fragrant, purple flowers that read in the evening |

All four species tolerate full sun and drought, which suits Veliko Tarnovo. The drawing labels the vine troughs only; the pots and herb planters are unlabelled symbols.

## Materials

- Pots: terracotta, for the cacti and herbs
- Vine troughs: long wooden or metal troughs, 300 mm wide in the drawing
- Vine supports: wooden or metal trellis fixed to the walls (not drawn)
- Walls: existing concrete, about 800 mm high
- Patio surface: existing; shown with an AR-SAND hatch (material not specified in the brief)

## Build phases

1. Site: patio zone, bar with door, both walls, steps, north arrow, two dimensions
2. Furniture: four tables with two chairs each
3. Planting: vine troughs, corner opuntia, herb planters by the door
4. Lighting: one lantern over the door

## Changes from the first draft

- Seating: the first draft had 4 rectangular tables (800 x 600) with about 16 chairs (Ø450). Sixteen seats did not fit 16 m² with room to circulate, so the build uses 4 square bistro tables (700 x 700) with 2 chairs each (Ø400), 8 seats in total.
- Layout: tables now form a 2 x 2 grid either side of a 1000 mm aisle aligned with the steps and the door.
- Bar door: moved to the patio centre line (x = 2000). It was centred on the 8 m bar (x = 4000), which put it outside the patio.
- Herb planters: moved from the middle of the aisle, (1800, 1400) and (1800, 2600), to either side of the bar door. After review they were reduced to 300 x 250, set 50 mm off the facade and moved out to x 1100 to 1400 and 2600 to 2900, so the door leaf no longer opens against the west planter.
- Vine troughs: narrowed from 600 to 300 mm and set against the walls.
- Walls, steps, tables and planters are drawn with library functions (`draw_wall`, `draw_steps`, `draw_rect_table`, `draw_planter`) instead of hand-written rectangles and lines.
- Lantern: moved from (1800, 4000) to (2000, 4250), centred over the door.
- Echeveria (8 to 10) and begonia (4 to 6) from the first-draft palette are not drawn in the current build, and there are no pots between the tables.
