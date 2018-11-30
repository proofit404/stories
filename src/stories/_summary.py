class FailureSummary(object):
    def __init__(self, ctx, failed_method, reason):
        self.is_success = False
        self.is_failure = True
        self.ctx = ctx
        self.failed_method = failed_method
        self.failure_reason = reason

    def failed_on(self, method_name):
        return method_name == self.failed_method

    def failed_because(self, reason):
        return reason == self.failure_reason

    @property
    def value(self):
        raise AssertionError

    def __repr__(self):
        return "Failure()"


class SuccessSummary(object):
    def __init__(self, value):
        self.is_success = True
        self.is_failure = False
        self.value = value

    def failed_on(self, method_name):
        return False

    def failed_because(self, reason):
        return False

    def __repr__(self):
        return "Success()"
