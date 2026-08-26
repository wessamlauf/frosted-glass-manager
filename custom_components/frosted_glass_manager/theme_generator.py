"""Pure helpers for rendering and writing Frosted Glass themes."""

from __future__ import annotations

import colorsys
import os
import re
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path


DEFAULT_LIGHT_RGB = "106, 116, 211"
DEFAULT_DARK_RGB = "106, 116, 211"

DEFAULT_PALETTE = {
    "05": "#0D0E19",
    "10": "#131526",
    "20": "#20233F",
    "30": "#30345F",
    "40": "#40467F",
    "50": "#6A74D3",
    "60": "#8F97DE",
    "70": "#ADB3E7",
    "80": "#D2D5F2",
    "90": "#EAECF9",
    "95": "#F6F7FC",
}

DEFAULT_LIGHT_BG_URL = "https://cdn.jsdelivr.net/gh/wessamlauf/homeassistant-frosted-glass-themes@refs/heads/main/themes/frosted-glass-light-background.jpg"
DEFAULT_DARK_BG_URL = "https://cdn.jsdelivr.net/gh/wessamlauf/homeassistant-frosted-glass-themes@refs/heads/main/themes/frosted-glass-dark-background.jpg"


@dataclass(frozen=True)
class ThemeSettings:
    """Normalized settings used to render both generated theme files."""

    light_primary: str = DEFAULT_LIGHT_RGB
    light_background: str = DEFAULT_LIGHT_BG_URL
    dark_primary: str = DEFAULT_DARK_RGB
    dark_background: str = DEFAULT_DARK_BG_URL


def normalize_rgb(
    value: str | Sequence[int] | None, fallback: str = DEFAULT_LIGHT_RGB
) -> str:
    """Return an RGB value as a validated, normalized comma-separated string."""
    if isinstance(value, str):
        parts = [part.strip() for part in value.split(",")]
    elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        parts = list(value)
    else:
        parts = []

    try:
        channels = [int(part) for part in parts]
    except (TypeError, ValueError):
        channels = []

    if len(channels) != 3 or any(channel < 0 or channel > 255 for channel in channels):
        return (
            normalize_rgb(fallback, DEFAULT_LIGHT_RGB)
            if fallback != value
            else DEFAULT_LIGHT_RGB
        )
    return ", ".join(str(channel) for channel in channels)


def generate_hex_palette(rgb_value: str | Sequence[int]) -> dict[str, str]:
    """Generate the Material-style tonal palette used by the theme templates."""
    rgb = normalize_rgb(rgb_value)
    red, green, blue = (int(channel) for channel in rgb.split(", "))
    hue, lightness, saturation = colorsys.rgb_to_hls(
        red / 255.0, green / 255.0, blue / 255.0
    )
    lightness_levels = {
        "05": 0.05,
        "10": 0.10,
        "20": 0.20,
        "30": 0.30,
        "40": 0.40,
        "50": lightness,
        "60": 0.60,
        "70": 0.70,
        "80": 0.80,
        "90": 0.90,
        "95": 0.96,
    }

    palette = {}
    for level, target_lightness in lightness_levels.items():
        new_red, new_green, new_blue = colorsys.hls_to_rgb(
            hue, target_lightness, saturation
        )
        channels = (
            max(0, min(255, int(new_red * 255))),
            max(0, min(255, int(new_green * 255))),
            max(0, min(255, int(new_blue * 255))),
        )
        palette[level] = "#{:02X}{:02X}{:02X}".format(*channels)
    return palette


def _replace_mode_values(
    content: str,
    default_rgb: str,
    primary: str,
    default_background: str,
    background: str,
) -> str:
    result = content.replace(default_rgb, primary).replace(
        default_background, background
    )
    palette = generate_hex_palette(primary)
    for level, old_hex in DEFAULT_PALETTE.items():
        result = result.replace(old_hex, palette[level])
    return result


def _extract_mode_body(content: str, mode: str) -> str:
    marker = f"    {mode}:\n"
    start = content.index(marker) + len(marker)
    end = content.index("\n    dark:\n", start) if mode == "light" else len(content)
    return content[start:end].rstrip()


def _render_engine_theme(combined: str, mode: str) -> str:
    block = _extract_mode_body(combined, mode)
    engine_match = re.search(
        r"^      card-mod-theme:\s*['\"]([^'\"]+)['\"]", block, re.MULTILINE
    )
    color_match = re.search(r"^      app-theme-color:\s*(.+)$", block, re.MULTILINE)
    if engine_match is None or color_match is None:
        raise ValueError(
            f"The {mode} template is missing its engine name or app theme color"
        )

    lines = []
    for line in block.splitlines():
        if line and not line.startswith("      "):
            raise ValueError(f"Unexpected indentation in the {mode} template: {line!r}")
        lines.append(line[4:] if line else "")

    return (
        f"{engine_match.group(1)}:\n"
        + "\n".join(lines)
        + "\n\n"
        + "  # Required by Home Assistant 2026.8; top-level values remain available to the styling engine.\n"
        + "  modes:\n"
        + f"    {mode}:\n"
        + f"      app-theme-color: {color_match.group(1)}\n"
    )


def render_theme(template: str, settings: ThemeSettings) -> str:
    """Customize a combined template and append its two styling-engine themes."""
    dark_marker = "\n    dark:\n"
    if dark_marker not in template:
        raise ValueError("Theme template does not contain a dark mode")
    light_part, dark_body = template.split(dark_marker, maxsplit=1)
    dark_part = dark_marker + dark_body

    light = _replace_mode_values(
        light_part,
        DEFAULT_LIGHT_RGB,
        normalize_rgb(settings.light_primary, DEFAULT_LIGHT_RGB),
        DEFAULT_LIGHT_BG_URL,
        settings.light_background,
    )
    dark = _replace_mode_values(
        dark_part,
        DEFAULT_DARK_RGB,
        normalize_rgb(settings.dark_primary, DEFAULT_DARK_RGB),
        DEFAULT_DARK_BG_URL,
        settings.dark_background,
    )
    combined = (light + dark).rstrip() + "\n"
    return (
        combined
        + "\n"
        + _render_engine_theme(combined, "light")
        + "\n"
        + _render_engine_theme(combined, "dark")
    )


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent, text=True
    )
    try:
        with os.fdopen(
            descriptor, "w", encoding="utf-8", newline="\n"
        ) as temporary_file:
            temporary_file.write(content)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def render_and_write_themes(
    themes_dir: Path,
    templates: Mapping[str, Path],
    settings: ThemeSettings,
) -> tuple[Path, ...]:
    """Render all templates and atomically replace their generated theme files."""
    written = []
    for output_filename, template_path in templates.items():
        template = template_path.read_text(encoding="utf-8")
        output_path = themes_dir / output_filename
        _atomic_write(output_path, render_theme(template, settings))
        written.append(output_path)
    return tuple(written)
