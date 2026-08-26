"""Tests for the standalone Frosted Glass theme renderer."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT / "custom_components" / "frosted_glass_manager" / "theme_generator.py"
)
SPEC = importlib.util.spec_from_file_location(
    "frosted_glass_theme_generator", MODULE_PATH
)
assert SPEC and SPEC.loader
GENERATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = GENERATOR
SPEC.loader.exec_module(GENERATOR)


def _template(name: str) -> str:
    return (
        ROOT / "custom_components" / "frosted_glass_manager" / "templates" / name
    ).read_text(encoding="utf-8")


def test_normalize_rgb_rejects_malformed_and_out_of_range_values() -> None:
    assert GENERATOR.normalize_rgb("1,2,3") == "1, 2, 3"
    assert GENERATOR.normalize_rgb([4, 5, 6]) == "4, 5, 6"
    assert GENERATOR.normalize_rgb("256, 0, 0") == GENERATOR.DEFAULT_LIGHT_RGB
    assert GENERATOR.normalize_rgb("1, 2") == GENERATOR.DEFAULT_LIGHT_RGB


def test_rendered_full_theme_is_self_contained() -> None:
    settings = GENERATOR.ThemeSettings(
        light_primary="12, 34, 56",
        light_background="https://example.com/light.jpg",
        dark_primary="78, 90, 123",
        dark_background="https://example.com/dark.jpg",
    )
    rendered = GENERATOR.render_theme(_template("frosted_glass.yaml"), settings)
    themes = yaml.safe_load(rendered)

    assert set(themes) == {
        "Frosted Glass Custom",
        "Frosted Glass Custom Light",
        "Frosted Glass Custom Dark",
    }
    combined = themes["Frosted Glass Custom"]
    assert combined["modes"]["light"]["card-mod-theme"] == "Frosted Glass Custom Light"
    assert combined["modes"]["dark"]["uix-theme"] == "Frosted Glass Custom Dark"
    assert (
        "https://example.com/light.jpg"
        in combined["modes"]["light"]["background-image"]
    )
    assert (
        "https://example.com/dark.jpg" in combined["modes"]["dark"]["background-image"]
    )
    assert combined["modes"]["light"]["primary-color"] == "rgb(12, 34, 56)"
    assert combined["modes"]["dark"]["primary-color"] == "rgb(78, 90, 123)"

    for mode, engine_name in (
        ("light", "Frosted Glass Custom Light"),
        ("dark", "Frosted Glass Custom Dark"),
    ):
        engine = themes[engine_name]
        assert engine["card-mod-theme"] == engine_name
        assert engine["uix-theme"] == engine_name
        assert engine["modes"][mode]
        assert "card-mod-card" in engine
        assert "card-mod-root" in engine


def test_lite_theme_omits_backdrop_filter() -> None:
    rendered = GENERATOR.render_theme(
        _template("frosted_glass_lite.yaml"), GENERATOR.ThemeSettings()
    )
    themes = yaml.safe_load(rendered)
    light_engine = themes["Frosted Glass Custom Light Lite"]
    assert "backdrop-filter:" not in light_engine["card-mod-card"]


def test_embedded_css_has_balanced_rules_and_no_yaml_comments() -> None:
    for template_name in ("frosted_glass.yaml", "frosted_glass_lite.yaml"):
        themes = yaml.safe_load(
            GENERATOR.render_theme(_template(template_name), GENERATOR.ThemeSettings())
        )
        for theme in themes.values():
            sections = [theme]
            if "modes" in theme:
                sections.extend(theme["modes"].values())
            for section in sections:
                for key, value in section.items():
                    if not key.startswith("card-mod-") or key == "card-mod-theme":
                        continue
                    css = re.sub(r"/\*.*?\*/", "", value, flags=re.DOTALL)
                    assert not re.search(r"^\s*#|;\s+#", css, flags=re.MULTILINE)
                    assert css.count("{") == css.count("}")


def test_render_and_write_themes_creates_directory_atomically(tmp_path: Path) -> None:
    themes_dir = tmp_path / "themes"
    written = GENERATOR.render_and_write_themes(
        themes_dir,
        {
            "Frosted Glass Custom.yaml": ROOT
            / "custom_components"
            / "frosted_glass_manager"
            / "templates"
            / "frosted_glass.yaml"
        },
        GENERATOR.ThemeSettings(),
    )
    assert written == (themes_dir / "Frosted Glass Custom.yaml",)
    assert yaml.safe_load(written[0].read_text(encoding="utf-8"))
    assert not list(themes_dir.glob("*.tmp"))
