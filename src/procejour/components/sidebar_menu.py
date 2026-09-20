from nicegui import ui

from .. import auth
from ..models import User


def sidebar_menu(
    current_user: User,
    expanded=True,
    page_links: list[tuple[str, str]] | None = None,
):
    with ui.left_drawer(top_corner=True, bordered=True, value=expanded) as left_drawer:
        with ui.row().classes("w-full items-center flex-nowrap"):
            with ui.link(target="/").classes(
                "items-center inline-flex whitespace-nowrap gap-2"
            ):
                ui.icon("home")
                ui.label("Home")
            ui.space()
            ui.button(icon="menu_open", on_click=left_drawer.toggle).props("flat dense")

        ui.link("Procedures", "/procedures")

        ui.separator()

        if page_links:
            with ui.list().props("dense"):
                for target, link in page_links:
                    with ui.item():
                        ui.link(link, target)

            ui.separator()

        ui.html(f"Signed in as <b>{current_user.email}</b>").classes("text-no-wrap")
        with ui.link(target="/user"):
            with ui.row().classes("items-center no-wrap"):
                ui.icon("person")
                ui.label("Profile")

        if current_user.admin:
            with ui.link(target="/admin"):
                with ui.row().classes("items-center no-wrap"):
                    ui.icon("settings")
                    ui.label("Admin")

        with ui.button(on_click=auth.logout).props("flat dense"):
            with ui.row().classes("items-center no-wrap"):
                ui.icon("logout")
                ui.label("Sign out")

    left_drawer.props("behavior=desktop").style("background: #fdfdff;")

    with ui.page_sticky(position="top-left", x_offset=0, y_offset=0):
        ui.button(icon="menu", on_click=left_drawer.toggle).props(
            "flat dense"
        ).bind_visibility_from(left_drawer, "value", value=False)
