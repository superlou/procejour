import json

from nicegui import ui

from procejour.datasheets import build_procedure_step

from . import auth, humanize
from .auth import CurrentUser
from .components.sidebar_menu import sidebar_menu
from .models import Datasheet, Procedure, ProcedureRev


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

    ui.label(current_rev.title).classes("text-h2")
    with ui.row():
        ui.label(current_rev.ref_doc)
        ui.label(current_rev.ref_rev)

    with ui.row().classes("w-full"):
        with ui.column().classes("col"):
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

        with ui.column().classes("col"):
            with ui.list().props("bordered separator"):
                with ui.item():
                    ui.button("Create datasheet", on_click=create_datasheet)

                with ui.item():
                    ui.link("Demo", f"/procedures/{id}/demo")

                with ui.item():
                    ui.link("Edit", f"/procedures/{id}/edit")

                with ui.item():
                    ui.button("Delete", on_click=delete_dialog.open).props(
                        "flat color=negative"
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

    sidebar_menu(current_user)
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


@ui.page("/procedures/{id}/demo")
async def show_procedure_demo(id: int, current_user: CurrentUser):
    procedure = await Procedure.get(id=id)
    procedure_rev = await procedure.current_rev

    header_links = [
        (f"#{step['id']}", f"{step['num']} {step['heading']}")
        for step in procedure_rev.steps
        if "heading" in step
    ]

    sidebar_menu(current_user, page_links=header_links)
    ui.label(f"{procedure_rev.title} - Demo")

    with ui.list().classes("w-full"):
        for step in procedure_rev.steps:
            await build_procedure_step(None, step, current_user)
