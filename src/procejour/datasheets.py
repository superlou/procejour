from nicegui import ui

from procejour.auth import CurrentUser
from procejour.components.datasheet_input import Autofill
from procejour.components.sidebar_menu import sidebar_menu
from procejour.components.step import (
    no_observation_step,
    observation_step,
    pass_fail_step,
)
from procejour.components.step_header import header_step
from procejour.datasheet_utils import determine_autofill, get_current_step_mark
from procejour.models import Datasheet, StepMark, StepMarkPassFail, User


@ui.page("/datasheets/{datasheet_id}")
async def run_datasheet(datasheet_id: int, current_user: CurrentUser):
    datasheet = await Datasheet.get(id=datasheet_id).prefetch_related("procedure_rev")
    procedure_rev = datasheet.procedure_rev

    header_links = [
        (f"#{step['id']}", f"{step['num']} {step['heading']}")
        for step in procedure_rev.steps
        if "heading" in step
    ]

    sidebar_menu(current_user, page_links=header_links)
    ui.label(procedure_rev.title)

    with ui.list().classes("w-full"):
        for step in procedure_rev.steps:
            await build_step(datasheet, step, current_user)


async def build_step(datasheet: Datasheet | None, step: dict, current_user: User):
    print(step)

    if step.get("heading", False):
        header_step(step)
    elif step.get("specification", False):
        await build_pass_fail_step(datasheet, step, current_user)
    elif "observation" in step:
        await build_observation_step(datasheet, step, current_user)
    else:
        await build_no_observation_step(datasheet, step, current_user)


async def build_no_observation_step(
    datasheet: Datasheet | None, step: dict, current_user: User
):
    if datasheet is None:
        done = False
    else:
        step_mark = await get_current_step_mark(step["id"], datasheet)
        done = step_mark.pass_fail == StepMarkPassFail.DONE if step_mark else False

    async def save_step(observation, done):
        if datasheet is None:
            return

        step_mark = StepMark(
            datasheet=datasheet, step_id=step["id"], comment="", set_by=current_user
        )
        step_mark.observation = {}
        step_mark.pass_fail = StepMarkPassFail.DONE if done else StepMarkPassFail.UNSET
        await step_mark.save()

    await no_observation_step(step["num"], step["action"], done, save_step)


async def build_observation_step(
    datasheet: Datasheet | None, step: dict, current_user: User
):
    if datasheet is None:
        observation = ""
        done = False
    else:
        step_mark = await get_current_step_mark(step["id"], datasheet)
        observation = (
            step_mark.observation["value"]
            if step_mark and "value" in step_mark.observation
            else ""
        )
        done = step_mark.pass_fail == StepMarkPassFail.DONE if step_mark else False

    async def save_step(observation, done):
        if datasheet is None:
            return

        step_mark = StepMark(
            datasheet=datasheet, step_id=step["id"], comment="", set_by=current_user
        )
        step_mark.observation = {"value": observation}
        step_mark.pass_fail = StepMarkPassFail.DONE if done else StepMarkPassFail.UNSET
        await step_mark.save()

    units = ""
    if step["observation"].startswith("decimal"):
        tokens = step["observation"].split(" ")
        if len(tokens) > 1:
            units = tokens[1]

    await observation_step(
        step["num"],
        step["action"],
        observation,
        units,
        done,
        determine_autofill(step),
        save_step,
    )


async def build_pass_fail_step(
    datasheet: Datasheet | None, step: dict, current_user: User
):
    if datasheet is None:
        observation = ""
        result = "unset"
    else:
        step_mark = await get_current_step_mark(step["id"], datasheet)
        observation = (
            step_mark.observation["value"]
            if step_mark and "value" in step_mark.observation
            else ""
        )
        match step_mark:
            case StepMark(pass_fail=StepMarkPassFail.PASS):
                result = "pass"
            case StepMark(pass_fail=StepMarkPassFail.FAIL):
                result = "fail"
            case _:
                result = "unset"

    async def save_step(observation, result):
        if datasheet is None:
            return

        step_mark = StepMark(
            datasheet=datasheet, step_id=step["id"], comment="", set_by=current_user
        )
        step_mark.observation = {"value": observation}
        if result == "pass":
            step_mark.pass_fail = StepMarkPassFail.PASS
        elif result == "fail":
            step_mark.pass_fail = StepMarkPassFail.FAIL
        else:
            step_mark.pass_fail = StepMarkPassFail.UNSET

        await step_mark.save()

    units = ""
    if step["observation"].startswith("decimal"):
        tokens = step["observation"].split(" ")
        if len(tokens) > 1:
            units = tokens[1]

    await pass_fail_step(
        step["num"],
        step["action"],
        observation,
        units,
        step["specification"],
        result,
        determine_autofill(step),
        save_step,
    )
