from typing import Callable, Coroutine

from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from nicegui.helpers import is_coroutine_function


class DatasheetInput:
    def __init__(
        self,
        value,
        units: str | None = None,
        on_commit: Callable | Coroutine | None = None,
        on_change: Callable | Coroutine | None = None,
    ):
        self.value = value
        self.units = units
        self.on_commit = on_commit

        self.render()

    def render(self):
        self.control = ui.input(value=self.value, on_change=self.update_value).props(
            "outlined"
        )
        if self.units:
            with self.control.add_slot("append"):
                ui.label(self.units)

        self.control.on("keydown.enter", self.call_on_commit)

    def update_value(self, evt: ValueChangeEventArguments | None = None):
        if self.value != self.control.value:
            self.control.props("filled")
        else:
            self.control.props(remove="filled")

    async def call_on_commit(self):
        self.value = self.control.value
        self.update_value()

        if is_coroutine_function(self.on_commit):
            await self.on_commit()
        else:
            self.on_commit()

    async def call_on_change(self):
        if is_coroutine_function(self.on_commit):
            await self.on_commit()
        else:
            self.on_commit()
