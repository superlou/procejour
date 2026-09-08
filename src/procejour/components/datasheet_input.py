from datetime import datetime
from enum import Enum
from typing import Callable, Coroutine

from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from nicegui.helpers import is_coroutine_function

from procejour.auth import get_user


class Autofill(Enum):
    USER = "user"
    DATE = "date"


class DatasheetInput:
    def __init__(
        self,
        value,
        units: str | None = None,
        on_commit: Callable | Coroutine | None = None,
        on_change: Callable | Coroutine | None = None,
        autofill: Autofill | None = None,
    ):
        self.value = value
        self.units = units
        self.on_commit = on_commit
        self.on_change = on_change
        self.autofill = autofill

        self.render()

    def render(self):
        self.control = ui.input(value=self.value, on_change=self.update_value).props(
            "outlined"
        )

        if self.units:
            with self.control.add_slot("append"):
                ui.label(self.units)

        if self.autofill:
            with self.control.add_slot("prepend"):
                ui.button(icon="auto_fix_high", on_click=self.run_autofill).props(
                    "flat dense"
                )

        self.control.on("keydown.enter", self.call_on_commit)

    async def run_autofill(self):
        match self.autofill:
            case Autofill.USER:
                self.control.value = (await get_user()).name
            case Autofill.DATE:
                self.control.value = datetime.now().strftime("%m/%d/%Y")

    async def update_value(self, evt: ValueChangeEventArguments | None = None):
        if self.value != self.control.value:
            self.control.props("filled")
        else:
            self.control.props(remove="filled")

        await self.call_on_change()

    async def call_on_commit(self):
        self.value = self.control.value
        await self.update_value()

        if is_coroutine_function(self.on_commit):
            await self.on_commit()
        elif self.on_commit:
            self.on_commit()

    async def call_on_change(self):
        if is_coroutine_function(self.on_change):
            await self.on_change()
        elif self.on_change:
            self.on_change()
