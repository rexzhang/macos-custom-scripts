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

    subtitle: str | None = None
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


class AFWFuncAbc:
    def __init__(self, args: list[str], logger) -> None:
        self.args = args
        self.logger = logger

    @property
    def _data_defaulte(self) -> list:
        raise NotImplementedError

    @property
    def _data_tips(self) -> list:
        raise NotImplementedError

    @property
    def _data_success(self) -> list:
        raise NotImplementedError

    @property
    def _data_error(self) -> list:
        raise NotImplementedError

    def get_response_success(self) -> list[AFWResponse]:
        return [
            AFWResponse(
                title=title, arg=title, subtitle=subtitle, icon=ICON_INFO, valid=True
            )
            for title, subtitle in self._data_success
        ] + [
            AFWResponse(
                title=title, arg=title, subtitle=subtitle, icon=ICON_NOTE, valid=False
            )
            for title, subtitle in self._data_tips
        ]

    def get_response_fail(self) -> list[AFWResponse]:
        return (
            [
                AFWResponse(
                    title=title,
                    arg=title,
                    subtitle=subtitle,
                    icon=ICON_ERROR,
                    valid=False,
                )
                for title, subtitle in self._data_error
            ]
            + [
                AFWResponse(
                    title=title,
                    arg=title,
                    subtitle=subtitle,
                    icon=ICON_INFO,
                    valid=True,
                )
                for title, subtitle in self._data_defaulte
            ]
            + [
                AFWResponse(
                    title=title,
                    arg=title,
                    subtitle=subtitle,
                    icon=ICON_NOTE,
                    valid=False,
                )
                for title, subtitle in self._data_tips
            ]
        )

    def _process(self) -> bool:
        raise NotImplementedError

    def __call__(self) -> list[AFWResponse]:
        if self._process():
            return self.get_response_success()

        return self.get_response_fail()
