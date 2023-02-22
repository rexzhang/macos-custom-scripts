import dataclasses
from typing import Optional

from ualfred import (
    ICON_ACCOUNT,
    ICON_BURN,
    ICON_CLOCK,
    ICON_COLOR,
    ICON_COLOUR,
    ICON_EJECT,
    ICON_ERROR,
    ICON_FAVORITE,
    ICON_FAVOURITE,
    ICON_GROUP,
    ICON_HELP,
    ICON_HOME,
    ICON_INFO,
    ICON_NETWORK,
    ICON_NOTE,
    ICON_SETTINGS,
    ICON_SWIRL,
    ICON_SWITCH,
    ICON_SYNC,
    ICON_TRASH,
    ICON_USER,
    ICON_WARNING,
    ICON_WEB,
)

__all__ = [
    "ICON_ACCOUNT",
    "ICON_BURN",
    "ICON_CLOCK",
    "ICON_COLOR",
    "ICON_COLOUR",
    "ICON_EJECT",
    "ICON_ERROR",
    "ICON_FAVORITE",
    "ICON_FAVOURITE",
    "ICON_GROUP",
    "ICON_HELP",
    "ICON_HOME",
    "ICON_INFO",
    "ICON_NETWORK",
    "ICON_NOTE",
    "ICON_SETTINGS",
    "ICON_SWIRL",
    "ICON_SWITCH",
    "ICON_SYNC",
    "ICON_TRASH",
    "ICON_USER",
    "ICON_WARNING",
    "ICON_WEB",
    "AFWResponse",
    "afw_responses_to_feedback",
]


@dataclasses.dataclass
class AFWResponse:
    """
    https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """

    title: str
    arg: str

    subtitle: Optional[str] = None
    icon: str = ICON_NOTE
    valid: bool = False


def afw_responses_to_feedback(responses: list[AFWResponse]) -> list[dict]:
    result = list()
    for obj in responses:
        data = dataclasses.asdict(obj)
        for k in list(data.keys()):
            if data[k] is None:
                data.pop(k)

        result.append(data)

    return result
