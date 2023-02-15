#!/usr/bin/python
# encoding: utf-8


import re

import arrow
from ualfred import ICON_CLOCK, ICON_ERROR, ICON_NOTE

DEFAULT_FEEDBACK = [
    {
        "title": 'Please enter timestamp, datetime string, "now", or space',
        "subtitle": "Examples: 1607609661, 2020-12-10 22:14:33, now",
        "valid": False,
        "icon": ICON_ERROR,
    },
    {
        "title": "Change time zone or time shift",
        "subtitle": "Examples: now +08, now +1d",
        "valid": False,
        "icon": ICON_ERROR,
    },
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


class Time(object):
    wf = None
    _query = None

    time = None
    now = False

    zone = None
    shift = None

    def __init__(self, wf):
        self.wf = wf

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        self._query = value.strip(" ")

    def do_parser(self):
        self.wf.logger.debug(
            "query string:{} {}".format(type(self.wf.args[0]), self.wf.args[0])
        )

        try:
            self.query = self.wf.args[0].encode("utf8")
        except IndexError:
            self.wf.logger.debug("parser workflow args failed.")
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
            self.wf.logger.debug("found zone info:{}".format(self.zone))
            return True

        r = re.match(RE_TIMEZONE, info)
        if r:
            self.query = query
            self.zone = info
            self.wf.logger.debug("found zone info:{}".format(self.zone))
            return True

        # time shift TODO
        r = re.match(RE_SHIFT, info)
        if r:
            self.query = query
            self.shift = info
            self.wf.logger.debug("found shift info:{}".format(self.shift))
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

        self.wf.logger.debug("parser datetime error,query string:{}".format(self.query))
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
            return DEFAULT_FEEDBACK

        if self.now:
            desc_now = "Now, "
        else:
            desc_now = ""

        f = list()
        for icon, force_utc, fmt, desc_format in FORMAT_LIST:
            # time shift
            if self.shift:
                desc_shift = "{}, ".format(self.shift)
            else:
                desc_shift = ""

            # time znone
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
            f.append(
                {
                    "title": value,
                    "subtitle": subtitle,
                    "valid": True,
                    "arg": value,
                    "icon": icon,
                }
            )

        return f


def do_convert(wf):
    time = Time(wf)
    time.do_parser()

    return time.get_feedback()
