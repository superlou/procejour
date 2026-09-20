import inspect
from typing import Callable, Literal

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
                with PFButton(icon="check", on_click=self.clear, color="green"):
                    ui.label("Pass").classes("gt-md")
                    ui.label("P").classes("lt-lg")
            case "fail":
                with PFButton(on_click=self.clear, color="red").props(
                    "icon-right=close"
                ):
                    ui.label("Fail").classes("gt-md")
                    ui.label("F").classes("lt-lg")

    async def call_on_change(self):
        if inspect.iscoroutinefunction(self.on_change):
            await self.on_change()
        elif self.on_change:
            self.on_change()

    async def set(
        self,
        value: Literal["pass"] | Literal["fail"] | Literal["unset"],
        run_callback=True,
    ):
        self.value = value
        self._render.refresh()
        if run_callback:
            await self.call_on_change()

    async def set_pass(self, run_callback=True):
        await self.set("pass", run_callback)

    async def set_fail(self, run_callback=True):
        await self.set("fail", run_callback)

    async def clear(self, run_callback=True):
        await self.set("unset", run_callback)
