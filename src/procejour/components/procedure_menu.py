from nicegui import ui

from ..models import Datasheet, Procedure, ProcedureRev


async def procedure_menu(procedure: Procedure, procedure_rev: ProcedureRev):
    async def create_datasheet():
        datasheet = await Datasheet.create(procedure_rev=procedure_rev)
        ui.navigate.to(f"/datasheets/{datasheet.id}")

    async def delete():
        await procedure.delete()
        ui.navigate.to("/procedures")

    async def history():
        ui.navigate.to(f"/procedures/{procedure.id}")

    async def demo():
        ui.navigate.to(f"/procedures/{procedure.id}/demo")

    async def edit():
        ui.navigate.to(f"/procedures/{procedure.id}/edit")

    async def statistics():
        ui.navigate.to(f"/procedures/{procedure.id}/stats")

    with ui.row().classes("w-full items-end"):
        ui.button(icon="checklist_rtl", on_click=history).props("flat dense")
        ui.button(icon="bar_chart", on_click=statistics).props("flat dense")

        ui.space()

        with ui.dropdown_button("New datasheet", on_click=create_datasheet).props(
            "split outline"
        ):
            ui.item("Demo", on_click=demo)

        with ui.dropdown_button("Edit", on_click=edit).props("split outline"):
            ui.item("Delete", on_click=delete)

    ui.separator()
