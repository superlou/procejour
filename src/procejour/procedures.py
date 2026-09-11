import json

from nicegui import ui

from procejour.auth import CurrentUser
from procejour.components.header import header
from procejour.models import Datasheet, Procedure, ProcedureRev

from . import humanize


@ui.page("/procedures")
async def get_procedures(current_user: CurrentUser):
    async def create_new_procedure():
        procedure = await Procedure.create()
        await ProcedureRev.create(procedure=procedure, title="New Procedure")
        ui.navigate.to(f"/procedures/{procedure.id}")

    procedures = await Procedure.all()

    header(current_user)
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

    header(current_user)

    ui.link("Procedures", "/procedures")
    ui.label(current_rev.title)
    with ui.row():
        ui.label(current_rev.ref_doc)
        ui.label(current_rev.ref_rev)
    ui.link("Edit", f"/procedures/{id}/edit")

    ui.button("Create datasheet", on_click=create_datasheet)

    ui.label("Datasheets")
    procedure_revs = await procedure.revs.order_by("-saved_at")
    with ui.list().props("separator"):
        for rev in procedure_revs:
            ui.item_label(humanize.timestamp(rev.saved_at)).props("header")

            ui.separator()

            for datasheet in await rev.datasheets.order_by("-created_at"):
                with ui.item():
                    ui.link(
                        f"{datasheet.id} {await datasheet.title}",
                        f"/datasheets/{datasheet.id}",
                    )


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

    header(current_user)
    ui.link("Procedures", "/procedures")
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
