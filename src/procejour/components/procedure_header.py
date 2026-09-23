from nicegui import ui

from ..models import ProcedureRev


async def procedure_header(procedure_rev: ProcedureRev):
    with ui.row().classes("w-full items-center"):
        ui.label(procedure_rev.title).classes("text-h6")
        ui.separator().props("vertical")
        ui.label(procedure_rev.ref_doc)
        ui.label(procedure_rev.ref_rev)
