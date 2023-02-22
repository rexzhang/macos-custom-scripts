import uuid

from afw_runtime import *

DEFAULT_RESPONSE = [
    AFWResponse(title="Please enter a UUID like string", arg="", icon=ICON_HELP),
    AFWResponse(title="Examples: 1111", arg="", icon=ICON_HELP),
]


def main(args: list[str], logger) -> list[AFWResponse]:
    logger.debug("test..")
    query = args[0]
    logger.debug(query)

    response = list()
    try:
        u = uuid.UUID(query)
    except ValueError as e:
        u = None
        v = str(uuid.uuid4()).upper()
        response += [
            AFWResponse(title=v, arg=v),
            AFWResponse(title=str(e), arg="", icon=ICON_ERROR),
        ]
        response += DEFAULT_RESPONSE

    if u is None:
        return response

    return [AFWResponse(title=str(u), arg=str(u), icon=ICON_NOTE, valid=True)]