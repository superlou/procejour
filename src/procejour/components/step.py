from typing import Coroutine, Literal

from nicegui import ui

from ..components.pass_fail_button import PassFailButton
from .datasheet_input import Autofill, DatasheetInput
from .done_button import DoneButton


async def no_observation_step(
    num: str,
    action: str,
    done: bool,
    save_step: Coroutine,
):
    async def on_save():
        await save_step("", complete_button.value)

    with ui.item().classes("grid grid-cols-12 w-full"):
        with ui.item_section().classes("col-span-1"):
            ui.label(num)
        with ui.item_section().classes("col-span-6"):
            ui.label(action)
        with ui.item_section().classes("col-span-2"):
            pass
        with ui.item_section().classes("col-span-2"):
            ui.label("").classes("text-center")
        with ui.item_section().classes("col-span-1"):
            complete_button = DoneButton(done, on_change=on_save)


async def observation_step(
    num: str,
    action: str,
    observation: str,
    units: str,
    done: bool,
    autofill: Autofill | None,
    save_step: Coroutine,
):
    async def on_save():
        await save_step(observation_input.value, complete_button.value)

    with ui.item().classes("grid grid-cols-12 w-full"):
        with ui.item_section().classes("col-span-1"):
            ui.label(num)
        with ui.item_section().classes("col-span-6"):
            ui.label(action)
        with ui.item_section().classes("col-span-2"):
            observation_input = DatasheetInput(
                observation, units, on_commit=on_save, autofill=autofill
            )
        with ui.item_section().classes("col-span-2"):
            ui.label("").classes("text-center")
        with ui.item_section().classes("col-span-1"):
            complete_button = DoneButton(done, on_change=on_save)


async def pass_fail_step(
    num: str,
    action: str,
    observation: str,
    units: str,
    specification: str,
    result: Literal["pass"] | Literal["fail"] | Literal["unset"],
    autofill: Autofill | None,
    save_step: Coroutine,
):
    async def on_save():
        await save_step(observation_input.value, pass_fail_button.value)

    with ui.item().classes("grid grid-cols-12 w-full"):
        with ui.item_section().classes("col-span-1"):
            ui.label(num)
        with ui.item_section().classes("col-span-6"):
            ui.label(action)
        with ui.item_section().classes("col-span-2"):
            observation_input = DatasheetInput(
                observation, units, on_commit=on_save, autofill=autofill
            )
        with ui.item_section().classes("col-span-2"):
            ui.label(specification).classes("text-center")
        with ui.item_section().classes("col-span-1"):
            pass_fail_button = PassFailButton(result, on_change=on_save)
