"""Constants for the Frosted Glass Theme Manager integration."""

from pathlib import Path

from .theme_generator import (
    DEFAULT_DARK_BG_URL,
    DEFAULT_DARK_RGB,
    DEFAULT_LIGHT_BG_URL,
    DEFAULT_LIGHT_RGB,
)

__all__ = [
    "DEFAULT_DARK_BG_URL",
    "DEFAULT_DARK_RGB",
    "DEFAULT_LIGHT_BG_URL",
    "DEFAULT_LIGHT_RGB",
]


DOMAIN = "frosted_glass_manager"

CONF_LIGHT_PRIMARY = "light_primary_color"
CONF_LIGHT_BG = "light_background_url"
CONF_DARK_PRIMARY = "dark_primary_color"
CONF_DARK_BG = "dark_background_url"
CONF_RESET = "reset_defaults"

THEME_FILENAME = "Frosted Glass Custom.yaml"
LITE_THEME_FILENAME = "Frosted Glass Custom Lite.yaml"

_TEMPLATE_DIR = Path(__file__).parent / "templates"
THEME_TEMPLATE_PATH = _TEMPLATE_DIR / "frosted_glass.yaml"
LITE_THEME_TEMPLATE_PATH = _TEMPLATE_DIR / "frosted_glass_lite.yaml"
