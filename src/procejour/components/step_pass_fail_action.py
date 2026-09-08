from nicegui import ui

from procejour.components.datasheet_input import DatasheetInput

from ..models import StepMark, StepMarkPassFail
from .pass_fail_button import PassFailButton
from .step_simple_action import determine_autofill, get_current_step_mark


async def pass_fail_action_step(step, datasheet):
    step_mark = await get_current_step_mark(step["id"], datasheet)
    observation = step_mark.observation["value"] if step_mark else ""
    pass_fail_mark = step_mark.pass_fail if step_mark else None

    units = None
    if "observation" in step and step["observation"].startswith("decimal"):
        tokens = step["observation"].split(" ")
        if len(tokens) > 1:
            units = tokens[1]

    async def save_step():
        step_mark = StepMark(datasheet=datasheet, step_id=step["id"], comment="")
        step_mark.observation = {"value": observation_input.value}
        match pass_fail_button.value:
            case "unset":
                step_mark.pass_fail = StepMarkPassFail.UNSET
            case "pass":
                step_mark.pass_fail = StepMarkPassFail.PASS
            case "fail":
                step_mark.pass_fail = StepMarkPassFail.FAIL

        await step_mark.save()

    with ui.item().classes("grid grid-cols-12 w-full"):
        with ui.item_section().classes("col-span-1"):
            ui.label(step["num"])
        with ui.item_section().classes("col-span-6"):
            ui.label(step["action"])
        with ui.item_section().classes("col-span-2"):
            observation_input = DatasheetInput(
                observation,
                units,
                on_commit=save_step,
                autofill=determine_autofill(step),
            )
        with ui.item_section().classes("col-span-2"):
            ui.label(step["specification"]).classes("text-center")
        with ui.item_section().classes("col-span-1"):
            value = "unset"
            match pass_fail_mark:
                case StepMarkPassFail.PASS:
                    value = "pass"
                case StepMarkPassFail.FAIL:
                    value = "fail"
            pass_fail_button = PassFailButton(value, on_change=save_step)
