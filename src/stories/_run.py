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
    def __init__(self, protocol):
        self.protocol = protocol

    def got_failure(self, ctx, method_name, reason):
        return FailureSummary(self.protocol, ctx, method_name, reason)

    def got_result(self, value):
        return SuccessSummary(self.protocol, value)

    def finished(self):
        return SuccessSummary(self.protocol, None)
