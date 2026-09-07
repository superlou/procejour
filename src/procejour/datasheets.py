from nicegui import ui

from procejour.components.done_button import DoneButton
from procejour.components.pass_fail_button import PassFailButton
from procejour.models import Datasheet, StepMark, StepMarkPassFail


@ui.page("/datasheets/{datasheet_id}")
async def run_datasheet(datasheet_id: int):
    datasheet = await Datasheet.get(id=datasheet_id).prefetch_related("procedure")
    procedure = datasheet.procedure

    ui.label(procedure.title)

    with ui.list().classes("w-full"):
        for step in procedure.steps:
            await build_procedure_step(datasheet, step)


async def build_procedure_step(datasheet: Datasheet, step: dict):
    print(step)

    step_mark = (
        await StepMark.filter(step_id=step["id"], datasheet=datasheet)
        .order_by("-timestamp")
        .first()
    )
    observation = step_mark.observation["value"] if step_mark else ""
    pass_fail = "specification" in step
    pass_fail_mark = step_mark.pass_fail if step_mark else None

    units = None
    if step["observation"].startswith("decimal"):
        tokens = step["observation"].split(" ")
        if len(tokens) > 1:
            units = tokens[1]

    async def save_step():
        step_mark = StepMark(datasheet=datasheet, step_id=step["id"], comment="")
        step_mark.observation = {"value": observation_input.value}
        if pass_fail:
            match pass_fail_button.value:
                case "unset":
                    step_mark.pass_fail = StepMarkPassFail.UNSET
                case "pass":
                    step_mark.pass_fail = StepMarkPassFail.PASS
                case "fail":
                    step_mark.pass_fail = StepMarkPassFail.FAIL
        else:
            if complete_button.value:
                step_mark.pass_fail = StepMarkPassFail.DONE
            else:
                step_mark.pass_fail = StepMarkPassFail.UNSET
        await step_mark.save()

    with ui.item():
        with ui.item_section().classes("col-6"):
            ui.label(step["action"])
        with ui.item_section().classes("col-5"):
            observation_input = (
                ui.input(value=observation).props("outlined").classes("items-center")
            )

            if units:
                with observation_input.add_slot("append"):
                    ui.label(units)

            observation_input.on("keydown.enter", save_step)
        with ui.item_section().classes("col-1"):
            if pass_fail:
                value = "unset"
                match pass_fail_mark:
                    case StepMarkPassFail.PASS:
                        value = "pass"
                    case StepMarkPassFail.FAIL:
                        value = "fail"
                pass_fail_button = PassFailButton(value, on_change=save_step)
            else:
                value = step_mark.pass_fail == StepMarkPassFail.DONE
                complete_button = DoneButton(value, on_change=save_step)
