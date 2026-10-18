# Project: Japanese backyard

## Design concept

A stroll garden read from the engawa. You enter through a torii by the gate, pass the
dry garden, and reach the veranda on a stepping-stone path. Water rises at a spring
beside the house, runs south under a timber bridge and fills the koi pond; the dry
garden by the gate stays dry. The tea garden sits behind a bamboo fence in the
north-west corner and is reached across the bridge.

## Zones

| Zone | Position (mm) | Size | Purpose |
|------|---------------|------|---------|
| House | (9000, 23000) | 10 x 12 m | existing |
| Engawa | (8500, 20500) | 11 x 2.5 m | timber veranda, main viewpoint |
| Koi pond | centre (6500, 15000) | rx 3500, ry 2500, rotated 15° | focal point |
| Stream | (5800, 27500) → pond | 550 wide | spring to pond |
| Dry garden | (1500, 2500) | 9 x 7 m, tapered | karesansui seen from the gate |
| Tea garden | (1000, 32000) | 7 x 6 m, tapered | roji with tsukubai |

## Elements

| Element | Position / route | Function | Layer |
|---------|------------------|----------|-------|
| Plot, fence, gate | gate centre x=14500, opening 1500 | `draw_plot`, `draw_fence` | PLOT_BOUNDARY, FENCE, GATES |
| Main path | gate → torii → east of pond → engawa | `draw_stepping_stones` 450/250 | STEPPING_STONES |
| Tea path | engawa → bridge → round the spring → fence gap → tsukubai | `draw_stepping_stones` 400/300 | STEPPING_STONES_TEA |
| Pond path | main path → north shore → engawa | `draw_stepping_stones` 400/250 | STEPPING_STONES_POND |
| Bridge | (4500, 23900), span 1800 | `draw_bridge` arched | BRIDGE |
| Torii | (14600, 1800) | `draw_torii` | TORII |
| Wisteria pergola + bench | (10800, 12300), 3 x 2.6 m | `draw_pergola`, `draw_bench` | FUJIDANA, FURNITURE |
| Tsukubai | (3200, 35200) | `draw_tsukubai` | TSUKUBAI |
| Dry garden stones | 3-stone group + pair, ripples 3/0/0/2/0 | `draw_zen_garden` | ZEN_GARDEN_* |
| Bamboo fences | behind dry garden; roji edge with a 1.2 m gap | `draw_bamboo_fence` | BAMBOO_FENCE |
| Stone lanterns | 6: pond, dry garden, roji, main path, gate, spring | `draw_stone_lantern` | LANTERNS |
| Spotlights | along the engawa edge, every 2.5 m | `draw_spotlight` | LIGHTING_SUBTLE |

## Plant palette

| Plant | Qty | Size | Position | Why |
|-------|-----|------|----------|-----|
| Black pine (niwaki) | 3 | crowns 3.0 / 2.5 / 2.0 m | west of pond, south of pond, roji | evergreen structure, never in a row |
| Japanese maple | 2 | 2.5 / 2.0 m | over the pond | autumn colour reflected in water |
| Sakura | 3 | 3.5 m | along the east fence | spring flowers, borrowed depth |
| Bamboo | 7 clumps | 0.8 m | north-east corner | screen |
| Azalea | 5 (3 + 2) | 1.0-1.5 m | both ends of the engawa | clipped mounds |
| Moss | 2 areas | | under the west pine, inside the roji | |
| Low hedge | 10.5 m | 0.6 m | inside the south fence | frames the dry garden |

## Clearance rules

| A | B | Min (mm) | Why |
|---|---|----------|-----|
| HOUSE | POND* | 3000 | water away from foundations |
| HOUSE | SAKURA | 2000 | crowns clear of the walls |
| STEPPING_STONES* | POND* | 300 | dry paths |
| STEPPING_STONES* | STREAM | 150 | stones stay off the water |
| STEPPING_STONES* | FUJIDANA | 300 | the path passes beside the pergola |
