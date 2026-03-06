# Project: Bar Patio Landscaping — Велико Търново

## Design Concept

Създаваме **"Тайна мексиканска градина в старо българско дворче"** — комбинация от увивни лози (българска традиция) и сукуленти/кактуси (мексикански акцент). Патиото е малко (4x4м), затова избягваме претрупване. Растенията са в **саксии/кашпи** (не в земя), така че са мобилни. Вечерното осветление от фенера подчертава силуетите на растенията и създава интимна атмосфера.

## Zone Layout

- Zone 1: PATIO — (0, 0) — 4000x4000 мм
- Zone 2: BAR INTERIOR — (0, 4000) — 8000x4000 мм
- Zone 3: STAIRS — (1500, -600) — 1000x600 мм (2 стъпала)
- Zone 4: WEST FENCE — (-200, 0→4000) — H=800 мм
- Zone 5: EAST FENCE — (4200, 0→4000) — H=800 мм

## Elements

| Element | Position (x,y) | Size | Function | Layer |
|---------|---------------|------|----------|-------|
| Patio zone | (0, 0) | 4000x4000 | draw_rect_zone | PATIO |
| Bar interior | (0, 4000) | 8000x4000 | draw_house | BUILDING |
| Stairs | (1500, -600) | 1000x600 | rectangles | STAIRS |
| West fence | (-200, 0)→(-200, 4000) | H=800 | line | FENCE |
| East fence | (4200, 0)→(4200, 4000) | H=800 | line | FENCE |
| Table 1 | (800, 600) | 800x600 | rectangle | FURNITURE |
| Table 2 | (2400, 600) | 800x600 | rectangle | FURNITURE |
| Table 3 | (800, 2200) | 800x600 | rectangle | FURNITURE |
| Table 4 | (2400, 2200) | 800x600 | rectangle | FURNITURE |
| Chairs | around tables | Ø450 | circles | FURNITURE |
| Vine planter W | (100, 500) | 600x3000 | rectangle | PLANTERS |
| Vine planter E | (3300, 500) | 600x3000 | rectangle | PLANTERS |
| Cactus 1 | (200, 200) | Ø400 | draw_shrub | PLANTS |
| Cactus 2 | (3600, 200) | Ø400 | draw_shrub | PLANTS |
| Cactus 3 | (200, 3600) | Ø400 | draw_shrub | PLANTS |
| Cactus 4 | (3600, 3600) | Ø400 | draw_shrub | PLANTS |
| Herb planter 1 | (1800, 1400) | 300x300 | rectangle | PLANTERS |
| Herb planter 2 | (1800, 2600) | 300x300 | rectangle | PLANTERS |
| Lantern | (1800, 4000) | point | draw_path_light | LIGHTING |
| Compass | (4500, 4500) | 500 | draw_compass | COMPASS |

## Plant Palette

| Plant | Qty | Size | Position | Why |
|-------|-----|------|----------|-----|
| Grape vine (Vitis vinifera) | 2 | 3m length | W/E fence | Bulgarian tradition, fast cover |
| Opuntia cactus | 4 | Ø400 pot | 4 corners | Mexican classic, drought-resistant |
| Echeveria mix | 8-10 | Ø100-150 | Between tables | Decorative succulents, low maintenance |
| Rosemary (Rosmarinus) | 2 | H=400, 300x300 pot | Central | Aromatic, blue flowers, culinary |
| Lavender (Lavandula) | 2-3 | H=300, group | Near chairs | Aromatic, purple evening flowers |
| Begonia | 4-6 | Small, hanging | Additional | Color (pink/red) warmth |

## Materials

- **Pots:** Terracotta (for cacti and herbs)
- **Vine planters:** Wooden or metal long troughs (~60x300cm)
- **Trellis for vines:** Wood or metal, fixed to fence (not drawn)

## Build Phases

1. Site foundation (patio, bar, fences, stairs, compass)
2. Furniture (tables, chairs)
3. Planters and plants (vine troughs, corner cacti, herb planters)
4. Lighting (lantern symbol)
5. Labels (plant names, dimensions)
