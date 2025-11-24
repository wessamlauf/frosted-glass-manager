"""The Frosted Glass Theme Manager integration."""
import os
import logging
import colorsys

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
    DEFAULT_PALETTE,
    THEME_TEMPLATE,
    THEME_FILENAME,
    LITE_THEME_TEMPLATE,
    LITE_THEME_FILENAME,
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

def generate_hex_palette(rgb_str):
    """
    Generate a tonal palette (HEX strings) based on a single RGB string.
    """
    try:
        parts = [int(x) for x in rgb_str.split(",")]
        r, g, b = parts[0], parts[1], parts[2]
    except (ValueError, IndexError):
        r, g, b = 106, 116, 211

    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    lightness_levels = {
        "05": 0.05, "10": 0.10, "20": 0.20, "30": 0.30, "40": 0.40,
        "50": l, "60": 0.60, "70": 0.70, "80": 0.80, "90": 0.90, "95": 0.96,
    }

    palette = {}
    for level, target_l in lightness_levels.items():
        new_r, new_g, new_b = colorsys.hls_to_rgb(h, target_l, s)
        new_r = max(0, min(255, int(new_r * 255)))
        new_g = max(0, min(255, int(new_g * 255)))
        new_b = max(0, min(255, int(new_b * 255)))
        palette[level] = f"#{new_r:02X}{new_g:02X}{new_b:02X}"

    return palette

def generate_theme_file(hass: HomeAssistant, entry: ConfigEntry):
    """Generate both theme YAML files based on options."""
    options = entry.options

    # Defaults
    def_light_rgb = DEFAULT_LIGHT_RGB
    def_dark_rgb = DEFAULT_DARK_RGB

    # Determine target values
    if options.get(CONF_RESET, False):
        new_light_primary = def_light_rgb
        new_light_bg = DEFAULT_LIGHT_BG_URL
        new_dark_primary = def_dark_rgb
        new_dark_bg = DEFAULT_DARK_BG_URL
    else:
        def get_rgb_string(conf_key, default_val):
            val = options.get(conf_key, default_val)
            if isinstance(val, list) or isinstance(val, tuple):
                return f"{val[0]}, {val[1]}, {val[2]}"
            return val 

        new_light_primary = get_rgb_string(CONF_LIGHT_PRIMARY, def_light_rgb)
        new_light_bg = options.get(CONF_LIGHT_BG, DEFAULT_LIGHT_BG_URL)
        new_dark_primary = get_rgb_string(CONF_DARK_PRIMARY, def_dark_rgb)
        new_dark_bg = options.get(CONF_DARK_BG, DEFAULT_DARK_BG_URL)

    # Generate Hex Palettes
    light_palette = generate_hex_palette(new_light_primary)
    dark_palette = generate_hex_palette(new_dark_primary)

    # -------------------------------------------------------------------------
    # HELPER FUNCTION TO PROCESS A SINGLE THEME
    # -------------------------------------------------------------------------
    def create_theme_file(content_template, output_filename):
        content = content_template
        
        split_marker = "    dark:"
        if split_marker not in content:
            _LOGGER.error(f"Frosted Glass Manager: CRITICAL ERROR - Split marker '{split_marker}' not found in {output_filename}.")
            return

        parts = content.split(split_marker)
        if len(parts) < 2:
            _LOGGER.error(f"Frosted Glass Manager: Parsing failed for {output_filename}.")
            return

        light_part = parts[0]
        dark_part = split_marker + "".join(parts[1:])

        # --- REPLACE LIGHT ---
        light_part = light_part.replace(def_light_rgb, new_light_primary)
        light_part = light_part.replace(DEFAULT_LIGHT_BG_URL, new_light_bg)
        for level, old_hex in DEFAULT_PALETTE.items():
            new_hex = light_palette.get(level, old_hex)
            light_part = light_part.replace(old_hex, new_hex)

        # --- REPLACE DARK ---
        dark_part = dark_part.replace(def_dark_rgb, new_dark_primary)
        dark_part = dark_part.replace(DEFAULT_DARK_BG_URL, new_dark_bg)
        for level, old_hex in DEFAULT_PALETTE.items():
            new_hex = dark_palette.get(level, old_hex)
            dark_part = dark_part.replace(old_hex, new_hex)

        final_content = light_part + dark_part

        # Write file
        try:
            themes_dir = hass.config.path("themes")
            if not os.path.isdir(themes_dir):
                os.mkdir(themes_dir)

            file_path = os.path.join(themes_dir, output_filename)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_content)
                
            _LOGGER.info(f"Frosted Glass theme successfully generated at {file_path}")
            
        except Exception as e:
            _LOGGER.error(f"Frosted Glass Manager: Error writing theme file {output_filename}: {e}")

    # -------------------------------------------------------------------------
    # EXECUTE GENERATION FOR BOTH THEMES
    # -------------------------------------------------------------------------
    
    # 1. Generate Main Theme
    create_theme_file(THEME_TEMPLATE, THEME_FILENAME)
    
    # 2. Generate Lite Theme
    create_theme_file(LITE_THEME_TEMPLATE, LITE_THEME_FILENAME)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
