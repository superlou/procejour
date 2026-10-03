from nicegui import ui
from procejour.components.done_button import DoneButton
from procejour.components.pass_fail_button import PassFailButton


@ui.page("/tests/controls")
def test_controls():
    state = {
        "enabled": True,
        "pass_fail": "unset",
    }

    ui.checkbox("Enabled").bind_value(state, "enabled")

    ui.label("DoneButton")
    DoneButton().bind_enabled_from(state, "enabled")

    ui.label("PassFailButton")
    ui.select(["unset", "pass", "fail"]).bind_value(state, "pass_fail")
    (PassFailButton()
        .bind_enabled_from(state, "enabled")
        .bind_value(state, "pass_fail")
        .on_value_change(lambda val: ui.notify(val)))
