"""The Frosted Glass Manager integration."""
import logging
import os

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, THEME_TEMPLATE, THEME_FILENAME

_LOGGER = logging.getLogger(__name__)

def hex_to_rgb_string(hex_color):
    """Converts HEX (#RRGGBB) to 'R, G, B' string."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return "106, 116, 211" # Fallback default
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"{r}, {g}, {b}"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    
    # Listen for updates
    entry.async_on_unload(entry.add_update_listener(update_theme_listener))
    
    # Initial generation
    await async_update_theme_file(hass, entry)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True

async def update_theme_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    await async_update_theme_file(hass, entry)

async def async_update_theme_file(hass: HomeAssistant, entry: ConfigEntry):
    """Generate the theme YAML file and reload themes."""
    
    primary_hex = entry.options.get("primary_color", "#6A74D3")
    accent_hex = entry.options.get("accent_color", "#6A74D3")
    
    primary_rgb = hex_to_rgb_string(primary_hex)
    accent_rgb = hex_to_rgb_string(accent_hex)
    
    _LOGGER.info(f"Updating Frosted Glass Theme with Primary: {primary_hex} ({primary_rgb})")

    # Replace placeholders with actual values
    theme_content = THEME_TEMPLATE.replace(
        "__PRIMARY_RGB__", primary_rgb
    ).replace(
        "__PRIMARY_HEX__", primary_hex
    ).replace(
        "__ACCENT_RGB__", accent_rgb
    ).replace(
        "__ACCENT_HEX__", accent_hex
    )
    
    themes_dir = hass.config.path("themes")
    file_path = os.path.join(themes_dir, THEME_FILENAME)
    
    if not os.path.exists(themes_dir):
        os.makedirs(themes_dir)

    def _write_file():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(theme_content)

    await hass.async_add_executor_job(_write_file)
    
    await hass.services.async_call("frontend", "reload_themes")
