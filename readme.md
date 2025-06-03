# blimgui

A [pyunrealsdk](https://github.com/bl-sdk/pyunrealsdk) mod library to easily add imgui windows in any Borderlands game.

## Installation

Download and unpack the [blimgui.zip](blimgui.zip) to your game’s `sdk_mods` directory.

---

## Theme System

blimgui supports both built-in and custom ImGui themes.  
You can choose from bundled themes or make your own!

### 📁 Theme Folder

Themes are located at:

```
<game folder>\sdk_mods\settings\themes
```

Each `.txt` file in that folder will appear as a selectable theme in the UI.

---

### 🎨 Adding Custom Themes

To add a new theme:

1. Place a `.txt` file in the `themes/` folder.
2. Use lowercase `imgui.Col_` names (see below).
3. Format: `name: r g b a` with values from `0.0` to `1.0`.

Example file path:
```
sdk_mods/settings/themes/ubuntu.txt
```

---

### ✍️ Making a Theme

Each line defines one color entry.  
The format is:

```
color_name: r g b a
```

Example theme `ubuntu.txt`:

```
# Ubuntu Theme
# Inspired by Ubuntu's color palette

window_bg: 0.188 0.157 0.153 0.98
child_bg: 0.198 0.167 0.163 0.98
popup_bg: 0.168 0.137 0.133 0.96

text: 0.90 0.90 0.90 1.00
text_disabled: 0.50 0.50 0.50 1.00
text_selected_bg: 0.925 0.302 0.075 0.40

button: 0.925 0.302 0.075 1.00
button_hovered: 0.950 0.400 0.150 1.00
button_active: 0.850 0.250 0.050 1.00
```

You can comment lines using `#`. Invalid lines are skipped.

---

### ✅ Supported `imgui.Col_` Attributes

Only the following names are supported:

```
window_bg, child_bg, border, border_shadow, button, button_active,
button_hovered, check_mark, frame_bg, frame_bg_active, frame_bg_hovered,
header, header_active, header_hovered, menu_bar_bg, modal_window_dim_bg,
popup_bg, resize_grip, resize_grip_active, resize_grip_hovered,
scrollbar_bg, scrollbar_grab, scrollbar_grab_active, scrollbar_grab_hovered,
separator, separator_active, separator_hovered, slider_grab, slider_grab_active,
tab, tab_hovered, tab_active, tab_selected, tab_unfocused, tab_unfocused_active,
table_border_light, table_border_strong, table_header_bg, table_row_bg, table_row_bg_alt,
text, text_disabled, text_link, text_selected_bg, title_bg, title_bg_active,
title_bg_collapsed, drag_drop_target, nav_highlight
```

---

### 🧪 Testing Your Theme

1. Drop it into `sdk_mods/settings/themes/`.
2. Reload or start the game.
3. Open your ImGui mod UI.
4. Select your theme from the dropdown.

---

### 🧡 Theme Contributions

Want to share a theme?  
Submit a `.txt` file via PR or drop it in the GitHub [themes folder](themes/).

```

Let me know if you'd like a preview screenshot section or a theme template download link included as well.