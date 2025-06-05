import site
from collections.abc import Callable
from pathlib import Path
import os
from typing import Any

from mods_base import Game, Library, build_mod, options, MODS_DIR
from mods_base.keybinds import keybind
THREADED_RENDERING = False

match Game.get_tree():
    case Game.Oak:
        site.addsitedir(str(Path(__file__).parent.absolute() / "dist64"))
        THREADED_RENDERING = True
    case Game.Willow2:
        site.addsitedir(str(Path(__file__).parent.absolute() / "dist32"))
    case Game.Willow1:
        site.addsitedir(str(Path(__file__).parent.absolute() / "dist32"))
    case _:
        raise RuntimeError("Unknown Game.")

from imgui_bundle import hello_imgui, imgui

__version__: str
__version_info__: tuple[int, ...]

DRAW_FUN = Callable[[], None]
IMPL = None

ALL_THEMES = [
    hello_imgui.ImGuiTheme_.darcula_darker,
    hello_imgui.ImGuiTheme_.darcula,
    hello_imgui.ImGuiTheme_.imgui_colors_classic,
    hello_imgui.ImGuiTheme_.imgui_colors_dark,
    hello_imgui.ImGuiTheme_.imgui_colors_light,
    hello_imgui.ImGuiTheme_.material_flat,
    hello_imgui.ImGuiTheme_.photoshop_style,
    hello_imgui.ImGuiTheme_.gray_variations,
    hello_imgui.ImGuiTheme_.gray_variations_darker,
    hello_imgui.ImGuiTheme_.microsoft_style,
    hello_imgui.ImGuiTheme_.cherry,
    hello_imgui.ImGuiTheme_.light_rounded,
    hello_imgui.ImGuiTheme_.so_dark_accent_blue,
    hello_imgui.ImGuiTheme_.so_dark_accent_yellow,
    hello_imgui.ImGuiTheme_.so_dark_accent_red,
    hello_imgui.ImGuiTheme_.black_is_black,
    hello_imgui.ImGuiTheme_.white_is_white,
]

ALL_THEMES_NAMES = [theme.name for theme in ALL_THEMES]

THEME_FOLDER = Path(__file__).parent.absolute() / "themes"
CUSTOM_THEMES: dict[str, dict[str, Any]] = {}

if not THEME_FOLDER.exists():
    THEME_FOLDER.mkdir(parents=True, exist_ok=True)

if THEME_FOLDER.is_dir():
    for theme_file in THEME_FOLDER.glob("*.txt"):
        theme_name = theme_file.stem
        current_theme_file_data: dict[str, Any] = {}
        try:
            with open(theme_file, "r") as f:
                for line_content in f:
                    line_content = line_content.strip()
                    if not line_content or line_content.startswith("#"):
                        continue
                    
                    parts = line_content.split(":", 1)
                    if len(parts) != 2:
                        continue
                    
                    attr_name = parts[0].strip()
                    values_str_list = parts[1].strip().split()
                    num_values = len(values_str_list)
                    parsed_value: Any = None

                    if num_values == 4:
                        try: parsed_value = tuple(float(v.strip()) for v in values_str_list)
                        except ValueError: continue
                    elif num_values == 2:
                        try: parsed_value = tuple(float(v.strip()) for v in values_str_list)
                        except ValueError: continue
                    elif num_values == 1:
                        val_str = values_str_list[0]
                        val_str_lower = val_str.lower()
                        if val_str_lower == "true": parsed_value = True
                        elif val_str_lower == "false": parsed_value = False
                        else:
                            try: parsed_value = float(val_str)
                            except ValueError: parsed_value = val_str
                    else:
                        continue
                    
                    if parsed_value is not None:
                        current_theme_file_data[attr_name] = parsed_value
            
            if current_theme_file_data:
                CUSTOM_THEMES[theme_name] = current_theme_file_data
                if f"Custom: {theme_name}" not in ALL_THEMES_NAMES:
                    ALL_THEMES_NAMES.append(f"Custom: {theme_name}")
        except Exception as e:
            print(f"Error loading theme {theme_name} from {theme_file.name}: {str(e)}")

