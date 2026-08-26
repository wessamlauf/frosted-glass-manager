# Frosted Glass Theme Manager 🎨

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-41BDF5?logo=home-assistant&logoColor=white)](https://github.com/hacs/integration)
[![Home Assistant](https://img.shields.io/badge/home%20assistant-%2341BDF5.svg)](https://www.home-assistant.io/)
[![Maintainer](https://img.shields.io/badge/maintainer-wessamlauf-blue)](https://github.com/wessamlauf)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-☕-orange?logo=buymeacoffee&logoColor=white)](https://www.buymeacoffee.com/wessamlauf)

<img alt="Frosted Glass Manager logo" src="https://github.com/user-attachments/assets/f1fd71d5-f5bb-451e-862c-cc668d987f66" />

### Customize your Frosted Glass experience without touching a single line of YAML. 🛠️

**Frosted Glass Theme Manager** is a powerful companion integration for Home Assistant. It allows you to easily customize the popular Frosted Glass aesthetic directly from the UI. Change colors, switch backgrounds, and generate optimized theme files instantly.

## ✨ Features

- **UI Color Picker**: Change the **Primary Color** for both Light and Dark modes using a visual picker. No more editing code! 🎨
- **Smart Tonal Palette**: This isn't just a simple color swap. The manager mathematically calculates a complete **Material Design tonal palette** (shades 05–95) based on your chosen color. This ensures text remains readable and contrast stays perfect. 🧠
- **Custom Backgrounds**: Easily paste a URL for your custom background images. 🖼️
- **Dual Generation**: With a single click, the manager generates two themes:
    1.  **Frosted Glass Custom**: The full experience with blur and glass effects. ❄️
    2.  **Frosted Glass Custom Lite**: A performance-optimized version for older devices (no blur). ⚡
- **Instant Updates**: Changes are applied immediately without needing to restart Home Assistant. 🚀
- **Self-Contained Output**: Generated files now include their own light and dark styling-engine themes. The separate Frosted Glass theme repository is not required.
- **Home Assistant 2026.8 Ready**: Generated YAML uses valid non-empty mode declarations and current form, switch and shape tokens.
- **UIX and card-mod Support**: Choose either styling engine without changing your dashboards.

---

## 🚀 Installation Guide

**Step 1: Prerequisites**
- You must have [HACS](https://hacs.xyz/) installed.
- Install exactly one styling engine through HACS:
  - [`UIX`](https://github.com/Lint-Free-Technology/uix), the actively developed successor to card-mod. It supports the existing card-mod theme keys used here.
  - [`card-mod`](https://github.com/thomasloven/lovelace-card-mod), if you prefer to keep your current setup.

Do not install both engines at the same time.

**Step 2: Install via HACS**
1. Open HACS -> Integrations.
2. Click the menu (three dots) in the top right -> **Custom repositories**.
3. Paste this repository URL: `https://github.com/wessamlauf/frosted-glass-manager`
4. Select Category: **Integration**.
5. Click **Add**, then find **Frosted Glass Theme Manager** in the list and install it.
6. **Restart Home Assistant.**

**Step 3: Install Manually (Alternative)**
1. Download this repository.
2. Copy the `custom_components/frosted_glass_manager` folder into your `config/custom_components/` directory.
3. Restart Home Assistant.

---

## ⚙️ Usage & Configuration

Once installed and restarted, you need to add the integration to your instance:

1. Go to **Settings** -> **Devices & Services**.
2. Click **Add Integration** (bottom right).
3. Search for **"Frosted Glass Theme Manager"**.
4. Finish the setup.

### How to Customize:
1. Find the integration in your list and click **CONFIGURE**.
2. You will see a form where you can set:
    * **Light Mode Primary Color** ☀️
    * **Light Mode Background URL**
    * **Dark Mode Primary Color** 🌑
    * **Dark Mode Background URL**
3. Click **SUBMIT**.

The integration automatically and atomically generates two files in your `themes/` folder: `Frosted Glass Custom.yaml` and `Frosted Glass Custom Lite.yaml`. Each file also contains its required light and dark engine themes, so no second theme package is needed.

### Activating the Theme:
1. Go to your **Profile** (click your name in the bottom-left corner).
2. Under **Theme**, select **Frosted Glass Custom** or **Frosted Glass Custom Lite**. The generated single-mode variants are also available when you want to force light or dark mode.

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

Found a bug or have a suggestion?  
Open an [issue](https://github.com/wessamlauf/frosted-glass-manager/issues) on GitHub.

*This integration is based on the visual design of the [Frosted Glass Themes](https://github.com/wessamlauf/homeassistant-frosted-glass-themes).*
