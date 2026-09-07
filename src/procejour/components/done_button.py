import inspect
from typing import Callable

from nicegui import ui


class BigButton(ui.button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.props("outline dense").classes("q-py-md w-full")


class DoneButton:
    def __init__(self, value: bool = False, on_change: Callable | None = None):
        self.value = value
        self.on_change = on_change
        self._render()

    @ui.refreshable_method
    def _render(self):
        if self.value:
            BigButton(icon="check_box", on_click=self.clear, color="black")
        else:
            BigButton(icon="check_box_outline_blank", on_click=self.set)

    async def call_on_change(self):
        if inspect.iscoroutinefunction(self.on_change):
            await self.on_change()
        elif self.on_change:
            self.on_change()

    async def set(self):
        self.value = True
        self._render.refresh()
        await self.call_on_change()

    async def clear(self):
        self.value = False
        self._render.refresh()
        await self.call_on_change()
