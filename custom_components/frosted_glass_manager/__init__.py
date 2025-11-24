"""The Frosted Glass Theme Manager integration."""
import os
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_LIGHT_PRIMARY,
    CONF_LIGHT_BG,
    CONF_DARK_PRIMARY,
    CONF_DARK_BG,
    CONF_RESET,
    DEFAULT_LIGHT_RGB,
    DEFAULT_DARK_RGB,
    DEFAULT_LIGHT_BG_URL,
    DEFAULT_DARK_BG_URL,
    THEME_TEMPLATE,
    THEME_FILENAME,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Frosted Glass Theme Manager from a config entry."""
    entry.async_on_unload(entry.add_update_listener(update_listener))
    await hass.async_add_executor_job(generate_theme_file, hass, entry)
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    await hass.async_add_executor_job(generate_theme_file, hass, entry)
    await hass.services.async_call("frontend", "reload_themes", {})

def generate_theme_file(hass: HomeAssistant, entry: ConfigEntry):
    """Generate the theme YAML file based on options."""
    options = entry.options

    # Defaults
    def_light_rgb = DEFAULT_LIGHT_RGB
    def_dark_rgb = DEFAULT_DARK_RGB

    if options.get(CONF_RESET, False):
        new_light_primary = def_light_rgb
        new_light_bg = DEFAULT_LIGHT_BG_URL
        new_dark_primary = def_dark_rgb
        new_dark_bg = DEFAULT_DARK_BG_URL
    else:
        # Helper to convert list back to "R, G, B" string
        def get_rgb_string(conf_key, default_val):
            val = options.get(conf_key, default_val)
            if isinstance(val, list) or isinstance(val, tuple):
                return f"{val[0]}, {val[1]}, {val[2]}"
            return val # It's already a string

        new_light_primary = get_rgb_string(CONF_LIGHT_PRIMARY, def_light_rgb)
        new_light_bg = options.get(CONF_LIGHT_BG, DEFAULT_LIGHT_BG_URL)
        new_dark_primary = get_rgb_string(CONF_DARK_PRIMARY, def_dark_rgb)
        new_dark_bg = options.get(CONF_DARK_BG, DEFAULT_DARK_BG_URL)

    content = THEME_TEMPLATE
    
    # ---------------------------------------------------------
    # SPLIT LOGIC
    # ---------------------------------------------------------
    # We look for "    dark:" (4 spaces indentation). 
    # Ensure const.py matches this EXACTLY.
    split_marker = "    dark:"
    
    if split_marker not in content:
        _LOGGER.error(f"Frosted Glass Manager: CRITICAL ERROR - Split marker '{split_marker}' not found in template. Theme not generated.")
        return

    parts = content.split(split_marker)
    
    if len(parts) < 2:
        _LOGGER.error("Frosted Glass Manager: Parsing failed, could not separate Light and Dark modes.")
        return

    # parts[0] is everything before '    dark:' (The Light Mode)
    # parts[1] is everything after. We must add the marker back to start of dark part.
    
    light_part = parts[0]
    # Reconstruct dark part ensuring the marker is present
    dark_part = split_marker + "".join(parts[1:])

    # --- REPLACE LIGHT ---
    # Replace the default placeholder with user value
    light_part = light_part.replace(def_light_rgb, new_light_primary)
    light_part = light_part.replace(DEFAULT_LIGHT_BG_URL, new_light_bg)

    # --- REPLACE DARK ---
    # Replace the default placeholder with user value
    dark_part = dark_part.replace(def_dark_rgb, new_dark_primary)
    dark_part = dark_part.replace(DEFAULT_DARK_BG_URL, new_dark_bg)

    # Reassemble
    final_content = light_part + dark_part

    # Write file
    try:
        themes_dir = hass.config.path("themes")
        if not os.path.isdir(themes_dir):
            os.mkdir(themes_dir)

        file_path = os.path.join(themes_dir, THEME_FILENAME)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_content)
            
        _LOGGER.info(f"Frosted Glass theme successfully generated at {file_path}")
        
    except Exception as e:
        _LOGGER.error(f"Frosted Glass Manager: Error writing theme file: {e}")

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
