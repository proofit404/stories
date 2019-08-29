class FailureSummary(object):
    def __init__(self, protocol, ctx, failed_method, reason):
        self.__protocol = protocol
        self.is_success = False
        self.is_failure = True
        self.ctx = ctx
        self.__failed_method = failed_method
        self.__failure_reason = reason

    def failed_on(self, method_name):
        return method_name == self.__failed_method

    def failed_because(self, reason):
        self.__protocol.check_failed_because_argument(reason)
        return self.__protocol.compare_failed_because_argument(
            reason, self.__failure_reason
        )

    @property
    def value(self):
        raise AssertionError

    def __repr__(self):
        return "Failure()"


class SuccessSummary(object):
    def __init__(self, protocol, value):
        self.__protocol = protocol
        self.is_success = True
        self.is_failure = False
        self.value = value

    def failed_on(self, method_name):
        return False

    def failed_because(self, reason):
        self.__protocol.check_failed_because_argument(reason)
        return False

    def __repr__(self):
        return "Success()"
