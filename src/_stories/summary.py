# -*- coding: utf-8 -*-


def make_failure_summary(protocol, ctx, failed_method, failure_reason):
    def failed_on_method(self, method_name):
        return method_name == failed_method

    def failed_because_method(self, reason):
        protocol.check_failed_because_argument(reason)
        return protocol.compare_failed_because_argument(reason, failure_reason)

    return type(
        "FailureSummary",
        (object,),
        {
            "is_success": False,
            "is_failure": True,
            "ctx": ctx,
            "value": failure_value_method,
            "failed_on": failed_on_method,
            "failed_because": failed_because_method,
            "__repr__": failure_repr_method,
        },
    )()


@property
def failure_value_method(self):
    raise AssertionError


def failure_repr_method(self):
    return "Failure()"


def make_success_summary(protocol, value):
    def success_failed_because_method(self, reason):
        protocol.check_failed_because_argument(reason)
        return False

    return type(
        "SuccessSummary",
        (object,),
        {
            "is_success": True,
            "is_failure": False,
            "value": value,
            "failed_on": success_failed_on_method,
            "failed_because": success_failed_because_method,
            "__repr__": success_repr_method,
        },
    )()


def success_failed_on_method(self, method_name):
    return False


def success_repr_method(self):
    return "Success()"
