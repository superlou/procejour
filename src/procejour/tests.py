from nicegui import ui
from procejour.components.done_button import DoneButton
from procejour.components.pass_fail_button import PassFailButton


@ui.page("/tests/controls")
def test_controls():
    state = {
        "enabled": True
    }

    ui.checkbox("Enabled").bind_value(state, "enabled")

    ui.label("DoneButton")
    DoneButton().bind_enabled_from(state, "enabled")

    ui.label("PassFailButton")
    PassFailButton().bind_enabled_from(state, "enabled")
