"""Every example project builds, passes its own checks and survives a DXF round trip."""

from pathlib import Path

import ezdxf
import pytest

from cad_helper.checks import check_document
from cad_helper.cli import _load_module

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = sorted(p.parent.name for p in (ROOT / "projects").glob("*/build.py"))


def test_projects_found():
    assert len(PROJECTS) >= 4


@pytest.mark.parametrize("name", PROJECTS)
def test_project_builds_clean(name, tmp_path):
    module = _load_module(ROOT / "projects" / name / "build.py")
    doc = module.build()
    issues = check_document(
        doc,
        bounds=getattr(module, "BOUNDS", None),
        clearances=getattr(module, "CLEARANCES", ()),
        plot_scale=getattr(module, "PLOT_SCALE", 100),
    )
    assert [str(i) for i in issues if i.level == "error"] == []

    out = tmp_path / f"{name}.dxf"
    doc.saveas(out)
    reread = ezdxf.readfile(out)
    assert len(reread.modelspace()) == len(doc.modelspace())
    assert reread.units == ezdxf.units.MM
