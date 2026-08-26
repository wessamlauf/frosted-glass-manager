"""The Frosted Glass Theme Manager integration."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_DARK_BG,
    CONF_DARK_PRIMARY,
    CONF_LIGHT_BG,
    CONF_LIGHT_PRIMARY,
    CONF_RESET,
    DEFAULT_DARK_BG_URL,
    DEFAULT_DARK_RGB,
    DEFAULT_LIGHT_BG_URL,
    DEFAULT_LIGHT_RGB,
    LITE_THEME_FILENAME,
    LITE_THEME_TEMPLATE_PATH,
    THEME_FILENAME,
    THEME_TEMPLATE_PATH,
)
from .theme_generator import ThemeSettings, normalize_rgb, render_and_write_themes


_LOGGER = logging.getLogger(__name__)


def _settings_from_options(options: dict) -> ThemeSettings:
    if options.get(CONF_RESET, False):
        return ThemeSettings()
    return ThemeSettings(
        light_primary=normalize_rgb(options.get(CONF_LIGHT_PRIMARY), DEFAULT_LIGHT_RGB),
        light_background=str(options.get(CONF_LIGHT_BG) or DEFAULT_LIGHT_BG_URL),
        dark_primary=normalize_rgb(options.get(CONF_DARK_PRIMARY), DEFAULT_DARK_RGB),
        dark_background=str(options.get(CONF_DARK_BG) or DEFAULT_DARK_BG_URL),
    )


def _generate_theme_files(hass: HomeAssistant, entry: ConfigEntry) -> tuple[Path, ...]:
    return render_and_write_themes(
        Path(hass.config.path("themes")),
        {
            THEME_FILENAME: THEME_TEMPLATE_PATH,
            LITE_THEME_FILENAME: LITE_THEME_TEMPLATE_PATH,
        },
        _settings_from_options(dict(entry.options)),
    )


async def _generate_and_reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    generated = await hass.async_add_executor_job(_generate_theme_files, hass, entry)
    await hass.services.async_call("frontend", "reload_themes", {}, blocking=True)
    _LOGGER.info("Generated and loaded Frosted Glass themes: %s", generated)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Frosted Glass Theme Manager from a config entry."""
    entry.async_on_unload(entry.add_update_listener(_update_listener))
    await _generate_and_reload(hass, entry)
    return True


async def _update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Regenerate and reload themes after an options update."""
    await _generate_and_reload(hass, entry)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
