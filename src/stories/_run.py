from ._summary import FailureSummary, SuccessSummary
from .exceptions import FailureError


class Call(object):
    def __init__(self, protocol):
        self.protocol = protocol

    def got_failure(self, ctx, method_name, reason):
        raise FailureError(self.protocol.cast_reason(reason))

    def got_result(self, value):
        return value

    def finished(self):
        pass


class Run(object):
    def __init__(self, protocol, story_cls_name, story_method_name):
        self.protocol = protocol
        self.story_cls_name = story_cls_name
        self.story_method_name = story_method_name

    def got_failure(self, ctx, method_name, reason):
        return FailureSummary(
            self.protocol,
            self.story_cls_name,
            self.story_method_name,
            ctx,
            method_name,
            self.protocol.cast_reason(reason),
        )

    def got_result(self, value):
        return SuccessSummary(value)

    def finished(self):
        return SuccessSummary(None)
