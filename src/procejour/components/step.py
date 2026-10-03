from typing import Coroutine, Literal

from nicegui import binding, ui

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


@binding.bindable_dataclass
class ObservationStepArgs:
    num: str = ""
    action: str = ""
    observation: str = ""
    units: str | None = None
    format: str | None = None
    done: bool = False
    autofill: Autofill | None = None
    enabled: bool = True


async def observation_step(
    args: ObservationStepArgs,
    save_step: Coroutine,
    advance: Coroutine,
):
    async def commit_and_advance():
        await complete_button.set_button(run_callback=False)
        await save()
        await advance()

    async def save():
        await save_step(observation_input.value, complete_button.value)

    with ui.item().classes("grid grid-cols-12 w-full"):
        with ui.item_section().classes("col-span-1"):
            ui.label(args.num)
        with ui.item_section().classes("col-span-6"):
            ui.label(args.action)
        with ui.item_section().classes("col-span-2"):
            observation_input = DatasheetInput(
                args.observation,
                args.units,
                on_commit=commit_and_advance,
                on_change=save,
                autofill=args.autofill,
            ).bind_enabled_from(args, "enabled")
        with ui.item_section().classes("col-span-2"):
            ui.label("").classes("text-center")
        with ui.item_section().classes("col-span-1"):
            complete_button = DoneButton(args.done, on_change=save).bind_enabled_from(
                args, "enabled"
            )

    return observation_input


@binding.bindable_dataclass
class PassFailStepArgs:
    num: str = ""
    action: str = ""
    observation: str = ""
    specification: str = ""
    result: Literal["unset"] | Literal["pass"] | Literal["fail"] = "unset"
    units: str | None = None
    format: str | None = None
    autofill: Autofill | None = None
    enabled: bool = True


async def pass_fail_step(
    args: PassFailStepArgs, save_step: Coroutine, advance: Coroutine
):
    async def commit_and_advance():
        obs = observation_input.value

        if observation_input.value == "":
            pf = "unset"
        else:
            pf = (
                "pass"
                if observation_meets_spec(obs, args.format, args.specification)
                else "fail"
            )

        await pass_fail_button.set(pf, run_callback=False)
        await save()
        await advance()

    async def save():
        await save_step(observation_input.value, pass_fail_button.value)

    with ui.item().classes("grid grid-cols-12 w-full"):
        with ui.item_section().classes("col-span-1"):
            ui.label(args.num)
        with ui.item_section().classes("col-span-6"):
            ui.label(args.action)
        with ui.item_section().classes("col-span-2"):
            observation_input = DatasheetInput(
                args.observation,
                args.units,
                on_commit=commit_and_advance,
                autofill=args.autofill,
                on_change=save,
            ).bind_enabled_from(args, "enabled")
        with ui.item_section().classes("col-span-2"):
            ui.label(args.specification).classes("text-center")
        with ui.item_section().classes("col-span-1"):
            pass_fail_button = PassFailButton(args.result, on_change=save).bind_enabled_from(args, "enabled")

    return observation_input
