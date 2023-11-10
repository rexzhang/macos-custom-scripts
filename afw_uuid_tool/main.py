import uuid

from afw_runtime import AFWFuncAbc, AFWResponse


class AFWFunc(AFWFuncAbc):
    _u: uuid.UUID
    _message_error: str

    @staticmethod
    def _make_data_from_uuid(u: uuid.UUID) -> list[AFWResponse]:
        return (
            (u.hex, "32-character lowercase hexadecimal string."),
            (str(u), "32-character lowercase hexadecimal string with dash."),
            # (str(u).upper(), ""),
            (str(u.int), "The UUID as a 128-bit integer."),
            (str(u.urn), "The UUID as a URN as specified in RFC 4122."),
            (
                f"Version {u.version}",
                "The UUID version number (1 through 5, specified is RFC_4122).",
            ),
        )

    @property
    def _data_defaulte(self) -> list:
        u = uuid.uuid4()
        return self._make_data_from_uuid(u)

    @property
    def _data_tips(self) -> list:
        return list()

    @property
    def _data_success(self) -> list:
        return self._make_data_from_uuid(self._u)

    @property
    def _data_error(self) -> list:
        return [
            (self._message_error, ""),
            # ("Please enter a UUID like string", ""),
            # ("Examples: 1111", ""),
        ]

    def _process(self) -> list[AFWResponse]:
        try:
            if len(self.args) == 0:
                raise ValueError(" Missing argument 'QUERY'")

            self._u = uuid.UUID(self.args[0])
            return True

        except ValueError as e:
            self._message_error = str(e)
            return False


def main(args: list[str], logger) -> list[AFWResponse]:
    return AFWFunc(args, logger)()
