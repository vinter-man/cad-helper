# Project: School Alley (Училищна алея)

## Design Concept
Модерна пешеходна алея (3x50m) между две училища с градиентна плочна композиция — светли тонове в центъра, преливащи към тъмни в периферията. Два джоба за сядане с пергол и пейки в двата края, цветни лехи и храсти по протежението.

## Coordinate System
- Origin (0,0): SW corner на настилката
- X: 0→50000 (изток, дължина на алеята)
- Y: 0→3000 (север, ширина на алеята)
- Бордюри: Y=-150..0 (юг), Y=3000..3150 (север)

## Overall Layout

```
                    N (Y+)
    ┌─────────────────────────────────────────────────────┐ Y=3150 (north curb)
    │ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ CURB ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒│ Y=3000
    │                                        ┌──────────┐│
    │  DARK 100x100 tiles                    │ EAST     ││
    │  MID  300x150 tiles                    │ POCKET   ││
W   │  LIGHT 600x300/450x300/300x300         │ pergola+ ││  E
    │  MID  300x150 tiles                    │ benches  ││
    │  DARK 100x100 tiles                    └──────────┘│
    │┌──────────┐                                        │
    ││ WEST     │                                        │
    ││ POCKET   │                                        │
    ││ pergola+ │                                        │ Y=0
    │▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ CURB ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒│ Y=-150
    └─────────────────────────────────────────────────────┘
    X=0                                              X=50000
```

## Tile Composition — Cross Section (3000mm width)

5 бандове от юг към север, симетрични спрямо центъра:

| Band | Y range | Width | Tile sizes | Color (ACI) | Description |
|------|---------|-------|------------|-------------|-------------|
| Edge S | 0–300 | 300mm | 100x100 | 250 (dark grey) | Тъмен акцент |
| Trans S | 300–750 | 450mm | 300x150 | 252 (med grey) | Преход |
| Center | 750–2250 | 1500mm | 600x300, 450x300, 300x300 | 254 (light grey) | Светъл център |
| Trans N | 2250–2700 | 450mm | 300x150 | 252 (med grey) | Преход |
| Edge N | 2700–3000 | 300mm | 100x100 | 250 (dark grey) | Тъмен акцент |

Gap между плочите: 5mm. Плочите се подреждат в редове по X с разместване (offset) за динамичен ефект.

## Seating Pockets

### West Pocket (south side)
- **Position**: X=1000..5000, Y=-3500..0
- **Size**: 4000 x 3500mm
- **Elements**:
  - Pergola 3500x3000 (комбинирана — дърво+метал)
  - 2 пейки (1800x500) под перголата
  - Настилка: 300x300 плочи (среден тон)
  - Храсти (3 бр.) около пейките

### East Pocket (north side)
- **Position**: X=45000..49000, Y=3000..6500
- **Size**: 4000 x 3500mm
- **Elements**:
  - Pergola 3500x3000
  - 2 пейки (1800x500)
  - Настилка: 300x300 плочи
  - Храсти (3 бр.)

## Flower Compositions

| Element | Position | Size | Description |
|---------|----------|------|-------------|
| Flower bed W | X=6000..9000, south side | 3000x1500 | Лавандула + шапчета |
| Flower bed center-S | X=21000..26000, south | 5000x1200 | Миксбордер |
| Flower bed center-N | X=23000..28000, north | 5000x1200 | Миксбордер |
| Flower bed E | X=40000..43000, north side | 3000x1500 | Рози + декоративни треви |
| Round bed | X=25000, center north | D=2000 | Кръгла леха — акцент |

## Shrubs at Benches

- 3 храста по 1000mm около всеки джоб за сядане (Spiraea, Berberis — подходящи за София)

## Curbs

- South curb: (0, -150) to (50000, 0), height 150mm
- North curb: (0, 3000) to (50000, 3150), height 150mm
- Pocket curbs extend around pocket perimeters

## Layers

| Layer | Color | Content |
|-------|-------|---------|
| CURB | 8 | Бордюри |
| TILE_DARK | 250 | Edge tiles 100x100 |
| TILE_MID | 252 | Transition tiles 300x150 |
| TILE_LIGHT | 254 | Center tiles (mixed large) |
| TILE_POCKET | 253 | Pocket paving |
| PERGOLA | 33 | Пергол |
| FURNITURE | 6 | Пейки |
| SHRUBS | 3 | Храсти |
| FLOWERS | 83 | Цветни лехи |
| FLOWERS_ROUND | 2 | Кръгла леха |
| DIMENSIONS | 7 | Размерни линии |
| LABELS | 7 | Текст |

## Build Phases
1. Curbs and alley boundary
2. Tile composition (5 bands)
3. Seating pocket paving
4. Pergolas and benches
5. Flower beds and shrubs
6. Labels and dimensions
