from contextlib import asynccontextmanager

from nicegui import ui

from ..models import Datasheet, ProcedureRev, User


@asynccontextmanager
async def datasheet_header(
    procedure_rev: ProcedureRev, datasheet: Datasheet, current_user: User
):
    with ui.row().classes("w-full items-center"):
        ui.label(procedure_rev.title).classes("text-h6")
        ui.separator().props("vertical")
        ui.label(await datasheet.title)
        ui.space()
        yield
