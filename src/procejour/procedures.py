import json

import plotly.graph_objects as go
from nicegui import ui
from pandas import DataFrame

from . import humanize
from .auth import CurrentUser
from .components.procedure_header import procedure_header
from .components.procedure_menu import procedure_menu
from .components.sidebar_menu import sidebar_menu
from .datasheets import build_datasheet
from .models import Datasheet, Procedure, ProcedureRev
from .observation_check import observation_value


@ui.page("/procedures")
async def get_procedures(current_user: CurrentUser):
    async def create_new_procedure():
        procedure = await Procedure.create()
        await ProcedureRev.create(procedure=procedure, title="New Procedure")
        ui.navigate.to(f"/procedures/{procedure.id}")

    procedures = await Procedure.all()

    sidebar_menu(current_user)

    with ui.list():
        for procedure in procedures:
            current_rev = await procedure.current_rev
            with ui.item().classes("items-center"):
                ui.link(current_rev.title, f"/procedures/{procedure.id}")

    ui.button("New", on_click=create_new_procedure)


@ui.page("/procedures/{id}")
async def show_procedure(id: int, current_user: CurrentUser):
    procedure = await Procedure.get(id=id)
    current_rev = await procedure.current_rev

    async def create_datasheet():
        datasheet = await Datasheet.create(procedure_rev=current_rev)
        ui.navigate.to(f"/datasheets/{datasheet.id}")

    async def delete():
        await procedure.delete()
        ui.navigate.to("/procedures")

    with ui.dialog() as delete_dialog, ui.card():
        with ui.card_section():
            ui.label("Delete procedure?").classes("text-h6")

        with ui.card_section():
            ui.label("This will delete this procedure and all associated datasheets.")

        with ui.card_section():
            with ui.row():
                ui.button("Cancel", on_click=delete_dialog.close)
                ui.button("Delete", on_click=delete)

    sidebar_menu(current_user)
    await procedure_header(current_rev)
    await procedure_menu(procedure, current_rev)

    with ui.grid(columns="auto 1fr auto auto").classes("w-full"):
        procedure_revs = await procedure.revs.order_by("-saved_at")

        ui.label("ID").classes("text-weight-bold")
        ui.label("Title").classes("text-weight-bold")
        ui.label("Created").classes("text-weight-bold")
        ui.label("Procedure Revision").classes("text-weight-bold")

        for rev in procedure_revs:
            rev_saved = humanize.timestamp(rev.saved_at)
            datasheets = await rev.datasheets.order_by("-created_at")

            for i, datasheet in enumerate(datasheets):
                ui.label(f"#{datasheet.id}")
                created_at = humanize.timestamp(datasheet.created_at)

                title = await datasheet.title
                title = title if title != "" else "(untitled)"
                ui.link(title, f"/datasheets/{datasheet.id}")
                ui.label(created_at)
                ui.label(rev_saved if i == 0 else "")


@ui.page("/procedures/{id}/edit")
async def edit_procedure(id: int, current_user: CurrentUser):
    procedure = await Procedure.get(id=id)
    current_rev = await procedure.current_rev

    async def save_procedure():
        await current_rev.fetch_related("datasheets")
        if len(current_rev.datasheets) == 0:
            rev = current_rev
        else:
            rev = ProcedureRev(procedure=procedure)

        rev.title = title_input.value
        rev.ref_doc = ref_doc_input.value
        rev.ref_rev = ref_rev_input.value
        rev.datasheet_title = datasheet_title_input.value

        response = await steps_input.run_editor_method("get")
        if "json" in response:
            current_json = response["json"]
        elif "text" in response:
            current_json = json.loads(response["text"])

        rev.steps = current_json
        await rev.save()
        ui.notify("Saved")

    sidebar_menu(current_user)
    await procedure_header(current_rev)
    await procedure_menu(procedure, current_rev)

    title_input = ui.input("Title", value=current_rev.title)
    with ui.row():
        ref_doc_input = ui.input("Reference Document", value=current_rev.ref_doc)
        ref_rev_input = ui.input("Reference Revision", value=current_rev.ref_rev)
    datasheet_title_input = ui.input(
        "Datasheet Title", value=current_rev.datasheet_title
    )

    steps_input = ui.json_editor(
        {"content": {"json": current_rev.steps}, "mode": "text"}
    ).classes("w-full h-100")
    ui.button("Save", on_click=save_procedure)


@ui.page("/procedures/{id}/demo")
async def show_procedure_demo(id: int, current_user: CurrentUser):
    procedure = await Procedure.get(id=id)
    procedure_rev = await procedure.current_rev
    await build_datasheet(None, procedure_rev, current_user)


@ui.page("/procedures/{id}/stats")
async def show_procedure_stats(id: int, current_user: CurrentUser):
    procedure = await Procedure.get(id=id)
    current_rev = await procedure.current_rev

    sidebar_menu(current_user)
    await procedure_header(current_rev)
    await procedure_menu(procedure, current_rev)

    datapoints = []
    for step in current_rev.steps:
        datapoints += await get_step_values(procedure, step)

    df = DataFrame(datapoints)

    for step in current_rev.steps:
        if "heading" in step:
            ui.label(step["heading"])
        else:
            ui.label(f"ID: {step['id']}")
            step_df = df[df.step_id == step["id"]]
            if len(step_df) > 0:
                plot = go.Scatter(x=step_df.timestamp, y=step_df.value, mode="markers")
                fig = go.Figure(plot)
                fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                ui.plotly(fig).classes("w-full h-40")


async def get_step_values(procedure: Procedure, step: dict) -> list[dict]:
    # For each datasheet for this procedure (including other revs),
    # get the latest StepMark, and it's timestamp and value.
    procedure_revs = [rev.id for rev in await procedure.revs]
    datasheets = await Datasheet.filter(procedure_rev_id__in=procedure_revs)

    datapoints = []

    for datasheet in datasheets:
        step_mark = await datasheet.step_mark_by_id(step["id"])
        if step_mark and "value" in step_mark.observation:
            try:
                value = observation_value(
                    step_mark.observation["value"], step["observation"]
                )
                datapoints.append(
                    {
                        "step_id": step["id"],
                        "value": value,
                        "timestamp": step_mark.timestamp,
                    }
                )
            except TypeError:
                pass

    return datapoints
