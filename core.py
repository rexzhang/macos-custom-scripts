#!/usr/bin/python
# encoding: utf-8


import arrow
from dateutil import tz
from workflow import ICON_CLOCK, ICON_NOTE

FORMAT_LIST = (
    (ICON_NOTE, 'X', 'UTC Timestamp (s)'),
    (ICON_NOTE, 'x', 'UTC Timestamp (us)'),
    (
        ICON_CLOCK, 'YYYY-MM-DD HH:mm:ss', 'Date and Time'
    ),
    (
        ICON_CLOCK, 'W, DDDD[th day]',
        'ISO Week date and Day for year'
    ),
    (  # https://www.w3.org/TR/NOTE-datetime
        ICON_CLOCK, 'YYYY-MM-DDTHH:mm:ssZZ',
        'W3C Format'
    ),
    (ICON_CLOCK, arrow.FORMAT_RFC850, 'RFC850 Format'),
    # FORMAT_RFC3339
)


def parser_query(wf):
    """parser datetime, timezone, shift"""
    try:
        query = wf.args[0].encode('utf8').strip(' ').rstrip(' ')

        if query.isdigit():
            query = int(query)

        wf.logger.debug('query string:{} {}'.format(type(query), query))
        return arrow.get(query), False

    except (IndexError, arrow.ParserError):
        wf.logger.debug('args:{}'.format(wf.args))
        return arrow.get(), True


def create_feedback(time, is_now):
    f = list()
    for icon, fmt, desc in FORMAT_LIST:
        value = time.to(tz.tzlocal()).format(fmt)
        # value = t.format(fmt)

        f.append({
            'title': value,
            'subtitle': 'Current, {}'.format(desc) if is_now else desc,
            'valid': True,
            'arg': value,
            'icon': icon,
        })

    return f


def do_convert(wf):
    time, is_now = parser_query(wf)
    return create_feedback(time, is_now)
