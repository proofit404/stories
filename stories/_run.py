from ._summary import FailureSummary, SuccessSummary
from .exceptions import FailureError


class Call(object):
    def got_failure(self, ctx, method_name, reason):
        raise FailureError(reason)

    def got_result(self, value):
        return value

    def finished(self):
        pass


class Run(object):
    def got_failure(self, ctx, method_name, reason):
        return FailureSummary(ctx, method_name, reason)

    def got_result(self, value):
        return SuccessSummary(value)

    def finished(self):
        return SuccessSummary(None)
