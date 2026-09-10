from nicegui import context, ui

from .. import auth
from ..models import User


def header(user: User):
    with ui.header().classes("text-white").style("background: #14497e; padding: 0px;"):
        with ui.element("q-toolbar").classes("q-py-sm q-px-md"):
            with ui.link(target="/").classes("text-white"):
                ui.button(icon="sym_o_calendar_clock", text="Procejour").props(
                    "dense flat color=white no-caps"
                ).classes("items-center")

            ui.space()

            with ui.button(icon="person").props("round dense flat color=white no-caps"):
                with ui.menu().props():
                    with (
                        ui.menu_item(auto_close=False)
                        .classes("items-center text-caption")
                        .style("pointer-events: none; cursor: default")
                    ):
                        ui.html(f"Signed in as <b>{user.email}</b>").classes(
                            "text-no-wrap"
                        )

                    ui.separator()

                    with ui.menu_item(on_click=lambda: ui.navigate.to("/user")):
                        with ui.row().classes("items-center no-wrap"):
                            ui.icon("person")
                            ui.label("Profile")

                    if user.admin:
                        with ui.menu_item(on_click=lambda: ui.navigate.to("/admin")):
                            with ui.row().classes("items-center no-wrap"):
                                ui.icon("settings")
                                ui.label("Admin")

                    with ui.menu_item(on_click=auth.logout):
                        with ui.row().classes("items-center no-wrap"):
                            ui.icon("logout")
                            ui.label("Sign out").classes("text-no-wrap")
