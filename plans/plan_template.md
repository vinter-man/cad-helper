# Plan Template — Landscape Project

Use this structure for Phase 2 plans. Save to `plans/<project_name>.md`.

---

# Project: [Name]

## Design Concept

[2-3 sentences describing the vision. What feeling should the garden evoke? What's the central idea?]

## Site Summary

- Plot: [W]x[L] meters ([area] sq.m)
- Climate: [zone/description]
- Style: [style]
- Key constraint: [most important limitation]
- Key wish: [most important user desire]

## Zone Layout

Describe each zone with position relative to the plot.

| Zone | Position | Size (m) | Purpose |
|------|----------|----------|---------|
| Terrace | South side of house | 4x10 | Outdoor dining, lounging |
| Zen garden | SW corner | 9x7 | Meditation, visual focus |
| Pond area | West-center | 7x5 | Water feature, koi |
| Tea garden | NW corner | 7x6 | Quiet retreat |
| ... | ... | ... | ... |

## Element List

Every element that will be drawn. This is the contract — Phase 3 must implement all of these.

| # | Element | Position (x,y mm) | Size (mm) | Function | Layer | Notes |
|---|---------|-------------------|-----------|----------|-------|-------|
| 1 | Plot boundary | (0,0) | 25000x40000 | draw_plot | PLOT_BOUNDARY | |
| 2 | House | (9000, 23000) | 10000x12000 | draw_house | HOUSE | entrance south |
| 3 | Koi pond | center (6000, 16000) | rx=3500, ry=2500 | draw_pond | POND | irregular, rotation 15 |
| ... | ... | ... | ... | ... | ... | ... |

## Plant Palette

| Plant | Qty | Crown/Size | Position | Why chosen | Layer |
|-------|-----|-----------|----------|------------|-------|
| Black Pine (niwaki) | 3 | 2-3m | by pond, tea garden | evergreen structure | NIWAKI |
| Japanese Maple | 2 | 2-2.5m | by pond | autumn color | MAPLES |
| Sakura | 3 | 3.5m | east fence | spring bloom | SAKURA |
| ... | ... | ... | ... | ... | ... |

## Materials

| Surface | Material | Pattern | Notes |
|---------|----------|---------|-------|
| Main paths | stepping stones | tobi-ishi | irregular natural stone |
| Terrace | wood deck | LINE hatch | horizontal planks |
| Zen garden | raked gravel | AR-SAND | white/grey granite |
| ... | ... | ... | ... |

## Build Phases

Order of implementation in build.py:

1. **Site foundation**: plot, house, fence, compass
2. **Zones**: engawa, tea garden, zen garden area
3. **Water**: pond, stream, bridge
4. **Hardscape**: stepping stone paths
5. **Structures**: torii, pergola, bench, tsukubai
6. **Planting**: niwaki, maples, sakura, bamboo, azaleas, moss, hedge
7. **Lighting**: stone lanterns, subtle spots

## Open Questions

- [Any unresolved decisions for the user to confirm]

---

**Show this plan to the user. Wait for approval before Phase 3.**
