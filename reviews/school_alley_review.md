# Review: School Alley

## Build Verification
- [x] Script runs without errors
- [x] Output: 3835 entities, 13 layers
- [x] DXF file generated at `projects/school_alley/school_alley.dxf`

## Geometry Checks
- [x] Alley boundary: 0..50000 x 0..3000 mm — correct (3m x 50m)
- [x] Curbs: 150mm on both sides, split at pocket openings
- [x] West pocket: X=1000..5000, Y=-3500..0 — extends south, correct
- [x] East pocket: X=45000..49000, Y=3000..6500 — extends north, correct
- [x] No overlapping structures (pockets at opposite ends and sides)
- [x] Pocket curbs wrap around 3 open sides (opening toward alley is seamless)

## Tile Composition
- [x] All 5 tile sizes used: 100x100, 300x150, 300x300, 450x300, 600x300
- [x] Edge bands: 100x100 tiles (dark grey, ACI 250) — 2 rows each side
- [x] Transition bands: 300x150 tiles (medium grey, ACI 252) — 3 rows each side
- [x] Center band: mixed 600x300, 450x300, 300x300 (light grey, ACI 254) — 5 rows
- [x] Gradient: dark edges → light center — achieved via ACI colors
- [x] Row offset (brick pattern): alternating rows offset for dynamic effect
- [x] 5mm gaps between tiles
- [x] Pocket paving: 300x300 tiles (ACI 253)

## Seating Pockets
- [x] West pocket: pergola (3500x3000) + 2 benches — correct
- [x] East pocket: pergola (3500x3000) + 2 benches — correct
- [x] 3 shrubs per pocket (Spiraea flanking, Berberis at back)
- [x] Pockets are on opposite sides for visual asymmetry

## Flower Beds
- [x] LAVANDULA bed: south side, X=6000..9000
- [x] MIXBORDER (south): X=21000..26000
- [x] MIXBORDER (north): X=23000..28000
- [x] ROSES & GRASSES: north side, X=40000..43000
- [x] Round accent bed: center north, diameter 2000mm
- [x] No flower beds overlap with pockets or alley

## Practical Checks
- [x] Alley is walkable end-to-end (no obstructions on paving)
- [x] Flower beds are OUTSIDE the alley (south/north of curbs)
- [x] Shrubs are outside pocket boundaries
- [x] Pergolas are inside pocket boundaries
- [x] Benches are under pergolas (sheltered)

## Layer Organization
- [x] CURB (8) — curbs and alley outline
- [x] TILE_DARK (250) — edge tiles
- [x] TILE_MID (252) — transition tiles
- [x] TILE_LIGHT (254) — center tiles
- [x] TILE_POCKET (253) — pocket paving
- [x] PERGOLA (33) — pergolas
- [x] FURNITURE (6) — benches
- [x] SHRUBS (3) — shrubs
- [x] FLOWER_BEDS (200) — flower beds
- [x] LABELS (7) — text

## Result: PASS
All checks passed. Ready for delivery.
