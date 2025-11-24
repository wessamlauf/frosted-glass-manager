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
    DEFAULT_PRIMARY_RGB,
    DEFAULT_LIGHT_BG_URL,
    DEFAULT_DARK_BG_URL,
    THEME_TEMPLATE,
    THEME_FILENAME,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Frosted Glass Theme Manager from a config entry."""
    
    # Register update listener
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    # Generate the theme on startup
    await hass.async_add_executor_job(generate_theme_file, hass, entry)
    
    return True

async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    await hass.async_add_executor_job(generate_theme_file, hass, entry)
    
    # Reload themes to apply changes immediately
    await hass.services.async_call("frontend", "reload_themes", {})

def generate_theme_file(hass: HomeAssistant, entry: ConfigEntry):
    """Generate the theme YAML file based on options."""
    options = entry.options

    # Check for Reset
    if options.get(CONF_RESET, False):
        new_light_primary = DEFAULT_PRIMARY_RGB
        new_light_bg = DEFAULT_LIGHT_BG_URL
        new_dark_primary = DEFAULT_PRIMARY_RGB
        new_dark_bg = DEFAULT_DARK_BG_URL
    else:
        # Get values from options or fallback to default
        # RGB Selector returns [R, G, B], we need "R, G, B" string
        
        # LIGHT
        opt_light_prim = options.get(CONF_LIGHT_PRIMARY, [106, 116, 211])
        # Handle case where it might be stored as string or list
        if isinstance(opt_light_prim, str):
             new_light_primary = opt_light_prim
        else:
             new_light_primary = f"{opt_light_prim[0]}, {opt_light_prim[1]}, {opt_light_prim[2]}"
             
        new_light_bg = options.get(CONF_LIGHT_BG, DEFAULT_LIGHT_BG_URL)
        
        # DARK
        opt_dark_prim = options.get(CONF_DARK_PRIMARY, [106, 116, 211])
        if isinstance(opt_dark_prim, str):
             new_dark_primary = opt_dark_prim
        else:
             new_dark_primary = f"{opt_dark_prim[0]}, {opt_dark_prim[1]}, {opt_dark_prim[2]}"
             
        new_dark_bg = options.get(CONF_DARK_BG, DEFAULT_DARK_BG_URL)

    # Prepare content
    content = THEME_TEMPLATE

    # ---------------------------------------------------------
    # GLOBAL REPLACEMENT STRATEGY
    # ---------------------------------------------------------
    # The theme uses the default RGB string "106, 116, 211" extensively.
    # We must replace it in two passes (Light section and Dark section).
    # Since the template is one big string, we split it by modes to avoid
    # Dark settings overwriting Light settings if they differ.
    
    # Find the split point (simple approximation based on indentation/comments)
    split_marker = "    dark:"
    parts = content.split(split_marker)
    
    if len(parts) != 2:
        _LOGGER.error("Could not parse theme template correctly. Structure might be changed.")
        return

    light_part = parts[0]
    dark_part = split_marker + parts[1]

    # --- APPLY LIGHT SETTINGS ---
    # Replace Primary Color everywhere in the Light section
    light_part = light_part.replace(DEFAULT_PRIMARY_RGB, new_light_primary)
    # Replace Background URL
    light_part = light_part.replace(DEFAULT_LIGHT_BG_URL, new_light_bg)

    # --- APPLY DARK SETTINGS ---
    # Replace Primary Color everywhere in the Dark section
    # Note: The default primary is the same for both, so we replace the same string
    dark_part = dark_part.replace(DEFAULT_PRIMARY_RGB, new_dark_primary)
    # Replace Background URL
    dark_part = dark_part.replace(DEFAULT_DARK_BG_URL, new_dark_bg)

    # Reassemble
    final_content = light_part + dark_part

    # Write to file
    themes_dir = hass.config.path("themes")
    if not os.path.isdir(themes_dir):
        os.mkdir(themes_dir)

    file_path = os.path.join(themes_dir, THEME_FILENAME)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    _LOGGER.info(f"Frosted Glass theme generated at {file_path}")

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
