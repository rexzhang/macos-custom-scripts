import dataclasses

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
    "AFWException",
    "afw_responses_to_feedback",
]


@dataclasses.dataclass
class AFWResponse:
    """
    https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """

    title: str
    subtitle: str | None = None
    icon: str = ICON_INFO

    arg: str | None = None
    valid: bool = True

    def __post_init__(self):
        if self.arg is not None:
            return

        if self.valid:
            self.arg = self.title


def afw_responses_to_feedback(responses: list[AFWResponse]) -> list[dict]:
    result = list()
    for obj in responses:
        data = dataclasses.asdict(obj)
        for k in list(data.keys()):
            if data[k] is None:
                data.pop(k)

        result.append(data)

    return result


class AFWException(Exception):
    pass


class AFWFuncAbc:
    icon_info = ICON_INFO
    icon_note = ICON_NOTE
    icon_error = ICON_ERROR

    responses: list[AFWResponse]

    def __init__(self, args: list[str], logger) -> None:
        self.args = args
        self.logger = logger
        self.responses = list()

    def append_response(self, response: AFWResponse):
        self.responses.append(response)

    def append_responses(self, responses: list[AFWResponse]):
        self.responses += responses

    @staticmethod
    def _afw_response_to_feedback_data(responses: list[AFWResponse]) -> list[dict]:
        result = list()
        for obj in responses:
            data = dataclasses.asdict(obj)
            for k in list(data.keys()):
                if data[k] is None:
                    data.pop(k)

            result.append(data)

        return result

    def get_reponse_error(self, message: str) -> AFWResponse:
        return AFWResponse(title=message, icon=self.icon_error, valid=False)

    def _process(self) -> bool:
        raise NotImplementedError

    def __call__(self) -> list[dict]:
        self.logger.debug(self.args)

        try:
            self._process()
        except AFWException as e:
            self.append_response(self.get_reponse_error(e))
            return self._afw_response_to_feedback_data(self.responses)

        if not self.responses:
            pass

        return self._afw_response_to_feedback_data(self.responses)
