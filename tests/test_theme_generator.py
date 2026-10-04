"""Tests for the standalone Frosted Glass theme renderer."""

from __future__ import annotations

import colorsys
import importlib.util
import re
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, StrictUndefined

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


def test_tonal_palette_preserves_primary_and_increases_in_lightness() -> None:
    for rgb in ("122, 162, 190", "106, 116, 211", "230, 240, 250", "12, 34, 56"):
        palette = GENERATOR.generate_hex_palette(rgb)
        channels = [int(channel) for channel in rgb.split(", ")]
        assert palette["50"] == "#{:02X}{:02X}{:02X}".format(*channels)
        lightness = []
        for value in palette.values():
            red, green, blue = (int(value[i : i + 2], 16) / 255 for i in (1, 3, 5))
            lightness.append(colorsys.rgb_to_hls(red, green, blue)[1])
        assert lightness == sorted(lightness)


def test_defaults_preserve_the_template_palette_in_both_modes() -> None:
    for filename in ("frosted_glass.yaml", "frosted_glass_lite.yaml"):
        template = _template(filename)
        source = next(iter(yaml.safe_load(template).values()))
        rendered = next(
            iter(
                yaml.safe_load(
                    GENERATOR.render_theme(template, GENERATOR.ThemeSettings())
                ).values()
            )
        )
        for mode in ("light", "dark"):
            assert rendered["modes"][mode] == source["modes"][mode]
        assert rendered["modes"]["dark"]["primary-background-color"] == "rgb(2, 6, 11)"


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
    assert combined["modes"]["light"]["bubble-accent-color"] == "rgb(12, 34, 56)"
    assert combined["modes"]["dark"]["navbar-primary-color"] == "rgb(78, 90, 123)"

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
        assert "var(--ha-space-1)" in engine["ha-dialog-surface-backdrop-filter"]
        assert engine["ha-dialog-scrim-backdrop-filter"] == "none"
        card_styles = {".": engine["card-mod-card"]}
        assert "{%" not in card_styles["."]
        assert "frosted-glass-fan-spin" not in card_styles["."]
        assert "frosted-glass-light-glow" not in card_styles["."]
        assert "card-mod-sidebar" in engine
        assert "card-mod-drawer" in engine
        assert "card-mod-more-info-yaml" not in engine
        assert engine["sidebar-background-color"].endswith(", 0.10)")
        assert engine["app-header-background-color"].endswith(", 0.10)")
        assert "var(--ha-color-neutral-50)" in engine["ha-dialog-surface-background"]
        assert engine["ha-card-background"] == "transparent"
        assert engine["ha-card-glass-tint"] == "transparent"
        assert engine["bubble-pop-up-main-background-color"] == "var(--frosted-glass-popup-surface)"


def test_lite_theme_disables_backdrop_filter() -> None:
    rendered = GENERATOR.render_theme(
        _template("frosted_glass_lite.yaml"), GENERATOR.ThemeSettings()
    )
    themes = yaml.safe_load(rendered)
    for mode in ("Light", "Dark"):
        engine = themes[f"Frosted Glass Custom {mode} Lite"]
        for key in (
            "ha-card-backdrop-filter",
            "sidebar-backdrop-filter",
            "navbar-backdrop-filter",
            "frosted-glass-popup-backdrop-filter",
        ):
            assert engine[key] == "none"
        assert engine["ha-card-background"] == "transparent"
        assert engine["bubble-main-background-color"] == "transparent"
        assert engine["navbar-background-color"] == "transparent"
        assert (
            engine["frosted-glass-popup-surface"] == engine["primary-background-color"]
        )
        assert engine["bubble-pop-up-main-background-color"] == "var(--frosted-glass-popup-surface)"
        assert engine["bubble-backdrop-filter"] == "none"
        assert engine["sidebar-background-color"] == "transparent"
        assert engine["app-header-background-color"] == "transparent"
        assert engine["app-header-backdrop-filter"] == "none"
        assert "var(--ha-card-glass-inset-shadow)" in engine["frosted-glass-badge-shadow"]
        card_styles = {".": engine["card-mod-card"]}
        assert not re.search(
            r"(?<![\w-])(?:-webkit-)?backdrop-filter\s*:", card_styles["."]
        )


def test_bubble_profiles_follow_custom_accents_and_keep_round_controls() -> None:
    settings = GENERATOR.ThemeSettings(
        light_primary="12, 34, 56", dark_primary="34, 56, 178"
    )
    for filename in ("frosted_glass.yaml", "frosted_glass_lite.yaml"):
        themes = yaml.safe_load(GENERATOR.render_theme(_template(filename), settings))
        suffix = " Lite" if "lite" in filename else ""
        for mode, primary in (("Light", "12, 34, 56"), ("Dark", "34, 56, 178")):
            engine = themes[f"Frosted Glass Custom {mode}{suffix}"]
            assert engine["bubble-accent-color"] == f"rgb({primary})"
            assert engine["bubble-main-background-color"] == "transparent"
            assert engine["bubble-icon-border-radius"] == "50%"
            assert engine["bubble-sub-button-border-radius"] == "18px"


def test_background_url_is_escaped_for_css_and_yaml() -> None:
    settings = GENERATOR.ThemeSettings(
        light_primary="12, 34, 56",
        light_background='https://example.com/image.png?label=O\'Reilly&token="abc"#6A74D3',
        dark_background="https://example.com/path\\image.png",
    )
    themes = yaml.safe_load(
        GENERATOR.render_theme(_template("frosted_glass.yaml"), settings)
    )
    modes = themes["Frosted Glass Custom"]["modes"]
    assert "O\\'Reilly" in modes["light"]["background-image"]
    assert 'token="abc"' in modes["light"]["background-image"]
    assert "#6A74D3" in modes["light"]["background-image"]
    assert "path\\\\image.png" in modes["dark"]["background-image"]


def test_embedded_css_has_balanced_rules_and_no_yaml_comments() -> None:
    def check_style(value: str | dict) -> None:
        if isinstance(value, dict):
            for child in value.values():
                check_style(child)
            return
        rendered = (
            Environment(undefined=StrictUndefined)
            .from_string(value)
            .render(config={}, is_state=lambda entity, state: False)
        )
        css = re.sub(r"/\*.*?\*/", "", rendered, flags=re.DOTALL)
        assert not re.search(r"^\s*#|;\s+#", css, flags=re.MULTILINE)
        assert css.count("{") == css.count("}")

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
                    check_style(
                        yaml.safe_load(value) if key.endswith("-yaml") else value
                    )


def test_generated_styling_has_no_automatic_state_effects_or_templates() -> None:
    for name in ("frosted_glass.yaml", "frosted_glass_lite.yaml"):
        themes = yaml.safe_load(GENERATOR.render_theme(_template(name), GENERATOR.ThemeSettings()))
        for theme in themes.values():
            for section in [theme, *theme.get("modes", {}).values()]:
                for key, value in section.items():
                    if not key.startswith("card-mod-") or key == "card-mod-theme":
                        continue
                    assert "{%" not in value and "{{" not in value
                    assert "frosted-glass-fan-spin" not in value
                    assert "frosted-glass-light-glow" not in value
                assert "card-mod-row-yaml" not in section
                assert "card-mod-glance-yaml" not in section
                assert "card-mod-more-info-yaml" not in section


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
