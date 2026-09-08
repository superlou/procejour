from nicegui import ui

from procejour.components.datasheet_input import DatasheetInput

from ..models import Datasheet, StepMark, StepMarkPassFail
from .done_button import DoneButton


async def get_current_step_mark(id: str, datasheet: Datasheet):
    return (
        await StepMark.filter(step_id=id, datasheet=datasheet)
        .order_by("-timestamp")
        .first()
    )


async def simple_action_step(step, datasheet):
    step_mark = await get_current_step_mark(step["id"], datasheet)
    observation = step_mark.observation["value"] if step_mark else ""

    units = None
    if "observation" in step and step["observation"].startswith("decimal"):
        tokens = step["observation"].split(" ")
        if len(tokens) > 1:
            units = tokens[1]

    async def save_step():
        print("saving")
        step_mark = StepMark(datasheet=datasheet, step_id=step["id"], comment="")
        step_mark.observation = {"value": observation_input.value}
        if complete_button.value:
            step_mark.pass_fail = StepMarkPassFail.DONE
        else:
            step_mark.pass_fail = StepMarkPassFail.UNSET
        await step_mark.save()

    with ui.item().classes("grid grid-cols-12 w-full"):
        with ui.item_section().classes("col-span-1"):
            ui.label(step["num"])
        with ui.item_section().classes("col-span-6"):
            ui.label(step["action"])
        with ui.item_section().classes("col-span-2"):
            observation_input = DatasheetInput(observation, units, on_commit=save_step)
        with ui.item_section().classes("col-span-2"):
            ui.label("").classes("text-center")
        with ui.item_section().classes("col-span-1"):
            value = step_mark.pass_fail == StepMarkPassFail.DONE if step_mark else None
            complete_button = DoneButton(value, on_change=save_step)
