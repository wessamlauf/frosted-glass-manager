# Frosted Glass UIX Theme Manager

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-41BDF5?logo=home-assistant&logoColor=white)](https://github.com/hacs/integration)
[![Home Assistant](https://img.shields.io/badge/home%20assistant-%2341BDF5.svg)](https://www.home-assistant.io/)
[![Maintainer](https://img.shields.io/badge/maintainer-wessamlauf-blue)](https://github.com/wessamlauf)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-☕-orange?logo=buymeacoffee&logoColor=white)](https://www.buymeacoffee.com/wessamlauf)

[![Open your Home Assistant instance and add this repository to HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=rockbaer2007&repository=frosted-glass-manager&category=integration)

<img alt="Frosted Glass Manager logo" src="https://github.com/user-attachments/assets/f1fd71d5-f5bb-451e-862c-cc668d987f66" />

### Private UIX experiment based on Frosted Glass Theme Manager.

**Frosted Glass UIX Theme Manager** is a local test branch that explores whether the Frosted Glass Manager concept can generate themes for UIX instead of card-mod.

This branch is not an official upstream release. The upstream manager repository currently has no recognized license in GitHub metadata, so keep this branch private/local unless permission or a clear upstream license is available.

Original projects:
- Frosted Glass Theme Manager: https://github.com/wessamlauf/frosted-glass-manager
- Frosted Glass Themes: https://github.com/wessamlauf/homeassistant-frosted-glass-themes

## ✨ Features

- **UI Color Picker**: Change the **Primary Color** for both Light and Dark modes using a visual picker. No more editing code! 🎨
- **Smart Tonal Palette**: This isn't just a simple color swap. The manager mathematically calculates a complete **Material Design tonal palette** (shades 05–95) based on your chosen color. This ensures text remains readable and contrast stays perfect. 🧠
- **Custom Backgrounds**: Easily paste a URL for your custom background images. 🖼️
- **Bundled Backgrounds**: The default light and dark backgrounds are copied locally to Home Assistant's `/local/frosted-glass-uix/` path.
- **Dual Generation**: With a single click, the manager generates two themes:
    1.  **Frosted Glass UIX Custom**: The full UIX experiment with blur and glass effects.
    2.  **Frosted Glass UIX Custom Lite**: A performance-optimized UIX experiment for older devices.
- **Instant Updates**: Changes are applied immediately without needing to restart Home Assistant. 🚀

---

## 🚀 Installation Guide

**Step 1: Prerequisites**
- You must have [HACS](https://hacs.xyz/) installed.
- You must have UIX installed and loaded in Home Assistant.

**Step 2: Install via HACS**
1. Open HACS -> Integrations.
2. Click the menu (three dots) in the top right -> **Custom repositories**.
3. Paste this repository URL: `https://github.com/rockbaer2007/frosted-glass-manager`
4. Select Category: **Integration**.
5. Click **Add**, then find **Frosted Glass UIX Theme Manager** in the list and install it.
6. **Restart Home Assistant.**

**Step 3: Install Manually (Alternative)**
1. Download this repository.
2. Copy the `custom_components/frosted_glass_uix_manager` folder into your `config/custom_components/` directory.
3. Restart Home Assistant.

---

## ⚙️ Usage & Configuration

Once installed and restarted, you need to add the integration to your instance:

1. Go to **Settings** -> **Devices & Services**.
2. Click **Add Integration** (bottom right).
3. Search for **"Frosted Glass UIX Theme Manager"**.
4. Finish the setup.

### How to Customize:
1. Find the integration in your list and click **CONFIGURE**.
2. You will see a form where you can set:
    * **Light Mode Primary Color** ☀️
    * **Light Mode Background URL**
    * **Dark Mode Primary Color** 🌑
    * **Dark Mode Background URL**
3. Click **SUBMIT**.

The integration will automatically generate two new files in your `themes/` folder: `Frosted Glass UIX Custom.yaml` and `Frosted Glass UIX Custom Lite.yaml`.

The bundled default backgrounds are copied to:

- `config/www/frosted-glass-uix/frosted-glass-light-background.jpg`
- `config/www/frosted-glass-uix/frosted-glass-dark-background.jpg`

The generated theme uses these local URLs by default:

- `/local/frosted-glass-uix/frosted-glass-light-background.jpg`
- `/local/frosted-glass-uix/frosted-glass-dark-background.jpg`

### Activating the Theme:
1. Go to your **Profile** (click your name in the bottom-left corner).
2. Under **Theme**, select either **Frosted Glass UIX Custom** or **Frosted Glass UIX Custom Lite**.

---

## 🔄 Reset to Defaults

Want to go back to the original "Blurple/Blue" look?
1. Open the integration configuration.
2. Check the box: **RESET to Defaults**.
3. Click **Submit**.

Everything will revert to the original Frosted Glass color scheme.

-----

## 🖼️ **Screenshots** (color picker/custom color/custom background)

![Untitled design (1)](https://github.com/user-attachments/assets/d5d228e9-1051-4785-a804-5cf97b0d3188)

<img alt="image" src="https://github.com/user-attachments/assets/dd595745-66ab-41a1-ae71-cc80967ea838" />

---

## ❤️ Support the Project
If this tool helped you make your dashboard beautiful and saved you time, consider buying me a coffee!

<a href="https://www.buymeacoffee.com/wessamlauf" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

---

## 🐞 Issues / Feedback

Found a bug or have a suggestion in the original manager?
Open an [issue](https://github.com/wessamlauf/frosted-glass-manager/issues) on GitHub.

For this UIX experiment, validate locally first before opening upstream issues.

*This integration is based on the visual design of the [Frosted Glass Themes](https://github.com/wessamlauf/homeassistant-frosted-glass-themes).*
