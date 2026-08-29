# Frosted Glass UIX Theme Manager experiment

This branch is a private technical experiment for using the Frosted Glass Manager idea with UIX instead of card-mod.

## Status

- Upstream repository: https://github.com/wessamlauf/frosted-glass-manager
- Upstream theme source: https://github.com/wessamlauf/homeassistant-frosted-glass-themes
- Upstream license status: no recognized license detected in the manager repository at the time this experiment was created.
- Publication status: keep private/local unless permission or a clear upstream license is available.

## What was changed

- Integration domain changed to `frosted_glass_uix_manager`.
- Generated theme files changed to:
  - `Frosted Glass UIX Custom.yaml`
  - `Frosted Glass UIX Custom Lite.yaml`
- Generated theme names changed to:
  - `Frosted Glass UIX Custom`
  - `Frosted Glass UIX Custom Lite`
- Theme template keys were mapped from card-mod naming to UIX naming:
  - `card-mod-theme` -> `uix-theme`
  - `card-mod-card` -> `uix-card`
  - `card-mod-root` -> `uix-root`

## Test checklist

1. Install UIX in Home Assistant.
2. Copy `custom_components/frosted_glass_uix_manager` into `config/custom_components/`.
3. Restart Home Assistant.
4. Add the integration `Frosted Glass UIX Theme Manager`.
5. Configure light and dark colors/backgrounds once.
6. Check whether both generated YAML files appear in `config/themes/`.
7. Select `Frosted Glass UIX Custom` or `Frosted Glass UIX Custom Lite` in the Home Assistant profile.
8. Verify dashboard cards, sidebar, dialogs and mobile view.

Some selectors may still need UIX-specific adjustment after live testing in Home Assistant.
