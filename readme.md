# blimgui 🎨
A [pyunrealsdk](https://github.com/bl-sdk/pyunrealsdk) mod library to easily add Dear ImGui windows in any Borderlands game.

## 🚀 Installation
Download the latest `blimgui.zip` from the [Releases page](blimgui.zip).
Unpack the `blimgui` folder into your game’s `sdk_mods` directory.

Example path: `Borderlands 2/Binaries/Win32/sdk_mods/blimgui/`

---

## 🖌️ Theme System
`blimgui` features an advanced theming system, allowing you to customize almost every aspect of its UI appearance, including colors, spacing, rounding, and more! You can use pre-made themes or unleash your creativity and make your own.

### 📁 Adding & Using Themes

1.  **Get Theme Files (`.txt`):**
    * Browse and download community-made themes from the [`themes`](./blimgui/themes) folder at the root of this GitHub repository.
    * Or, craft your unique theme by following the guide below!

2.  **Place Your Themes:**
    * Themes are loaded from a `themes` folder located *directly within your `blimgui` mod's directory*.
    * So, if `blimgui` is at `YourGame/sdk_mods/blimgui/`, your themes go into:
        ```
        YourGame/sdk_mods/blimgui/themes/
        ```
    * Create this `themes` subfolder if it doesn't exist.
    * Drop your `.txt` theme files in there.

3.  **Select in Game:**
    * Launch your game. `blimgui` automatically finds themes at startup.
    * Open any `blimgui` window.
    * Use the theme selector dropdown – your themes will appear as "Custom: YourThemeName".
    * The chosen theme applies instantly!

---

### ✨ Making Your Own Themes

Creating a custom theme is all about defining style properties in a simple text file.

1.  **Create Your File:**
    * Make a new text file, naming it something like `MyEpicTheme.txt`.
    * The filename (before `.txt`) becomes its name in the UI.
    * Save it in your `blimgui/themes/` folder.

2.  **Define Properties:**
    * Each line sets one style property using the format:
        ```
        property_name: value1 [value2 ...]
        ```
    * `property_name`: The ImGui style or color identifier (see table below for examples).
    * `value(s)`: Space-separated, depending on the property.

3.  **Value Formats:**
    * **Colors (RGBA)**: Four floats. `text: 1.0 0.9 0.8 1.0`
    * **ImVec2 (X Y)**: Two floats. `window_padding: 8.0 8.0`
    * **Floats**: Single float. `alpha: 0.95` or `window_rounding: 4.0`
    * **Booleans**: `true` or `false` (case-insensitive). `anti_aliased_lines: true`
    * **Enums (`ImGuiDir`)**: String like "Left", "Right", "None". `window_menu_button_position: Left`

4.  **Comments:**
    * Lines starting with `#` are ignored. Use them for notes!
        ```text
        # My Spooky Halloween Theme
        window_bg: 0.1 0.05 0.0 1.0 # Dark and eerie
        ```

5.  **Supported Style Attributes (Examples):**

    The theme engine supports most `ImGuiStyle` variables and all `ImGuiCol_` color values.

    | Attribute Name (`.txt`)       | Value Format Examples         | Description                                                              |
    | :---------------------------- | :---------------------------- | :----------------------------------------------------------------------- |
    | **General Style** |                               |                                                                          |
    | `alpha`                       | `0.95` (float)                | Global UI alpha transparency.                                            |
    | `disabled_alpha`              | `0.5` (float)                 | Alpha for disabled items.                                                |
    | `window_padding`              | `8.0 8.0` (X Y floats)        | Padding inside windows.                                                  |
    | `window_rounding`             | `4.0` (float)                 | Corner radius for windows.                                               |
    | `window_border_size`          | `1.0` (float)                 | Window border thickness.                                                 |
    | `window_menu_button_position` | `Left` (string)               | Position of the window collapse button ("Left", "Right", "None").      |
    | `frame_padding`               | `4.0 3.0` (X Y floats)        | Padding inside frames (buttons, inputs).                                 |
    | `frame_rounding`              | `3.0` (float)                 | Corner radius for frames.                                                |
    | `item_spacing`                | `8.0 4.0` (X Y floats)        | Spacing between widgets.                                                 |
    | `item_inner_spacing`          | `4.0 4.0` (X Y floats)        | Spacing within composite widgets.                                        |
    | `indent_spacing`              | `21.0` (float)                | Horizontal indentation amount.                                           |
    | `scrollbar_size`              | `14.0` (float)                | Scrollbar thickness.                                                     |
    | `scrollbar_rounding`          | `9.0` (float)                 | Scrollbar grab corner radius.                                            |
    | `grab_rounding`               | `3.0` (float)                 | Slider grab corner radius.                                               |
    | `tab_rounding`                | `4.0` (float)                 | Tab corner radius.                                                       |
    | `anti_aliased_lines`          | `true` / `false` (boolean)    | Enable/disable anti-aliased lines.                                       |
    | `anti_aliased_fill`           | `true` / `false` (boolean)    | Enable/disable anti-aliased fills.                                       |
    | **Colors (RGBA Format)** | `R G B A`                     | All take 4 floats (0.0-1.0)                                              |
    | `text`                        | `0.9 0.9 0.9 1.0`             | Default text color.                                                      |
    | `text_disabled`               | `0.6 0.6 0.6 1.0`             | Disabled text color.                                                     |
    | `window_bg`                   | `0.1 0.1 0.12 0.95`           | Window background.                                                       |
    | `child_bg`                    | `0.09 0.09 0.11 0.95`         | Child window background.                                                 |
    | `popup_bg`                    | `0.08 0.08 0.1 0.98`          | Popup and tooltip background.                                            |
    | `border`                      | `0.3 0.3 0.35 0.8`            | Border color for windows and frames.                                     |
    | `frame_bg`                    | `0.2 0.2 0.22 1.0`            | Background of inputs, sliders, checkboxes.                               |
    | `frame_bg_hovered`            | `0.25 0.25 0.28 1.0`          | Frame background when hovered.                                           |
    | `frame_bg_active`             | `0.3 0.3 0.33 1.0`            | Frame background when active/clicked.                                    |
    | `title_bg`                    | `0.15 0.15 0.17 1.0`          | Window title bar background.                                             |
    | `title_bg_active`             | `0.2 0.4 0.7 1.0`             | Title bar when window is active.                                         |
    | `title_bg_collapsed`          | `0.15 0.15 0.17 0.7`          | Title bar when window is collapsed.                                      |
    | `menu_bar_bg`                 | `0.12 0.12 0.14 1.0`          | Menu bar background.                                                     |
    | `button`                      | `0.2 0.4 0.7 1.0`             | Button color.                                                            |
    | `button_hovered`              | `0.25 0.5 0.8 1.0`            | Button color when hovered.                                               |
    | `button_active`               | `0.15 0.3 0.6 1.0`            | Button color when active.                                                |
    | `header`                      | `0.2 0.4 0.7 0.7`             | Collapsing header, TreeNode, Selectable background.                      |
    | `header_hovered`              | `0.25 0.5 0.8 0.8`            | Header when hovered.                                                     |
    | `header_active`               | `0.15 0.3 0.6 1.0`            | Header when active.                                                      |
    | `check_mark`                  | `0.9 0.9 0.9 1.0`             | Checkbox tick color.                                                     |
    | `slider_grab`                 | `0.5 0.5 0.5 1.0`             | Slider grabber color.                                                    |
    | `separator`                   | `0.4 0.4 0.4 0.8`             | Separator line color.                                                    |
    | `modal_window_dim_bg`         | `0.1 0.1 0.1 0.35`            | Modal window dimming background color.                                   |
    | *...and any other `ImGuiCol_` (e.g., `tab_hovered`, `plot_lines`, etc.)* | `R G B A` | See ImGui documentation for full list.                                   |

    **Note:** For a full list of non-color style variable names, you can refer to the Dear ImGui `ImGuiStyle` structure documentation or inspect the `imgui.get_style()` object in Python (e.g., using `dir(imgui.get_style())`). Color names correspond to `ImGuiCol_` enums (lowercase, without the prefix).

6.  **🧪 Testing:**
    * Save your `.txt` in `blimgui/themes/`.
    * Launch game, open `blimgui` UI, select your theme.
    * To see live edits, re-select the theme in the UI. (A game restart ensures a full fresh load).

---

### 💖 Theme Contributions
Created an awesome theme? Share it! Submit a `.txt` file via a Pull Request to the [`themes`](./themes) folder on GitHub.