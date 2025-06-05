import threading

from imgui_bundle import hello_imgui, immapp
from unrealsdk import logging

from .backend import DrawCallback, RenderBackend


class ThreadBasedBackend(RenderBackend):
    def __init__(self) -> None:
        super().__init__()
        self._lock = threading.Lock()
        self._runner_thread: threading.Thread | None = None

    def create_window(
        self,
        title: str,
        width: int | None = None,
        height: int | None = None,
        callback: DrawCallback | None = None,
    ) -> None:
        def _threaded_window() -> None:
            self._should_close = False
            self._draw_callback = callback or self._draw_callback or self._fallback_drawcall
            self._theme_applied = False

            params = immapp.RunnerParams(
                fps_idling=hello_imgui.FpsIdling(fps_idle=0.0, enable_idling=False),
                callbacks=hello_imgui.RunnerCallbacks(
                    show_gui=self.render, 
                ),
                app_window_params=hello_imgui.AppWindowParams(
                    window_title=title,
                    window_geometry=hello_imgui.WindowGeometry(
                        size=None if not width or not height else (width, height),
                    ),
                    restore_previous_geometry=True,
                ),
            )
            add_ons_params = immapp.AddOnsParams(with_implot=True, with_markdown=True, with_node_editor=True)
            
            immapp.run(params, add_ons_params=add_ons_params)

            with self._lock:
                self._should_close = True 
                self._runner_thread = None


        with self._lock:
            if self.is_window_open(): 
                self.close_window()

            self._runner_thread = threading.Thread(
                target=_threaded_window,  
                daemon=True,
            )
            self._runner_thread.start()

    def close_window(self) -> None:
        with self._lock:
            if not self._runner_thread or not self._runner_thread.is_alive():
                if self.is_window_open(): 
                     if hello_imgui.get_runner_params():
                         hello_imgui.get_runner_params().app_shall_exit = True
                super().close_window()
                return None

            if hello_imgui.get_runner_params():
                 hello_imgui.get_runner_params().app_shall_exit = True
            
            self._runner_thread.join(timeout=1)
            if self._runner_thread.is_alive():
                logging.warning("blimgui: Runner thread did not exit in time after join.")
            self._runner_thread = None

        super().close_window() 
        return None


    def initialize(self) -> None:
        pass

    def render(self, *_) -> None: 
        with self._lock:
            self.apply_theme()
            
            if self._should_close: 
                if hello_imgui.get_runner_params():
                    hello_imgui.get_runner_params().app_shall_exit = True
                return

            if self._draw_callback:
                try:
                    self._draw_callback()
                except Exception as e: 
                    logging.error(f"Error in draw callback: {e}")
                    self._should_close = True 
                    if hello_imgui.get_runner_params():
                        hello_imgui.get_runner_params().app_shall_exit = True