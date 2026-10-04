import inspect
from typing import Callable, Literal

from nicegui import ui
from nicegui.binding import BindableProperty
from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.text_element import TextElement
from nicegui.elements.mixins.value_element import ValueElement


class PFButton(ui.button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.props("outline dense").classes("q-py-md w-full")


class PassFailButton(DisableableElement, ValueElement, ui.button_group):
    def __init__(self, value="unset"):
        super().__init__(value=value, on_value_change=lambda: self._render())
        self.props("outline dense").classes("w-full")
        self._render()

    @ui.refreshable_method
    def _render(self):
        with self:
            self.clear()
            match self.value:
                case "unset":
                    PFButton("P", on_click=lambda: self.set_value("pass"))
                    PFButton("F", on_click=lambda: self.set_value("fail"))
                case "pass":
                    with PFButton(
                        icon="check",
                        on_click=lambda: self.set_value("unset"),
                        color="green",
                    ):
                        ui.label("Pass").classes("gt-md")
                        ui.label("P").classes("lt-lg")
                case "fail":
                    with PFButton(
                        on_click=lambda: self.set_value("unset"), color="red"
                    ).props("icon-right=close"):
                        ui.label("Fail").classes("gt-md")
                        ui.label("F").classes("lt-lg")

        for button in self:
            if isinstance(button, ui.button):
                button.bind_enabled_from(self, "enabled")
