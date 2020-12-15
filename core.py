#!/usr/bin/python
# encoding: utf-8


import re

import arrow
from workflow import ICON_CLOCK, ICON_NOTE, ICON_ERROR

DEFAULT_FEEDBACK = [{
    'title': 'Please enter timestamp, datetime string, "now", or space',
    'subtitle': 'Examples: 1607609661, 2020-12-10 22:14:33, now +08',
    'valid': False,
    'icon': ICON_ERROR,
}]

FORMAT_LIST = (
    (ICON_NOTE, True, 'X', 'Timestamp(s)'),
    (ICON_NOTE, True, 'x', 'Timestamp(us)'),
    (
        ICON_CLOCK, False, 'YYYY-MM-DD HH:mm:ss', 'Date and Time'
    ),
    (
        ICON_CLOCK, False, 'W, DDDD[th day]',
        'ISO Week date and Day for year'
    ),
    (  # https://www.w3.org/TR/NOTE-datetime
        ICON_CLOCK, False, 'YYYY-MM-DDTHH:mm:ssZZ',
        'W3C Format'
    ),
    (ICON_CLOCK, False, arrow.FORMAT_RFC850, 'RFC850 Format'),
    # FORMAT_RFC3339
)

RE_TIMEZONE = '^[+-][0-9]{2}$'
RE_SHIFT = '^[+-][0-9]+[smhdmy]$'


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
        self._query = value.strip(' ')

    def do_parser(self):
        self.wf.logger.debug('query string:{} {}'.format(
            type(self.wf.args[0]), self.wf.args[0])
        )

        try:
            self.query = self.wf.args[0].encode('utf8')
        except IndexError:
            self.wf.logger.debug('parser workflow args failed.')
            return False

        while True:
            if not self._parser_extend_info():
                break

        return self._parser_datetime()

    def _parser_extend_info(self):
        """parser timezone, shift"""
        index = self.query.rfind(' ')
        if index == -1:
            query = ''
            info = self.query
        else:
            query = self.query[:index]
            info = self.query[index + 1:].strip(' ')

        # time zone
        if info.upper() == 'UTC' or info == '+00' or info == '-00':
            self.query = query
            self.zone = 'UTC'
            self.wf.logger.debug('found zone info:'.format(self.zone))
            return True

        r = re.match(RE_TIMEZONE, info)
        if r:
            self.query = query
            self.zone = info
            self.wf.logger.debug('found zone info:'.format(self.zone))
            return True

        # time shift TODO

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
            self.wf.logger.debug(
                'parser datetime error,query string:{}'.format(self.query)
            )

        if self.query == 'now' or self.query == '':
            self.now = True
            self.time = arrow.now()
            return True

        return False

    def get_feedback(self):
        if self.time is None:
            return DEFAULT_FEEDBACK

        if self.now:
            desc_now = 'Now, '
        else:
            desc_now = ''

        f = list()
        for icon, force_utc, fmt, desc_format in FORMAT_LIST:

            if force_utc:
                self.time = self.time.to('UTC')
                desc_zone = 'UTC, '
            elif self.zone and not force_utc:
                self.time = self.time.to(self.zone)
                desc_zone = '{}, '.format(self.zone)
            else:
                self.time = self.time.to('local')
                desc_zone = 'Local, '

            value = self.time.format(fmt)
            subtitle = '{}{}{}'.format(
                desc_now, desc_zone, desc_format
            )
            f.append({
                'title': value,
                'subtitle': subtitle,
                'valid': True,
                'arg': value,
                'icon': icon,
            })

        return f


def do_convert(wf):
    time = Time(wf)
    time.do_parser()

    return time.get_feedback()
