from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from imgui_bundle import hello_imgui, imgui
from imgui_bundle import icons_fontawesome_4 as icons

type DrawCallback = Callable[[], None]


class RenderBackend(ABC):
    def __init__(self) -> None:
        self._draw_callback: DrawCallback | None = self._fallback_drawcall
        self._should_close: bool = False
        self._theme_applied: bool = False

    def set_draw_callback(self, callback: DrawCallback) -> None:
        self._draw_callback = callback

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def create_window(
        self,
        title: str,
        width: int | None = None,
        height: int | None = None,
        callback: DrawCallback | None = None,
    ) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass

    def close_window(self) -> None:
        self._should_close = True

    def is_window_open(self) -> bool:
        return hello_imgui.is_using_hello_imgui() and not self._should_close

    def apply_theme(self) -> None:
        if self._theme_applied:
            return
        from blimgui import style_ui
        style_ui() 

        self._theme_applied = True

    def _fallback_drawcall(self) -> None:
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                clicked_quit, _selected_quit = imgui.menu_item("Quit", "Cmd+Q", False, True)
                if clicked_quit:
                    self.close_window()
                imgui.end_menu()
            imgui.end_main_menu_bar()

        imgui.begin("Hello World", True)
        imgui.text("This is a text!" + icons.ICON_FA_HEART)
        imgui.text_colored((0.2, 1.0, 0.0, 1.0), "Colored Text, wow!")
        imgui.end()