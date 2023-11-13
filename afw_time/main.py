import re
from collections import deque
from logging import Logger

import arrow

from afw_runtime import ICON_CLOCK, AFWException, AFWFuncAbc, AFWResponse

SHIFT_UNIT_MAP = {
    "ms": "microseconds",
    "s": "seconds",
    "m": "minutes",
    "h": "hours",
    "d": "days",
    "w": "weeks",
    "M": "months",
    "q": "quarters",
    "y": "years",
}


RE_TIMEZONE = "^[+-][0-9]{2}$"
RE_SHIFT = "^[+-][0-9]+[smhdwMy]$"


class TimeData:
    query: str
    logger: Logger

    time: arrow.Arrow | None = None
    zone: str = "local"
    shifts: list = list()

    def __init__(self, query: str, logger: Logger) -> None:
        self.query = query
        self.logger = logger

    def _is_ext(self, data_str: str) -> bool:
        # time shift
        r = re.match(RE_SHIFT, data_str)
        if r:
            self.logger.debug(f"found shift info:{data_str}")

            index = len(data_str) - 1
            unit = data_str[index]
            number = int(data_str[:index])
            kwargs = {
                SHIFT_UNIT_MAP[unit]: number,
            }
            self.shifts.append(kwargs)

            # self.time = self.time.shift(**kwargs)
            return True

        # time zone
        r = re.match(RE_TIMEZONE, data_str)
        if r:
            self.logger.debug(f"found zone info:{data_str}")
            self.zone = data_str

            # self.time = self.time.to(self.zone)
            return True

        return False

    def __call__(self) -> "TimeData":
        query_deque = deque(self.query.split(" "))
        self.logger.debug(f"query_deque:{query_deque}")

        for _ in range(len(query_deque)):
            data = query_deque.pop()
            if not self._is_ext(data):
                query_deque.append(data)
                break

        time_base_str = " ".join(query_deque)
        self.logger.debug(f"query_deque:{query_deque}")
        self.logger.debug(f"time_base_str:{time_base_str}")

        try:
            if time_base_str == "" or time_base_str.lower() == "now":
                self.time = arrow.now()

            elif time_base_str.isdigit():
                self.time = arrow.get(int(time_base_str))

            elif time_base_str.replace(".", "", 1).isdigit():
                self.time = arrow.get(float(time_base_str))

            else:
                self.time = arrow.get(time_base_str)

            if self.time is None:
                raise ValueError()

        except (arrow.ParserError, ValueError) as e:
            self.logger.warning(
                f"Time paser failed, query={self.query}, time_base_str={time_base_str}, {e}"
            )
            raise AFWException(f"Bad format: {time_base_str}")

        self.time = self.time.to(self.zone)
        for kwargs in self.shifts:
            self.time = self.time.shift(**kwargs)

        return self


class AFWFunc(AFWFuncAbc):
    icon_info = ICON_CLOCK

    _time: arrow.Arrow | None = None
    _tips = False

    def make_responses_from_time(self) -> list[AFWResponse]:
        return [
            AFWResponse(
                title=self._time.time.to("UTC").format("X"),
                subtitle="The time[UTC] as a Timestamp(s).",
                icon=self.icon_info,
            ),
            AFWResponse(
                title=self._time.time.to("UTC").format("x"),
                subtitle="The time[UTC] as a Timestamp(us).",
                icon=self.icon_info,
            ),
            AFWResponse(
                title=self._time.time.format("W, DDDD[th day]"),
                subtitle=f"The time[{self._time.zone}] as ISO Week date and Day for year.",
                icon=self.icon_info,
                arg=self._time.time.format("W"),
            ),
            AFWResponse(
                title=self._time.time.format("YYYY-MM-DD HH:mm:ss"),
                subtitle=f"The time[{self._time.zone}] as Date and Time.",
                icon=self.icon_info,
            ),
            AFWResponse(
                title=self._time.time.format(arrow.FORMAT_RFC3339),
                subtitle=f"The time[{self._time.zone}] as RFC3339 Formaself._time.",
                icon=self.icon_info,
            ),
            AFWResponse(
                # https://www.w3.org/TR/NOTE-datetime
                title=self._time.time.format("YYYY-MM-DDTHH:mm:ssZZ"),
                subtitle=f"The time[{self._time.zone}] as ISO 8601/W3C Formaself._time.",
                icon=self.icon_info,
            ),
            AFWResponse(
                title=self._time.time.format(arrow.FORMAT_RFC850),
                subtitle=f"The time[{self.zone}] as RFC850 Formaself._time.",
                icon=self.icon_info,
            ),
        ]

    def append_tips(self):
        self.responses += [
            AFWResponse(
                title="Please enter timestamp, datetime string, 'now', or space",
                # subtitle=example1,
                subtitle="Examples: 1607609661, 2020-12-10 22:14:33, now",
                icon=self.icon_note,
                arg="1607609661",
            ),
            AFWResponse(
                title="Change time zone or/and time shift",
                subtitle="Examples: now +08, now +1d, now +08 +1d",
                icon=self.icon_note,
                arg="now +08 +1d",
            ),
        ]

    def append_error_message(self, message: str):
        self.responses.append(
            AFWResponse(title=message, icon=self.icon_error, valid=False)
        )

    def _guess_input(self) -> arrow.Arrow | None:
        if len(self.args) == 0:
            self._tips = True
            query = "now"
        else:
            query = self.args[0]

        try:
            t = TimeData(query=query, logger=self.logger)()
        except AFWException as e:
            self.append_error_message(f"Bad query: {e}")
            self._tips = True
            return None

        return t

    def _createa_responses(self):
        if self._time:
            self.append_responses(self.make_responses_from_time())

        if self._tips:
            self.append_tips()

    def _process(self) -> None:
        self._time = self._guess_input()
        if self._time is None:
            self._tips = True

        self.logger.debug(f"self._time:{self._time}")
        self._createa_responses()
        return


def main(args: list[str], logger: Logger) -> list[dict]:
    return AFWFunc(args, logger)()
