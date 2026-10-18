"""Raster previews of a drawing (PNG), using ezdxf's drawing add-on and matplotlib.

The agent reads these images to review its own work, and they double as the
screenshots in the README.
"""

from __future__ import annotations

from pathlib import Path

import ezdxf
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from ezdxf import bbox
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.config import BackgroundPolicy, Configuration
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.document import Drawing

BACKGROUNDS = {
    "dark": "#212830",  # AutoCAD's default model space colour
    "light": "#ffffff",
}


def render_png(
    source: Drawing | str | Path,
    output: str | Path,
    *,
    theme: str = "dark",
    width_px: int = 1600,
    margin: float = 0.03,
) -> Path:
    """Render the model space of ``source`` (a document or a DXF path) to ``output``."""
    if theme not in BACKGROUNDS:
        raise ValueError(f"theme must be one of {sorted(BACKGROUNDS)}, got {theme!r}")
    doc = source if isinstance(source, Drawing) else ezdxf.readfile(source)
    msp = doc.modelspace()

    extents = bbox.extents(msp, fast=True)
    if not extents.has_data:
        raise ValueError("drawing is empty, nothing to render")
    w, h = extents.size.x, extents.size.y
    aspect = (h * (1 + 2 * margin)) / (w * (1 + 2 * margin))

    dpi = 200
    fig = plt.figure(figsize=(width_px / dpi, max(width_px * aspect, 200) / dpi), dpi=dpi)
    ax = fig.add_axes((0, 0, 1, 1))
    config = Configuration(
        background_policy=BackgroundPolicy.CUSTOM, custom_bg_color=BACKGROUNDS[theme]
    )
    backend = MatplotlibBackend(ax, adjust_figure=False)
    Frontend(RenderContext(doc), backend, config=config).draw_layout(msp, finalize=True)
    ax.set_xlim(extents.extmin.x - w * margin, extents.extmax.x + w * margin)
    ax.set_ylim(extents.extmin.y - h * margin, extents.extmax.y + h * margin)

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=dpi, facecolor=BACKGROUNDS[theme])
    plt.close(fig)
    return output
