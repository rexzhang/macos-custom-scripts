import re

import arrow
from afw_runtime import *

DEFAULT_RESPONSE = [
    AFWResponse(
        title='Please enter timestamp, datetime string, "now", or space',
        arg="",
        subtitle="Examples: 1607609661, 2020-12-10 22:14:33, now",
        icon=ICON_HELP,
    ),
    AFWResponse(
        title="Change time zone or time shift",
        arg="",
        subtitle="Examples: now +08, now +1d",
        icon=ICON_HELP,
    ),
]

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

FORMAT_LIST = (
    (ICON_NOTE, True, "X", "Timestamp(s)"),
    (ICON_NOTE, True, "x", "Timestamp(us)"),
    (ICON_CLOCK, False, "W, DDDD[th day]", "ISO Week date and Day for year"),
    (ICON_CLOCK, False, "YYYY-MM-DD HH:mm:ss", "Date and Time"),
    (ICON_CLOCK, False, "YYYY-MM-DD HH:mm:ss.SSSSSS", "Date and Time"),
    (ICON_CLOCK, False, arrow.FORMAT_RFC3339, "RFC3339 Format"),
    (  # https://www.w3.org/TR/NOTE-datetime
        ICON_CLOCK,
        False,
        "YYYY-MM-DDTHH:mm:ssZZ",
        "ISO 8601/W3C Format",
    ),
    (ICON_CLOCK, False, arrow.FORMAT_RFC850, "RFC850 Format"),
)

RE_TIMEZONE = "^[+-][0-9]{2}$"
RE_SHIFT = "^[+-][0-9]+[smhdwMy]$"


class Time:
    _query: str = None

    time = None
    now = False

    zone = None
    shift = None

    def __init__(self, args: list[str], logger):
        self.args = args
        self.logger = logger

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        self._query = value.strip(" ")

    def __call__(self, *args, **kwargs):
        self.do_parser()
        return self.get_feedback()

    def do_parser(self):
        query = self.args[0]
        self.logger.debug(f"query string:{type(query)} {query}")

        try:
            # self.query = self.wf.args[0].encode("utf8")
            self.query = query
        except IndexError:
            self.logger.debug("parser workflow args failed.")
            return False

        while True:
            if not self._parser_extend_info():
                break

        self._parser_datetime()
        self._apply_shift()

    def _parser_extend_info(self):
        """parser timezone, shift"""
        index = self.query.rfind(" ")
        if index == -1:
            query = ""
            info = self.query
        else:
            query = self.query[:index]
            info = self.query[index + 1 :].strip(" ")

        # time zone
        if info.upper() == "UTC" or info == "+00" or info == "-00":
            self.query = query
            self.zone = "UTC"
            self.logger.debug(f"found zone info:{self.zone}")
            return True

        r = re.match(RE_TIMEZONE, info)
        if r:
            self.query = query
            self.zone = info
            self.logger.debug(f"found zone info:{self.zone}")
            return True

        # time shift TODO
        r = re.match(RE_SHIFT, info)
        if r:
            self.query = query
            self.shift = info
            self.logger.debug(f"found shift info:{self.shift}")
            return True

        return False

    def _parser_datetime(self):
        """parser datetime"""
        try:
            if self.query.isdigit():
                self.time = arrow.get(int(self.query))
            else:
                self.time = arrow.get(self.query)

            return True

        except arrow.ParserError:
            pass

        if self.query == "now" or self.query == "":
            self.now = True
            self.time = arrow.now()
            return True

        self.logger.debug(f"parser datetime error,query string:{self.query}")
        return False

    def _apply_shift(self):
        if self.time is None or self.shift is None:
            return

        index = len(self.shift) - 1
        unit = self.shift[index]
        number = int(self.shift[:index])
        kwargs = {
            SHIFT_UNIT_MAP[unit]: number,
        }
        self.time = self.time.shift(**kwargs)

    def get_feedback(self):
        if self.time is None:
            return DEFAULT_RESPONSE

        if self.now:
            desc_now = "Now, "
        else:
            desc_now = ""

        responses = list()
        for icon, force_utc, fmt, desc_format in FORMAT_LIST:
            # time shift
            if self.shift:
                desc_shift = f"{self.shift}, "
            else:
                desc_shift = ""

            # time zone
            if force_utc:
                self.time = self.time.to("UTC")
                desc_zone = "UTC"
            elif self.zone and not force_utc:
                self.time = self.time.to(self.zone)
                desc_zone = self.zone
            else:
                self.time = self.time.to("local")
                desc_zone = "Local"

            value = self.time.format(fmt)
            subtitle = "{}{}[{}] {}".format(
                desc_now, desc_shift, desc_zone, desc_format
            )
            responses.append(
                AFWResponse(
                    title=value, arg=value, subtitle=subtitle, icon=icon, valid=True
                )
            )

        return responses


def main(args: list[str], logger) -> list[AFWResponse]:
    time_convert = Time(args, logger)
    return time_convert()
