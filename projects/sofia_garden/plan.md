# Project: Sofia garden

## Design concept

A small Japanese garden seen from a timber deck. A single stepping-stone path leads
from the gate past a cherry to the deck; the pond is the centre of the view, with a
maple leaning over its west end. In revision 2 the gravel garden became a fire circle
for summer evenings, and the pond grew.

## Site summary

- Plot: 12 x 18 m (216 m²), flat, north up
- Climate: Sofia, continental, USDA 6b
- Style: Japanese, calm
- Key constraint: neighbours close on the east
- Key wish: a pond and somewhere to cook outside with friends

## Zones

| Zone | Position | Size | Purpose |
|------|----------|------|---------|
| House | north, (1000, 11500) | 10 x 6 m | existing |
| Deck | south of house, (1500, 9100) | 7 x 2.4 m | sitting, view over the pond |
| Grill corner | east of deck, (9000, 9300) | 1.8 x 1.9 m, L-shaped | cooking |
| Pond | centre (4300, 5900) | 5.2 x 3.4 m | focal point |
| Fire circle (rev. 2) | centre (2700, 2000) | Ø 3.96 m gravel | evenings, replaces the gravel garden |
| Lawn strip | between pond and deck | ~6.5 x 0.9 m | soft ground for the dog |
| Privacy hedge | along the east fence | 0.6 x 9.8 m | screen from the neighbours |

## Elements

| Element | Position (mm) | Size | Function | Layer |
|---------|---------------|------|----------|-------|
| Plot, dimensions | (0, 0) | 12000 x 18000 | `draw_plot` | PLOT_BOUNDARY, DIMENSIONS |
| House | (1000, 11500) | 10000 x 6000, door south | `draw_house` | HOUSE |
| Fence, gate | south, gate centre x=9800 | opening 1200 | `draw_fence` | FENCE, GATES |
| Deck | (1500, 9100) | 7000 x 2400, LINE hatch | `draw_rect_zone` | ZONE_DECK |
| Grill + counter | (9000, 9300) | grill 1200 x 600, counter 600 x 1900 | `draw_bbq_zone` | BBQ |
| Pond | (4300, 5900) | rx 2600, ry 1700, rotated -8° | `draw_pond` | POND, POND_FILL |
| Fire pit + bench | (2700, 2000) | pit Ø 1000, bench r 1500-1950, open south | `draw_fire_pit` | FIRE_PIT, FIRE_PIT_SEATING |
| Gravel circle | (2700, 2000) | r 1980 | `draw_zone` | ZONE_GRAVEL |
| Main path | gate → deck | 450 stones, 250 joints | `draw_stepping_stones` | STEPPING_STONES |
| Fire path | main path → bench gap | 400 stones | `draw_stepping_stones` | STEPPING_STONES_FIRE |
| Path lights | 800 mm east of the path, every 3 m | | `draw_lights_along_path` | LIGHTING |
| Stone lantern | (6600, 7000) | 550 | `draw_stone_lantern` | LANTERNS |

## Plant palette

| Plant | Qty | Size | Position | Why |
|-------|-----|------|----------|-----|
| Acer palmatum | 1 | crown 2.2 m | west end of the pond | autumn colour over water, hardy to -25 °C |
| Pinus thunbergii (niwaki) | 1 | crown 1.8 m | (7300, 1800), south | evergreen structure; moved east in rev. 2, see below |
| Prunus serrulata | 1 | crown 2.6 m | (9900, 4800), by the path | spring flowers at the entrance |
| Taxus baccata hedge | 9.8 m | 0.6 m wide | east fence | dense evergreen screen, tolerates clipping and shade |
| Moss | 1 bed | ~2 x 1 m | under the pine | |
| Lawn | 1 strip | | pond to deck | the dog |

## Materials

| Surface | Material | Hatch |
|---------|----------|-------|
| Deck | thermo-ash boards | LINE |
| Paths | irregular granite stepping stones | solid grey |
| Fire circle | 8/16 mm grey gravel | AR-SAND |

## Clearance rules

| A | B | Min (mm) | Why |
|---|---|----------|-----|
| HOUSE | POND* | 3000 | water away from foundations |
| BBQ | MAPLE, NIWAKI | 3000 | no branches over the grill |
| FIRE_PIT | NIWAKI, MAPLE | 3000 | sparks vs crowns |
| FIRE_PIT | HOUSE | 4000 | smoke and sparks |
| FIRE_PIT_SEATING | POND* | 300 | bench on dry ground |
| STEPPING_STONES* | POND* | 300 | dry path |
| LAWN, ZONE_GRAVEL | POND* | 100 | edges stay dry |

## Revision 2 (user: "make the pond bigger and swap the gravel garden for a fire pit")

- Pond rx/ry 2000/1300 → 2600/1700, centre moved to (4300, 5900).
- Gravel garden removed; fire pit with a 240° bench and a gravel circle in its place.
- First build failed two checks (fire 1549 mm from the pine crown; bench over the
  enlarged pond). Fix: pine moved from (5900, 2000) to (7300, 1800), fire pit moved
  from (3000, 2400) to (2700, 2000).
- Lawn edge pulled north off the larger pond; stepping-stone branch added to the bench gap.
