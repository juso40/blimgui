import site
from collections.abc import Callable
from pathlib import Path
import os

from mods_base import Game, Library, build_mod, options, MODS_DIR # type: ignore
from mods_base.keybinds import keybind # type: ignore
TREE_INFO = None
THREADED_RENDERING = False

def get_tree_info():
    return TREE_INFO

match Game.get_tree():
    case Game.Oak:
        site.addsitedir(str(Path(__file__).parent.absolute() / "dist64"))
        THREADED_RENDERING = True
        TREE_INFO = "Oak"
    case Game.Willow2:
        site.addsitedir(str(Path(__file__).parent.absolute() / "dist32"))
        TREE_INFO = "Willow2"
    case Game.Willow1:
        site.addsitedir(str(Path(__file__).parent.absolute() / "dist32"))
        TREE_INFO = "Willow1"
    case _:
        raise RuntimeError("Unknown Game.")

from imgui_bundle import hello_imgui, imgui  # type: ignore

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

# Custom theme loading
THEME_FOLDER = MODS_DIR / "settings" / "themes"
CUSTOM_THEMES = {}

if THEME_FOLDER.exists() and THEME_FOLDER.is_dir():
    for theme_file in THEME_FOLDER.glob("*.txt"):
        theme_name = theme_file.stem
        theme_data = {}
        try:
            with open(theme_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split(":")
                    if len(parts) != 2:
                        continue
                    col_name = parts[0].strip()
                    values = [float(x.strip()) for x in parts[1].split()]
                    if len(values) != 4:
                        continue
                    theme_data[col_name] = tuple(values)
            CUSTOM_THEMES[theme_name] = theme_data
            ALL_THEMES_NAMES.append(f"Custom: {theme_name}")
        except Exception as e:
            print(f"Failed to load theme {theme_name}: {str(e)}")
else:
    THEME_FOLDER.mkdir(exist_ok=True)

if THREADED_RENDERING:
    from blimgui.backends.threaded import ThreadBasedBackend as Backend
else:
    from blimgui.backends.hook_based import HookBasedBackend as Backend
IMPL = Backend()
IMPL.initialize()


def apply_custom_theme(theme_data: dict[str, tuple[float, float, float, float]]) -> None:
    """
    Applies a custom theme from loaded theme data.
    
    Args:
        theme_data: Dictionary mapping color names to RGBA tuples
    """
    imgui.style_colors_dark()
    for col_name, color in theme_data.items():
        if hasattr(imgui.Col_, col_name):
            col_enum = getattr(imgui.Col_, col_name)
            imgui.push_style_color(col_enum, imgui.ImVec4(*color))


def style_ui(_option: options.SpinnerOption | None = None, val: str = "") -> None:
    """
    Apply the selected theme to the UI. Supports both built-in and custom themes.
    
    Returns: None
    """
    if not hello_imgui.is_using_hello_imgui():
        return
    theme_name = val or imgui_theme.value
    
    if theme_name.startswith("Custom: "):
        base_name = theme_name.replace("Custom: ", "", 1)
        if base_name in CUSTOM_THEMES:
            apply_custom_theme(CUSTOM_THEMES[base_name])
    else:
        theme = ALL_THEMES[ALL_THEMES_NAMES.index(theme_name)]
        hello_imgui.apply_theme(theme)


imgui_theme = options.SpinnerOption(
    "Theme",
    ALL_THEMES_NAMES[0],
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