import inspect
from typing import Callable

from nicegui import ui


class PFButton(ui.button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.props("outline dense").classes("q-py-md w-full")


class PassFailButton:
    def __init__(self, value="unset", on_change: Callable | None = None):
        self.value = value
        self.on_change = on_change
        self._render()

    @ui.refreshable_method
    def _render(self):
        match self.value:
            case "unset":
                with ui.button_group().props("outline dense").classes("w-full"):
                    PFButton("P", on_click=self.set_pass)
                    PFButton("F", on_click=self.set_fail)
            case "pass":
                btn = PFButton("Pass", icon="check", on_click=self.clear, color="green")
                with btn.add_slot("append"):
                    ui.label("test")
            case "fail":
                PFButton("Fail", on_click=self.clear, color="red").props(
                    "icon-right=close"
                )

    async def call_on_change(self):
        if inspect.iscoroutinefunction(self.on_change):
            await self.on_change()
        elif self.on_change:
            self.on_change()

    async def set_pass(self):
        self.value = "pass"
        self._render.refresh()
        await self.call_on_change()

    async def set_fail(self):
        self.value = "fail"
        self._render.refresh()
        await self.call_on_change()

    async def clear(self):
        self.value = "unset"
        self._render.refresh()
        await self.call_on_change()
