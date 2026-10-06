from collections import Counter
from typing import Coroutine, Literal

from nicegui import binding, ui

from procejour.auth import CurrentUser
from procejour.components.datasheet_header import datasheet_header
from procejour.components.sidebar_menu import sidebar_menu
from procejour.components.step import (
    ObservationStepArgs,
    PassFailStepArgs,
    no_observation_step,
    observation_step,
    pass_fail_step,
)
from procejour.components.step_header import header_step
from procejour.datasheet_utils import (
    Autofill,
    determine_autofill,
    get_current_step_mark,
)
from procejour.models import (
    Datasheet,
    DatasheetReview,
    ProcedureRev,
    ReviewResult,
    StepMark,
    StepMarkPassFail,
    User,
)


@ui.page("/datasheets/{datasheet_id}")
async def run_datasheet(datasheet_id: int, current_user: CurrentUser):
    datasheet = await Datasheet.get(id=datasheet_id).prefetch_related("procedure_rev")
    procedure_rev = datasheet.procedure_rev
    await build_datasheet(datasheet, procedure_rev, current_user)


async def build_datasheet(
    datasheet: Datasheet | None, procedure_rev: ProcedureRev, current_user: CurrentUser
):
    state = {"review_visible": False}

    await procedure_rev.fetch_related("procedure")
    header_links = [
        (f"#{step['id']}", f"{step['num']} {step['heading']}")
        for step in procedure_rev.steps
        if "heading" in step
    ]
    header_links.insert(
        0, (f"/procedures/{procedure_rev.procedure.id}", procedure_rev.title)
    )

    sidebar_menu(current_user, page_links=header_links)

    def toggle_review():
        state["review_visible"] = not state["review_visible"]

    async def save_review():
        match review_result.value:
            case "Incomplete":
                result = ReviewResult.INCOMPLETE
            case "Pass":
                result = ReviewResult.PASS
            case "Fail":
                result = ReviewResult.FAIL
            case _:
                result = ReviewResult.INCOMPLETE

        review = DatasheetReview(
            datasheet=datasheet,
            reviewer=current_user,
            result=result,
            comments=review_comments.value,
        )
        await review.save()
        state["review_visible"] = False
        review_result.value = "Incomplete"
        review_comments.value = ""

    if datasheet:
        async with datasheet_header(procedure_rev, datasheet, current_user):
            if current_user.qa:
                ui.button("Review", on_click=toggle_review).props("outline")

            if await datasheet.fully_reviewed:
                ui.icon("verified")

    else:
        ui.label(procedure_rev.title + " (demo)").classes("text-h6")

    with (
        ui.card()
        .bind_visibility_from(state, "review_visible")
        .classes("w-full")
        .props("flat bordered")
        .tight()
    ):
        with ui.card_section():
            ui.label("Review")
            review_result = ui.select(
                ["Incomplete", "Pass", "Fail"], label="Status", value="Incomplete"
            )
            review_comments = ui.textarea("Comments").classes("w-full")

        ui.separator()

        with ui.card_actions():
            ui.button("Submit", on_click=save_review)

    step_focus_targets = {}

    async def advance(current_step_id: int):
        # todo Kinda gross
        found = False
        next_focus_target = None
        for step_id, focus_target in step_focus_targets.items():
            if step_id == current_step_id:
                found = True
                continue

            if found and focus_target is not None:
                next_focus_target = focus_target
                break

        if next_focus_target is not None:
            focus_target.take_focus()

    with ui.list().classes("w-full"):
        for step in procedure_rev.steps:
            step_focus_targets[step["id"]] = await build_step(
                datasheet, step, current_user, advance
            )


async def build_step(
    datasheet: Datasheet | None, step: dict, current_user: User, advance: Coroutine
):
    print(step)

    if step.get("heading", False):
        header_step(step)
    elif step.get("specification", False):
        return await build_pass_fail_step(datasheet, step, current_user, advance)
    elif "observation" in step:
        return await build_observation_step(datasheet, step, current_user, advance)
    else:
        return await build_no_observation_step(datasheet, step, current_user, advance)


async def build_no_observation_step(
    datasheet: Datasheet | None, step: dict, current_user: User, advance: Coroutine
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

    return await no_observation_step(
        step["num"],
        step["action"],
        done,
        save_step,
        advance=lambda: advance(step["id"]),
    )


async def build_observation_step(
    datasheet: Datasheet | None, step: dict, current_user: User, advance: Coroutine
):
    args = ObservationStepArgs(
        num=step["num"],
        action=step["action"],
        autofill=determine_autofill(step),
    )

    if datasheet:
        step_mark = await get_current_step_mark(step["id"], datasheet)
        args.observation = (
            step_mark.observation["value"]
            if step_mark and "value" in step_mark.observation
            else ""
        )
        args.done = step_mark.pass_fail == StepMarkPassFail.DONE if step_mark else False

    async def save_step(observation, done):
        if datasheet is None:
            return

        step_mark = StepMark(
            datasheet=datasheet, step_id=step["id"], comment="", set_by=current_user
        )
        step_mark.observation = {"value": observation}
        step_mark.pass_fail = StepMarkPassFail.DONE if done else StepMarkPassFail.UNSET
        await step_mark.save()

    if step["observation"].startswith("decimal"):
        tokens = step["observation"].split(" ")
        if len(tokens) > 1:
            args.units = tokens[1]

    return await observation_step(
        args,
        save_step,
        advance=lambda: advance(step["id"]),
    )


async def build_pass_fail_step(
    datasheet: Datasheet | None, step: dict, current_user: User, advance: Coroutine
):
    args = PassFailStepArgs(
        num=step["num"],
        action=step["action"],
        specification=step["specification"],
        autofill=determine_autofill(step),
    )

    if datasheet:
        step_mark = await get_current_step_mark(step["id"], datasheet)
        args.observation = (
            step_mark.observation["value"]
            if step_mark and "value" in step_mark.observation
            else ""
        )
        match step_mark:
            case StepMark(pass_fail=StepMarkPassFail.PASS):
                args.result = "pass"
            case StepMark(pass_fail=StepMarkPassFail.FAIL):
                args.result = "fail"
            case _:
                args.result = "unset"

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

    if step["observation"].startswith("decimal"):
        tokens = step["observation"].split(" ")
        if len(tokens) > 0:
            args.format = tokens[0]
        if len(tokens) > 1:
            args.units = tokens[1]

    return await pass_fail_step(
        args,
        save_step,
        advance=lambda: advance(step["id"]),
    )
