#!/usr/bin/env python3
"""CAD Helper — generate DXF files for AutoCAD.

Usage:
    python generate.py paving --width 3000 --length 20000
    python generate.py grid --width 5000 --length 8000 --tile 600x300
    python generate.py herringbone --width 3000 --length 12000 --tile 300x100
    python generate.py border --width 4000 --length 10000 --tile 300x150
"""

import argparse
import sys
from pathlib import Path


def parse_tile_size(s: str) -> tuple[float, float]:
    """Parse 'WxH' string into (width, height) tuple."""
    parts = s.lower().split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(f"Invalid tile size: {s}. Use format WxH, e.g. 600x300")
    return (float(parts[0]), float(parts[1]))


def parse_tile_list(s: str) -> list[tuple[float, float]]:
    """Parse comma-separated tile sizes: '600x600,300x300,400x200'."""
    return [parse_tile_size(part.strip()) for part in s.split(",")]


def cmd_paving(args):
    from lib.patterns.paving import create_paving
    tiles = parse_tile_list(args.tiles) if args.tiles else None
    path = create_paving(
        width=args.width,
        length=args.length,
        tiles=tiles,
        gap=args.gap,
        filled=args.filled,
        output=args.output,
    )
    print(f"Created: {path}")


def cmd_grid(args):
    from lib.patterns.grid import create_grid
    tile = parse_tile_size(args.tile) if args.tile else (600, 300)
    path = create_grid(
        width=args.width,
        length=args.length,
        tile_w=tile[0],
        tile_h=tile[1],
        gap=args.gap,
        offset_rows=args.offset,
        filled=args.filled,
        output=args.output,
    )
    print(f"Created: {path}")


def cmd_herringbone(args):
    from lib.patterns.herringbone import create_herringbone
    tile = parse_tile_size(args.tile) if args.tile else (300, 100)
    path = create_herringbone(
        width=args.width,
        length=args.length,
        tile_w=tile[0],
        tile_h=tile[1],
        gap=args.gap,
        filled=args.filled,
        output=args.output,
    )
    print(f"Created: {path}")


def cmd_border(args):
    from lib.patterns.border import create_border
    tile = parse_tile_size(args.tile) if args.tile else (300, 150)
    path = create_border(
        width=args.width,
        length=args.length,
        tile_w=tile[0],
        tile_h=tile[1],
        gap=args.gap,
        border_rows=args.rows,
        filled=args.filled,
        output=args.output,
    )
    print(f"Created: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="CAD Helper — generate DXF tile patterns for AutoCAD",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Common arguments
    def add_common_args(p):
        p.add_argument("--width", type=float, required=True, help="Area width in mm")
        p.add_argument("--length", type=float, required=True, help="Area length in mm")
        p.add_argument("--gap", type=float, default=5, help="Gap between tiles in mm (default: 5)")
        p.add_argument("--filled", action="store_true", help="Draw tiles with solid fill")
        p.add_argument("--output", "-o", type=str, default=None, help="Output DXF file path")

    # paving
    p = subparsers.add_parser("paving", help="Mixed-size paving pattern")
    add_common_args(p)
    p.add_argument("--tiles", type=str, default=None,
                   help="Tile sizes as 'WxH,WxH,...' (e.g. '600x600,300x300')")
    p.set_defaults(func=cmd_paving)

    # grid
    p = subparsers.add_parser("grid", help="Regular grid of same-sized tiles")
    add_common_args(p)
    p.add_argument("--tile", type=str, default=None, help="Tile size as WxH (default: 600x300)")
    p.add_argument("--offset", action="store_true", help="Offset alternating rows (running bond)")
    p.set_defaults(func=cmd_grid)

    # herringbone
    p = subparsers.add_parser("herringbone", help="Herringbone (елочка) pattern")
    add_common_args(p)
    p.add_argument("--tile", type=str, default=None, help="Tile size as WxH (default: 300x100)")
    p.set_defaults(func=cmd_herringbone)

    # border
    p = subparsers.add_parser("border", help="Border/frame around an area")
    add_common_args(p)
    p.add_argument("--tile", type=str, default=None, help="Border tile size as WxH (default: 300x150)")
    p.add_argument("--rows", type=int, default=1, help="Number of border rows (default: 1)")
    p.set_defaults(func=cmd_border)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
