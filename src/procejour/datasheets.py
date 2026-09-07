from nicegui import ui

from procejour.models import Datasheet, StepMark


@ui.page("/datasheets/{datasheet_id}")
async def run_datasheet(datasheet_id: int):
    datasheet = await Datasheet.get(id=datasheet_id).prefetch_related("procedure")
    procedure = datasheet.procedure

    ui.label(procedure.title)

    with ui.list().classes("w-full"):
        for step in procedure.steps:
            await build_procedure_step(
                datasheet, step, pass_fail="specification" in step
            )


async def pass_fail_button():
    with ui.button_group().props("outline"):
        ui.button("P").props("outline")
        ui.button("F").props("outline")


async def build_procedure_step(datasheet: Datasheet, step: dict, pass_fail=True):
    print(step)

    step_mark = (
        await StepMark.filter(step_id=step["id"], datasheet=datasheet)
        .order_by("-timestamp")
        .first()
    )
    observation = step_mark.observation["value"] if step_mark else ""

    units = None
    if step["observation"].startswith("decimal"):
        tokens = step["observation"].split(" ")
        if len(tokens) > 1:
            units = tokens[1]

    async def save_step():
        step_mark = StepMark(datasheet=datasheet, step_id=step["id"], comment="")
        step_mark.observation = {"value": observation_input.value}
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
            observation_input.on("blur", save_step)  # todo only if changed
        with ui.item_section().classes("col-1"):
            if pass_fail:
                await pass_fail_button()
