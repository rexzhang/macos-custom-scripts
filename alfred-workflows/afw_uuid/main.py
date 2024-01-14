import uuid
from logging import Logger

from afw_runtime import AFWFuncAbc, AFWResponse


class AFWFunc(AFWFuncAbc):
    _uuid: uuid.UUID | None = None
    _tips = False

    def make_responses_from_uuid(self) -> list[AFWResponse]:
        return [
            AFWResponse(
                title=str(self._uuid),
                subtitle="The UUID as a 32-character lowercase hexadecimal string with dash.",
                icon=self.icon_info,
            ),
            AFWResponse(
                title=self._uuid.hex,
                subtitle="The UUID as a 32-character lowercase hexadecimal string.",
                icon=self.icon_info,
            ),
            AFWResponse(
                title=str(self._uuid.int),
                subtitle="The UUID as a 128-bit integer.",
                icon=self.icon_info,
            ),
            AFWResponse(
                title=str(self._uuid.urn),
                subtitle="The UUID as a URN as specified in RFC 4122.",
                icon=self.icon_info,
            ),
            AFWResponse(
                title=f"{self._uuid.version}",
                subtitle="The UUID version number (1 through 5, specified is RFC_4122).",
                icon=self.icon_info,
                arg=4,
            ),
        ]

    def append_tips(self):
        example1 = "uuid 4"
        example2 = "uuid 8d402c08-8155-11ee-9f73-a45e60bae6e9"
        self.responses += [
            AFWResponse(
                title="Example", subtitle=example1, icon=self.icon_note, arg=example1
            ),
            AFWResponse(
                title="Example", subtitle=example2, icon=self.icon_note, arg=example2
            ),
        ]

    def _guess_input(self) -> uuid.UUID | None:
        if len(self.args) == 0:
            self._tips = True
            query = "4"

        else:
            query = self.args[0]

        try:
            v = int(query)
            match v:
                case 1:
                    u = uuid.uuid1()
                case 4:
                    u = uuid.uuid4()
                case _:
                    raise ValueError

            return u

        except ValueError:
            pass

        try:
            u = uuid.UUID(query)
        except ValueError:
            return None

        return u

    def _createa_responses(self):
        if self._uuid:
            self.append_responses(self.make_responses_from_uuid())

        if self._tips:
            self.append_tips()

    def _process(self) -> None:
        self._uuid = self._guess_input()
        if self._uuid is None:
            self._tips = True

        self._createa_responses()
        return


def main(args: list[str], logger: Logger) -> list[dict]:
    return AFWFunc(args, logger)()
