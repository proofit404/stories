from typing import Optional

from ._types import FailureVariant, ValueVariant


class Result(object):
    def __init__(self, value=None):
        # type: (ValueVariant) -> None
        self.value = value

    def __repr__(self):
        # type: () -> str
        return "Result(" + repr(self.value) + ")"


class Success(object):
    def __init__(self, **kwargs):
        # type: (**ValueVariant) -> None
        self.kwargs = kwargs

    def __repr__(self):
        # type: () -> str
        return (
            "Success("
            + ", ".join([k + "=" + repr(v) for k, v in self.kwargs.items()])
            + ")"
        )


class Failure(object):
    def __init__(self, reason=None):
        # type: (Optional[FailureVariant]) -> None
        self.reason = reason

    def __repr__(self):
        # type: () -> str
        reason = repr(self.reason) if self.reason else ""
        return "Failure(" + reason + ")"


class Skip(object):
    def __repr__(self):
        # type: () -> str
        return "Skip()"
