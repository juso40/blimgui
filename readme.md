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

| Name                     | Description                                               |
|--------------------------|-----------------------------------------------------------|
| `window_bg`              | Background color of windows                               |
| `child_bg`               | Background color of child windows                         |
| `border`                 | Border color                                              |
| `border_shadow`          | Border shadow color (rarely used)                         |
| `button`                 | Normal button color                                       |
| `button_hovered`         | Button color on hover                                     |
| `button_active`          | Button color when held/active                             |
| `check_mark`             | Color of checkboxes' check marks                          |
| `frame_bg`               | Background of input fields and sliders                    |
| `frame_bg_hovered`       | Background when hovered                                   |
| `frame_bg_active`        | Background when active (clicked/focused)                  |
| `header`                 | Collapsing header background                              |
| `header_hovered`         | Collapsing header on hover                                |
| `header_active`          | Collapsing header when open                               |
| `menu_bar_bg`            | Background of menu bars                                   |
| `modal_window_dim_bg`    | Background dimming color for modal dialogs                |
| `popup_bg`               | Background of popups                                      |
| `resize_grip`            | Color of resize grip                                      |
| `resize_grip_hovered`    | Resize grip on hover                                      |
| `resize_grip_active`     | Resize grip when dragging                                 |
| `scrollbar_bg`           | Scrollbar background                                      |
| `scrollbar_grab`         | Scrollbar handle                                          |
| `scrollbar_grab_hovered` | Scrollbar handle on hover                                 |
| `scrollbar_grab_active`  | Scrollbar handle when dragging                            |
| `separator`              | Separator line                                            |
| `separator_hovered`      | Separator on hover                                        |
| `separator_active`       | Separator when clicked                                    |
| `slider_grab`            | Slider knob                                               |
| `slider_grab_active`     | Slider knob when active                                   |
| `tab`                    | Tab background (inactive)                                 |
| `tab_hovered`            | Tab on hover                                              |
| `tab_active`             | Active tab                                                |
| `tab_selected`           | Selected tab                                              |
| `tab_unfocused`          | Unfocused tab                                             |
| `tab_unfocused_active`   | Active tab when unfocused                                 |
| `table_border_light`     | Light border of tables                                    |
| `table_border_strong`    | Strong table border (usually outer edge)                  |
| `table_header_bg`        | Background of table headers                               |
| `table_row_bg`           | Background for table rows                                 |
| `table_row_bg_alt`       | Alternate row background (striped tables)                 |
| `text`                   | Default text color                                        |
| `text_disabled`          | Disabled/grayed-out text                                  |
| `text_link`              | Clickable link-style text                                 |
| `text_selected_bg`       | Background of selected text                               |
| `title_bg`               | Title bar background                                      |
| `title_bg_active`        | Title bar when window is active                           |
| `title_bg_collapsed`     | Title bar when window is collapsed                        |
| `drag_drop_target`       | Highlight when dragging over drop targets                 |
| `nav_highlight`          | Highlighted item under keyboard/gamepad navigation focus  |


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