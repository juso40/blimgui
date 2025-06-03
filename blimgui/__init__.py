import site
from collections.abc import Callable
from pathlib import Path

from mods_base import Game, Library, build_mod, options
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
# git clone https://github.com/pthom/imgui_bundle.git
# cd imgui_bundle
# py -V:3.13-32 -m pip install -v . -t "./dist"
# monkey patched pyglet.gl.win32.py:32 to never use WGL_ARB_pixel_format

from imgui_bundle import hello_imgui  # type: ignore

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


if THREADED_RENDERING:
    from blimgui.backends.threaded import ThreadBasedBackend as Backend
else:
    from blimgui.backends.hook_based import HookBasedBackend as Backend
IMPL = Backend()
IMPL.initialize()


def style_ui(_option: options.SpinnerOption | None = None, val: str = "") -> None:
    """
    Apply the selected theme to the UI.

    :return: None
    """
    if not hello_imgui.is_using_hello_imgui():
        return
    theme = ALL_THEMES[ALL_THEMES_NAMES.index(val or imgui_theme.value)]
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


mod = build_mod(
    cls=Library,
    options=[
        imgui_theme,
    ],
    keybinds=[
        test_window,
    ],
)
