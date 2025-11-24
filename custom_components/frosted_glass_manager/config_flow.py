"""Config flow for Frosted Glass Theme Manager integration."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

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
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Frosted Glass Theme Manager."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Frosted Glass Manager", data={})

        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Helper to convert "R, G, B" string to [R, G, B] list for the selector
        def str_rgb_to_list(rgb_str):
            try:
                return [int(x) for x in rgb_str.split(", ")]
            except ValueError:
                return [106, 116, 211] # Default fallback

        # Get current values or defaults
        current_light_primary = self.config_entry.options.get(CONF_LIGHT_PRIMARY, DEFAULT_PRIMARY_RGB)
        current_light_bg = self.config_entry.options.get(CONF_LIGHT_BG, DEFAULT_LIGHT_BG_URL)
        current_dark_primary = self.config_entry.options.get(CONF_DARK_PRIMARY, DEFAULT_PRIMARY_RGB)
        current_dark_bg = self.config_entry.options.get(CONF_DARK_BG, DEFAULT_DARK_BG_URL)

        schema = vol.Schema(
            {
                vol.Optional(CONF_RESET, default=False): bool,
                
                vol.Required(
                    CONF_LIGHT_PRIMARY,
                    default=str_rgb_to_list(current_light_primary)
                ): selector.ColorRGBSelector(),
                
                vol.Required(
                    CONF_LIGHT_BG,
                    default=current_light_bg
                ): selector.TextSelector(),
                
                vol.Required(
                    CONF_DARK_PRIMARY,
                    default=str_rgb_to_list(current_dark_primary)
                ): selector.ColorRGBSelector(),
                
                vol.Required(
                    CONF_DARK_BG,
                    default=current_dark_bg
                ): selector.TextSelector(),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema
        )
