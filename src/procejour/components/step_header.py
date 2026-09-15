from nicegui import ui


def header_step(step):
    with ui.item() as header:
        with ui.item_section().classes("col-span-1"):
            ui.label(step["num"])
        with ui.item_section().classes("col-span-6"):
            ui.label(step["heading"])
        with ui.item_section().classes("col-span-5"):
            pass

    header.classes("grid grid-cols-12 w-full")
    header.style("border-bottom: 1px solid #d0d0d8; background: #f4f4f8")
    header.props(f"id={step['id']}")
