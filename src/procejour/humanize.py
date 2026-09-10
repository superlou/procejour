from datetime import datetime


def timestamp(dt: datetime) -> str:
    return dt.strftime("%m/%d/%Y %I:%M %p")
