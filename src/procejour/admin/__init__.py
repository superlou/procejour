from fastapi import HTTPException, status
from nicegui import ui

from ..auth import CurrentUser
from ..components.admin_menu import AdminMenu
from .users import users


@ui.page("/admin")
@ui.page("/admin/{_:path}")
async def admin(user: CurrentUser):
    if not user.admin:
        ui.label("Forbidden")
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    with ui.row().classes("w-full"):
        with ui.column().classes("col-2"):
            AdminMenu().display()
        with ui.column().classes("col-9"):
            ui.sub_pages(
                {
                    "/admin": admin_index,
                    "/admin/users": lambda: users(user),
                }
            ).classes("w-full")


async def admin_index():
    ui.page_title("Admin")
    ui.label("Admin")
    ui.label("These settings configure the Procejour application.")
