"""Config flow for Frosted Glass Theme Manager integration."""
import voluptuous as vol
import logging

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
    DEFAULT_LIGHT_RGB,
    DEFAULT_DARK_RGB,
    DEFAULT_LIGHT_BG_URL,
    DEFAULT_DARK_BG_URL,
)

_LOGGER = logging.getLogger(__name__)

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
        # OPRAVA: Premenujeme premennú, aby sme nekolidovali s internou property HA
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # === OPRAVA RESET LOGIKY ===
            if user_input.get(CONF_RESET):
                
                def str_to_list(rgb_str):
                    try:
                        return [int(x) for x in rgb_str.split(", ")]
                    except ValueError:
                        return [106, 116, 211] 

                user_input[CONF_LIGHT_PRIMARY] = str_to_list(DEFAULT_LIGHT_RGB)
                user_input[CONF_LIGHT_BG] = DEFAULT_LIGHT_BG_URL
                user_input[CONF_DARK_PRIMARY] = str_to_list(DEFAULT_DARK_RGB)
                user_input[CONF_DARK_BG] = DEFAULT_DARK_BG_URL
                
                user_input[CONF_RESET] = False

            return self.async_create_entry(title="", data=user_input)

        def ensure_rgb_list(rgb_val, default_str):
            if isinstance(rgb_val, (list, tuple)):
                return list(rgb_val)
            if isinstance(rgb_val, str):
                try:
                    return [int(x) for x in rgb_val.split(", ")]
                except ValueError:
                    pass
            return [int(x) for x in default_str.split(", ")]

        # OPRAVA: Používame self._config_entry namiesto self.config_entry
        val_light_prim = self._config_entry.options.get(CONF_LIGHT_PRIMARY, DEFAULT_LIGHT_RGB)
        val_light_bg = self._config_entry.options.get(CONF_LIGHT_BG, DEFAULT_LIGHT_BG_URL)
        val_dark_prim = self._config_entry.options.get(CONF_DARK_PRIMARY, DEFAULT_DARK_RGB)
        val_dark_bg = self._config_entry.options.get(CONF_DARK_BG, DEFAULT_DARK_BG_URL)

        schema = vol.Schema(
            {
                vol.Optional(CONF_RESET, default=False): bool,
                
                vol.Required(
                    CONF_LIGHT_PRIMARY,
                    default=ensure_rgb_list(val_light_prim, DEFAULT_LIGHT_RGB)
                ): selector.ColorRGBSelector(),
                
                vol.Required(
                    CONF_LIGHT_BG,
                    default=val_light_bg
                ): selector.TextSelector(),
                
                vol.Required(
                    CONF_DARK_PRIMARY,
                    default=ensure_rgb_list(val_dark_prim, DEFAULT_DARK_RGB)
                ): selector.ColorRGBSelector(),
                
                vol.Required(
                    CONF_DARK_BG,
                    default=val_dark_bg
                ): selector.TextSelector(),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema
        )
