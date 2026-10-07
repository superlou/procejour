from nicegui import app, ui
from tortoise.contrib.fastapi import register_tortoise

from procejour.config import media_path

from . import admin, auth, datasheets, procedures, tests, users  # noqa: F401
from .auth import CurrentUser
from .components.sidebar_menu import sidebar_menu
from .orm import TORTOISE_ORM

db_url: str = TORTOISE_ORM["connections"]["default"]
models: list[str] = TORTOISE_ORM["apps"]["models"]["models"]
register_tortoise(
    app, db_url=db_url, modules={"models": models}, add_exception_handlers=True
)

media_path.mkdir(parents=True, exist_ok=True)
app.add_static_files("/media", "./data/media")


@ui.page("/")
def home(current_user: CurrentUser):
    sidebar_menu(current_user)
    ui.link("Procedures", "/procedures")


secret = "osLj63o3qH4Kncmv6x6vRmyiqD8g/nPEMQQEl7JFZh4="
ui.run(
    storage_secret=secret,
    fastapi_docs=True,
    title="Procejour",
    favicon="✅",
)
