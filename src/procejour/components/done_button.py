import inspect
from typing import Callable

from nicegui import ui


class DoneButton(ui.button):
    def __init__(self, value: bool = False, on_change: Callable | None = None):
        super().__init__(on_click=self.click)
        self.props("outline dense").classes("q-py-md w-full")
        self.value = value
        self.on_change = on_change

        self.bind_icon_from(
            self, "value", lambda x: "check_box" if x else "check_box_outline_blank"
        )
        self.bind_background_color_from(
            self, "value", lambda x: "black" if x else "primary"
        )

    def take_focus(self):
        ui.run_javascript(f"getHtmlElement({self.id}).focus()")

    async def call_on_change(self):
        if inspect.iscoroutinefunction(self.on_change):
            await self.on_change()
        elif self.on_change:
            self.on_change()

    async def click(self):
        if self.value:
            await self.clear_button()
        else:
            await self.set_button()

    async def set_button(self, run_callback=True):
        self.value = True
        if run_callback:
            await self.call_on_change()

    async def clear_button(self, run_callback=True):
        self.value = False
        if run_callback:
            await self.call_on_change()
