# -*- coding: utf-8 -*-
from _stories.exceptions import make_failure_error
from _stories.summary import make_failure_summary
from _stories.summary import make_success_summary


class Call(object):
    def got_failure(self, ctx, method_name, reason):
        raise make_failure_error(reason)

    def got_result(self, value):
        return value

    def finished(self):
        pass


class Run(object):
    def __init__(self, protocol):
        self.protocol = protocol

    def got_failure(self, ctx, method_name, reason):
        return make_failure_summary(self.protocol, ctx, method_name, reason)

    def got_result(self, value):
        return make_success_summary(self.protocol, value)

    def finished(self):
        return make_success_summary(self.protocol, None)
