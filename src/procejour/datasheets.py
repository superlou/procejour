from nicegui import ui

from procejour.auth import CurrentUser
from procejour.components.header import header
from procejour.components.step_header import header_step
from procejour.components.step_pass_fail_action import pass_fail_action_step
from procejour.components.step_simple_action import simple_action_step
from procejour.models import Datasheet


@ui.page("/datasheets/{datasheet_id}")
async def run_datasheet(datasheet_id: int, current_user: CurrentUser):
    datasheet = await Datasheet.get(id=datasheet_id).prefetch_related("procedure_rev")
    procedure_rev = datasheet.procedure_rev

    header(current_user)
    ui.label(procedure_rev.title)

    with ui.list().classes("w-full"):
        for step in procedure_rev.steps:
            await build_procedure_step(datasheet, step)


async def build_procedure_step(datasheet: Datasheet, step: dict):
    print(step)

    if step.get("heading", False):
        header_step(step)
    elif step.get("specification", False):
        await pass_fail_action_step(step, datasheet)
    else:
        await simple_action_step(step, datasheet)
