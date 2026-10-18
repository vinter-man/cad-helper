from pathlib import Path

import pytest

from cad_helper.cli import main


def test_new_then_build(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["new", "Corner Garden", "--width", "12000", "--length", "18000"]) == 0
    assert Path("projects/corner_garden/build.py").exists()
    assert main(["new", "corner_garden", "--width", "1", "--length", "1"]) == 1  # no overwrite

    assert main(["build", "corner_garden"]) == 0
    out = capsys.readouterr().out
    assert "Checks: all passed" in out
    assert Path("projects/corner_garden/corner_garden.dxf").exists()
    assert Path("projects/corner_garden/preview.png").stat().st_size > 10_000


def test_tiles_command_prints_quantities(tmp_path, capsys):
    out = tmp_path / "walk.dxf"
    assert (
        main(
            [
                "tiles",
                "grid",
                "--width",
                "1500",
                "--length",
                "3000",
                "--tile",
                "600x300",
                "--offset",
                "-o",
                str(out),
            ]
        )
        == 0
    )
    printed = capsys.readouterr().out
    assert "TILE_600x300" in printed and "cut" in printed
    assert out.exists()


def test_check_command_fails_on_bounds(tmp_path, capsys):
    out = tmp_path / "walk.dxf"
    main(["tiles", "grid", "--width", "1000", "--length", "1000", "-o", str(out)])
    assert main(["check", str(out), "--bounds", "0,0,500,500"]) == 1
    assert "bounds" in capsys.readouterr().out


def test_bad_tile_size_is_rejected():
    with pytest.raises(SystemExit):
        main(["tiles", "grid", "--width", "1", "--length", "1", "--tile", "600"])


def test_layers_command(tmp_path, capsys):
    out = tmp_path / "walk.dxf"
    main(["tiles", "herringbone", "--width", "1000", "--length", "2000", "-o", str(out)])
    capsys.readouterr()
    assert main(["layers", str(out)]) == 0
    table = capsys.readouterr().out
    assert "TILE_H" in table and "TILE_V" in table and "ENTITIES" in table
