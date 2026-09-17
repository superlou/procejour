from enum import Enum

from procejour.models import Datasheet, StepMark


async def get_current_step_mark(id: str, datasheet: Datasheet) -> StepMark | None:
    return (
        await StepMark.filter(step_id=id, datasheet=datasheet)
        .order_by("-timestamp")
        .first()
    )


class Autofill(Enum):
    USER = "user"
    DATE = "date"


def determine_autofill(step) -> Autofill | None:
    if "observation" not in step:
        return None

    if step["observation"] == "name":
        return Autofill.USER
    elif step["observation"] == "date":
        return Autofill.DATE

    return None
