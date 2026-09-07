import json

from nicegui import ui

from procejour.models import Datasheet, Procedure


@ui.page("/procedures")
async def get_procedures():
    async def create_new_procedure():
        procedure = Procedure(title="New procedure")
        await procedure.save()
        ui.navigate.to(f"/procedures/{procedure.id}")

    async def create_new_datasheet(procedure: Procedure):
        datasheet = Datasheet(procedure=procedure)
        await datasheet.save()
        print(datasheet.id)
        ui.navigate.to(f"/datasheets/{datasheet.id}")

    procedures = await Procedure.all()

    with ui.list():
        for procedure in procedures:
            with ui.item().classes("items-center"):
                ui.link(procedure.title, f"/procedures/{procedure.id}")
                ui.html("&nbsp;")
                ui.button(
                    "New datasheet",
                    on_click=lambda p=procedure: create_new_datasheet(p),
                ).props("flat")

                await procedure.fetch_related("datasheets")
                with ui.list():
                    for datasheet in procedure.datasheets:
                        with ui.item():
                            ui.link(
                                f"Datasheet {datasheet.id}",
                                f"/datasheets/{datasheet.id}",
                            )

    ui.button("New", on_click=create_new_procedure)


@ui.page("/procedures/{id}")
async def edit_procedure(id: int):
    procedure = await Procedure.get(id=id)

    async def save_procedure():
        procedure.title = title_input.value
        procedure.ref_doc = ref_doc_input.value
        procedure.ref_rev = ref_rev_input.value

        response = await steps_input.run_editor_method("get")
        if "json" in response:
            current_json = response["json"]
        elif "text" in response:
            current_json = json.loads(response["text"])

        procedure.steps = current_json
        await procedure.save()
        ui.notify("Saved")

    ui.link("Procedures", "/procedures")
    title_input = ui.input("Title", value=procedure.title)
    with ui.row():
        ref_doc_input = ui.input("Reference Document", value=procedure.ref_doc)
        ref_rev_input = ui.input("Reference Revision", value=procedure.ref_rev)

    steps_input = ui.json_editor(
        {"content": {"json": procedure.steps}, "mode": "text"}
    ).classes("w-full h-100")
    ui.button("Save", on_click=save_procedure)