if THREADED_RENDERING:
    from blimgui.backends.threaded import ThreadBasedBackend as Backend
else:
    from blimgui.backends.hook_based import HookBasedBackend as Backend
IMPL = Backend()
IMPL.initialize()


def style_ui(_option: options.SpinnerOption | None = None, val: str = "") -> None:
    if not imgui.get_current_context():
        return
        
    if not hello_imgui.is_using_hello_imgui():
        return

    theme_name_to_apply = val or imgui_theme.value
    applied_theme_display_name = theme_name_to_apply 

    base_hello_theme = hello_imgui.ImGuiTheme_.darcula_darker
    if theme_name_to_apply in ALL_THEMES_NAMES and not theme_name_to_apply.startswith("Custom: "):
        try:
            theme_index = ALL_THEMES_NAMES.index(theme_name_to_apply)
            if 0 <= theme_index < len(ALL_THEMES):
                 base_hello_theme = ALL_THEMES[theme_index]
        except ValueError as e:
            print(f"Error applying theme: {e}")
    
    hello_imgui.apply_theme(base_hello_theme)
    style = imgui.get_style()
    
    if theme_name_to_apply.startswith("Custom: "):
        base_name = theme_name_to_apply.replace("Custom: ", "", 1)
        applied_theme_display_name = base_name
        if base_name in CUSTOM_THEMES:
            custom_definitions = CUSTOM_THEMES[base_name]
            for attr_name, parsed_value in custom_definitions.items():
                is_color = hasattr(imgui.Col_, attr_name) and isinstance(parsed_value, tuple) and len(parsed_value) == 4
                
                if is_color:
                    if hasattr(style, 'set_color_'):
                        col_enum = getattr(imgui.Col_, attr_name)
                        style.set_color_(col_enum, imgui.ImVec4(parsed_value[0], parsed_value[1], parsed_value[2], parsed_value[3]))
                elif hasattr(style, attr_name):
                    try:
                        if isinstance(parsed_value, tuple) and len(parsed_value) == 2:
                            setattr(style, attr_name, imgui.ImVec2(parsed_value[0], parsed_value[1]))
                        elif isinstance(parsed_value, (float, bool)):
                            setattr(style, attr_name, parsed_value)
                        elif isinstance(parsed_value, str):
                            enum_val_to_set = None
                            if attr_name in ("window_menu_button_position", "color_button_position"):
                                val_lower = parsed_value.lower()
                                if val_lower == "left": enum_val_to_set = imgui.Dir.Left
                                elif val_lower == "right": enum_val_to_set = imgui.Dir.Right
                                elif val_lower == "none": enum_val_to_set = imgui.Dir.None_
                            
                            if enum_val_to_set is not None:
                                setattr(style, attr_name, enum_val_to_set)
                    except Exception as e:
                        print(f"Error setting attribute {e}")
    
    actual_print_name = applied_theme_display_name
    if theme_name_to_apply.startswith("Custom: "): 
        actual_print_name = theme_name_to_apply.replace("Custom: ", "", 1)
        
    print(f"blimgui: Theme '{actual_print_name}' processed.")


imgui_theme = options.SpinnerOption(
    "Theme",
    ALL_THEMES_NAMES[0] if ALL_THEMES_NAMES else "",
    ALL_THEMES_NAMES,
    wrap_enabled=True,
    on_change=style_ui,
)

close_window = IMPL.close_window
create_window = IMPL.create_window
set_draw_callback = IMPL.set_draw_callback
is_window_open = IMPL.is_window_open


@keybind("Test Window", "F1")
def test_window() -> None:
    if is_window_open():
        close_window()
        return
    create_window("Test Window")


def test():
    "helper for testing so I don't have to load a save"
    if is_window_open():
        close_window()
        return
    create_window("Test Window")


mod = build_mod(
    cls=Library,
    options=[
        imgui_theme,
    ],
    keybinds=[
        test_window,
    ],
)