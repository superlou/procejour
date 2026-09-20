from typing import Coroutine, Literal

from nicegui import ui

from procejour.observation_check import observation_meets_spec

from ..components.pass_fail_button import PassFailButton
from .datasheet_input import Autofill, DatasheetInput
from .done_button import DoneButton


async def no_observation_step(
    num: str,
    action: str,
    done: bool,
    save_step: Coroutine,
    advance: Coroutine,
):
    async def on_save():
        await save_step("", complete_button.value)
        if complete_button.value:
            await advance()

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

        return complete_button


async def observation_step(
    num: str,
    action: str,
    observation: str,
    units: str,
    done: bool,
    autofill: Autofill | None,
    save_step: Coroutine,
    advance: Coroutine,
):
    async def commit_and_advance():
        await complete_button.set(run_callback=False)
        await save()
        await advance()

    async def save():
        await save_step(observation_input.value, complete_button.value)

    with ui.item().classes("grid grid-cols-12 w-full"):
        with ui.item_section().classes("col-span-1"):
            ui.label(num)
        with ui.item_section().classes("col-span-6"):
            ui.label(action)
        with ui.item_section().classes("col-span-2"):
            observation_input = DatasheetInput(
                observation, units, on_commit=commit_and_advance, autofill=autofill
            )
        with ui.item_section().classes("col-span-2"):
            ui.label("").classes("text-center")
        with ui.item_section().classes("col-span-1"):
            complete_button = DoneButton(done, on_change=save)

    return observation_input


async def pass_fail_step(
    num: str,
    action: str,
    observation: str,
    format,
    units: str,
    specification: str,
    result: Literal["pass"] | Literal["fail"] | Literal["unset"],
    autofill: Autofill | None,
    save_step: Coroutine,
    advance: Coroutine,
):
    async def commit_and_advance():
        obs = observation_input.value

        if observation_input.value == "":
            pf = "unset"
        else:
            pf = (
                "pass" if observation_meets_spec(obs, format, specification) else "fail"
            )

        await pass_fail_button.set(pf, run_callback=False)
        await save()
        await advance()

    async def save():
        await save_step(observation_input.value, pass_fail_button.value)

    with ui.item().classes("grid grid-cols-12 w-full"):
        with ui.item_section().classes("col-span-1"):
            ui.label(num)
        with ui.item_section().classes("col-span-6"):
            ui.label(action)
        with ui.item_section().classes("col-span-2"):
            observation_input = DatasheetInput(
                observation, units, on_commit=commit_and_advance, autofill=autofill
            )
        with ui.item_section().classes("col-span-2"):
            ui.label(specification).classes("text-center")
        with ui.item_section().classes("col-span-1"):
            pass_fail_button = PassFailButton(result, on_change=save)

    return observation_input
