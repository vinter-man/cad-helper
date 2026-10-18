import pytest

from cad_helper.checks import Clearance, check_document
from cad_helper.core import create_document
from cad_helper.planting import draw_tree
from cad_helper.site import draw_house
from cad_helper.water import draw_pond


def site(pond_x: float):
    doc = create_document()
    msp = doc.modelspace()
    draw_house(msp, doc, x=10_000, y=10_000, w=8_000, h=6_000)
    draw_pond(msp, doc, cx=pond_x, cy=13_000, rx=2_000, ry=1_500, irregular=False)
    return doc


def errors(issues, check):
    return [i for i in issues if i.level == "error" and i.check == check]


def test_clean_drawing_passes():
    issues = check_document(
        site(4_000), bounds=(0, 0, 25_000, 25_000), clearances=[Clearance("HOUSE", "POND*", 3_000)]
    )
    assert not [i for i in issues if i.level == "error"]


@pytest.mark.parametrize(("pond_x", "expected_gap"), [(7_000, 1_000), (11_000, 0)])
def test_clearance_measures_real_distance(pond_x, expected_gap):
    issues = check_document(site(pond_x), clearances=[Clearance("HOUSE", "POND", 3_000)])
    (issue,) = errors(issues, "clearance")
    assert f"is {expected_gap} mm" in issue.message


def test_bounds_catches_elements_outside_the_site():
    doc = create_document()
    msp = doc.modelspace()
    draw_tree(msp, doc, cx=500, cy=5_000, crown_diameter=3_000)  # crown crosses x = 0
    (issue,) = errors(check_document(doc, bounds=(0, 0, 10_000, 10_000)), "bounds")
    assert "TREES" in issue.message


def test_layer_zero_and_small_text_are_warned():
    doc = create_document()
    msp = doc.modelspace()
    msp.add_line((0, 0), (1, 1))
    msp.add_text("tiny", height=20, dxfattribs={"layer": "LABELS"})
    checks = {i.check for i in check_document(doc) if i.level == "warning"}
    assert {"layers", "text"} <= checks


def test_missing_layer_in_rule_is_reported():
    issues = check_document(site(4_000), clearances=[Clearance("HOUSE", "BBQ", 3_000)])
    assert any("no geometry on BBQ" in i.message for i in issues)
