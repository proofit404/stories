from typing import NoReturn

from ._summary import FailureSummary, SuccessSummary
from ._types import (
    AbstractContext,
    AbstractRunner,
    AbstractSummary,
    FailureVariant,
    ValueVariant,
)
from .exceptions import FailureError


class Call(AbstractRunner):
    def got_failure(self, ctx, method_name, reason):
        # type: (AbstractContext, str, FailureVariant) -> NoReturn
        raise FailureError(reason)

    def got_result(self, value):
        # type: (ValueVariant) -> ValueVariant
        return value

    def finished(self):
        # type: () -> None
        pass


class Run(AbstractRunner):
    def __init__(self, protocol):
        self.protocol = protocol

    def got_failure(self, ctx, method_name, reason):
        # type: (AbstractContext, str, FailureVariant) -> AbstractSummary
        return FailureSummary(self.protocol, ctx, method_name, reason)

    def got_result(self, value):
        # type: (ValueVariant) -> AbstractSummary
        return SuccessSummary(self.protocol, value)

    def finished(self):
        # type: () -> AbstractSummary
        return SuccessSummary(self.protocol, None)
