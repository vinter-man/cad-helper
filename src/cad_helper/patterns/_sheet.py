"""Tile placement shared by all patterns: clipping to the area and counting full vs cut tiles."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from ezdxf.document import Drawing
from ezdxf.enums import TextEntityAlignment

from cad_helper.core import add_label, add_layer, create_document, draw_tile, rect_points, save

MIN_CUT = 20  # mm; offcuts narrower than this are not laid


@dataclass
class PatternResult:
    path: Path
    counts: dict[str, dict[str, int]]  # layer -> {"full": n, "cut": n}

    def summary(self) -> str:
        lines = [f"Created: {self.path}"]
        for layer, c in sorted(self.counts.items()):
            lines.append(f"  {layer:<16} full {c['full']:>5}   cut {c['cut']:>4}")
        return "\n".join(lines)


@dataclass
class TileSheet:
    """A rectangular area ``length`` (X) by ``width`` (Y) mm that tiles are laid into."""

    length: float
    width: float
    filled: bool = False
    doc: Drawing = field(default_factory=create_document)
    counts: Counter = field(default_factory=Counter)

    def __post_init__(self) -> None:
        self.msp = self.doc.modelspace()
        add_layer(self.doc, "BORDER", color=7)
        add_layer(self.doc, "LABELS", color=8)
        self.msp.add_lwpolyline(
            rect_points(0, 0, self.length, self.width), close=True, dxfattribs={"layer": "BORDER"}
        )

    def layer(self, name: str, color: int) -> str:
        add_layer(self.doc, name, color=color)
        return name

    def place(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        layer: str,
        clip: tuple[float, float, float, float] | None = None,
    ) -> None:
        """Lay a w x h tile at (x, y), cut at the area edge (or at ``clip`` = x0, y0, x1, y1)."""
        cx0, cy0, cx1, cy1 = clip or (0, 0, self.length, self.width)
        x0, y0 = max(x, cx0), max(y, cy0)
        x1, y1 = min(x + w, cx1), min(y + h, cy1)
        if x1 - x0 < MIN_CUT or y1 - y0 < MIN_CUT:
            return
        draw_tile(self.msp, x0, y0, x1 - x0, y1 - y0, layer=layer, filled=self.filled)
        whole = (x0, y0, x1, y1) == (x, y, x + w, y + h)
        self.counts[layer, "full" if whole else "cut"] += 1

    def finish(self, title: str, output: str | Path) -> PatternResult:
        """Write a title and tile schedule above the area and save the DXF."""
        per_layer: dict[str, dict[str, int]] = {}
        for (layer, kind), n in self.counts.items():
            per_layer.setdefault(layer, {"full": 0, "cut": 0})[kind] = n
        h = max(60, min(self.length, self.width) / 40)
        y = self.width + h * 2
        add_label(
            self.msp,
            title,
            (0, y),
            height=h * 1.4,
            layer="LABELS",
            align=TextEntityAlignment.BOTTOM_LEFT,
        )
        for layer, c in sorted(per_layer.items(), reverse=True):
            y += h * 2.4
            add_label(
                self.msp,
                f"{layer}: {c['full']} full + {c['cut']} cut",
                (0, y),
                height=h,
                layer="LABELS",
                align=TextEntityAlignment.BOTTOM_LEFT,
            )
        return PatternResult(save(self.doc, output), per_layer)
