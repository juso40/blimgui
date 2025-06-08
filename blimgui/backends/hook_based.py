from imgui_bundle import (
    hello_imgui,  # type: ignore
    immapp,
)
from mods_base import Game
from unrealsdk import logging
from unrealsdk.hooks import Type, add_hook

from .backend import DrawCallback, RenderBackend

try:
    HOOK_ADDRESSES = {
        Game.Willow1: "Engine.GameViewportClient:Tick",
        Game.Willow2: "WillowGame.WillowGameViewportClient:Tick",
    }
except AttributeError:
    # Fallback while the SDK's nightly is not released
    HOOK_ADDRESSES = {
        Game.Willow2: "WillowGame.WillowGameViewportClient:Tick",
    }


class HookBasedBackend(RenderBackend):
    def initialize(self) -> None:
        if (hook_addr := HOOK_ADDRESSES.get(Game.get_tree())) is None:
            raise RuntimeError(f"Unsupported game: {Game.get_tree()}")

        add_hook(
            hook_addr,
            Type.POST_UNCONDITIONAL,
            "blimgui_hooked_render",
            self.render,
        )

    def create_window(
        self,
        title: str,
        width: int | None = None,
        height: int | None = None,
        callback: DrawCallback | None = None,
    ) -> None:
        if self.is_window_open():
            print("Window already open!")
            return

        self._should_close = False
        self._draw_callback = callback or self._draw_callback or self._fallback_drawcall
        self._theme_applied = False

        immapp.manual_render.setup_from_runner_params(
            runner_params=immapp.RunnerParams(
                fps_idling=hello_imgui.FpsIdling(fps_idle=0.0, enable_idling=False),
                callbacks=hello_imgui.RunnerCallbacks(
                    show_gui=self._draw_callback,
                ),
                app_window_params=hello_imgui.AppWindowParams(
                    window_title=title,
                    window_geometry=hello_imgui.WindowGeometry(
                        size=None if not width or not height else (width, height),
                    ),
                    restore_previous_geometry=True,
                ),
            ),
            add_ons_params=immapp.AddOnsParams(with_implot=True, with_markdown=True, with_node_editor=True),
        )
        self.apply_theme()

    def render(self, *_) -> None:  # noqa: ANN002
        if not hello_imgui.is_using_hello_imgui():
            return
        try:
            immapp.manual_render.render()
        except Exception as e:  # noqa: BLE001
            logging.error(f"Error during rendering: {e}")
            self.close_window()
        if self._should_close:
            if hello_imgui.get_runner_params():
                hello_imgui.get_runner_params().app_shall_exit = True
            immapp.manual_render.tear_down()
