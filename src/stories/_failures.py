from ._compat import Enum, EnumMeta
from ._repr import failures_representation
from .exceptions import FailureProtocolError


def make_protocol(failures):

    if isinstance(failures, EnumMeta):
        return EnumProtocol(failures)
    elif isinstance(failures, (list, tuple, set, frozenset)):
        return CollectionProtocol(failures)
    elif failures is None:
        return NullProtocol(failures)
    else:
        message = wrong_type_template.format(failures=failures)
        raise FailureProtocolError(message)


class Protocol(object):
    def __init__(self, failures):
        self.failures = failures
        self.available = failures_representation(failures)

    def check_return_statement(self, method, reason):
        if not reason:
            message = null_reason_template.format(
                available=self.available,
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
            )
            raise FailureProtocolError(message)
        if not self.check_reason(reason):
            message = wrong_reason_template.format(
                reason=reason,
                available=self.available,
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
            )
            raise FailureProtocolError(message)

    def summarize(self, cls_name, method_name, reason):
        # TODO: Deny to use `failed_because(None)`.
        if not self.check_reason(reason):
            message = wrong_summary_template.format(
                reason=reason,
                available=self.available,
                cls=cls_name,
                method=method_name,
            )
            raise FailureProtocolError(message)

    def check_reason(self, reason):

        raise NotImplementedError

    def cast_reason(self, reason):

        raise NotImplementedError

    def compare(self, a, b):

        raise NotImplementedError


class NullProtocol(Protocol):
    def check_return_statement(self, method, reason):
        if reason:
            message = null_protocol_template.format(
                reason=reason,
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
            )
            raise FailureProtocolError(message)

    def summarize(self, cls_name, method_name, reason):
        message = null_summary_template.format(cls=cls_name, method=method_name)
        raise FailureProtocolError(message)

    def cast_reason(self, reason):
        return None


class CollectionProtocol(Protocol):
    def check_reason(self, reason):
        return reason in self.failures

    def cast_reason(self, reason):
        return reason

    def compare(self, a, b):

        return a == b


class EnumProtocol(Protocol):
    def check_reason(self, reason):
        return isinstance(reason, Enum) and reason.name in self.failures.__members__

    def cast_reason(self, reason):
        return self.failures.__members__[reason.name]

    def compare(self, a, b):

        return a.name == b.name


def combine_failures(
    first_failures,
    first_cls_name,
    first_method_name,
    second_failures,
    second_cls_name,
    second_method_name,
):
    if first_failures is None:
        return second_failures
    elif second_failures is None:
        return first_failures
    elif isinstance(first_failures, EnumMeta) and isinstance(second_failures, EnumMeta):
        return Enum(
            first_failures.__name__,
            ",".join(
                list(first_failures.__members__.keys())
                + [
                    failure
                    for failure in second_failures.__members__.keys()
                    if failure not in first_failures.__members__.keys()
                ]
            ),
        )
    elif isinstance(first_failures, (list, tuple, set, frozenset)) and isinstance(
        second_failures, (list, tuple, set, frozenset)
    ):
        return first_failures + [
            failure for failure in second_failures if failure not in first_failures
        ]
    else:
        message = type_error_template.format(
            cls=first_cls_name,
            method=first_method_name,
            available=failures_representation(first_failures),
            other_cls=second_cls_name,
            other_method=second_method_name,
            other_available=failures_representation(second_failures),
        )
        raise FailureProtocolError(message)


class DisabledNullProtocol(NullProtocol):
    def check_return_statement(self, method, reason):
        if not reason:
            message = disabled_null_template.format(
                cls=method.__self__.__class__.__name__, method=method.__name__
            )
            raise FailureProtocolError(message)
        super(DisabledNullProtocol, self).check_return_statement(method, reason)


def maybe_disable_null_protocol(methods, reasons):

    if reasons is None:
        return methods
    disabled = DisabledNullProtocol(None)
    return [
        (f, disabled if type(protocol) is NullProtocol else protocol)
        for f, protocol in methods
    ]


wrong_type_template = """
Unexpected type for story failure protocol: {failures!r}
""".strip()


wrong_reason_template = """
Failure({reason!r}) failure reason is not allowed by current protocol.

Available failures are: {available}

Function returned value: {cls}.{method}
""".strip()


null_reason_template = """
Failure() can not be used in a story with failure protocol.

Available failures are: {available}

Function returned value: {cls}.{method}

Use one of them as Failure() argument.
""".strip()


null_protocol_template = """
Failure({reason!r}) can not be used in a story without failure protocol.

Function returned value: {cls}.{method}

Use 'failures' story method to define failure protocol.
""".strip()


wrong_summary_template = """
'failed_because' method got argument mismatching failure protocol: {reason!r}

Available failures are: {available}

Story returned result: {cls}.{method}
""".strip()


null_summary_template = """
'failed_because' method can not be used with story defined without failure protocol.

Story returned result: {cls}.{method}

Use 'failures' story method to define failure protocol.
""".strip()


type_error_template = """
Story and substory failure protocols has incompatible types:

Story method: {cls}.{method}

Story failure protocol: {available}

Substory method: {other_cls}.{other_method}

Substory failure protocol: {other_available}
""".strip()


disabled_null_template = """
Failure() can not be used in a story composition.

Different types of failure protocol were used in parent and substory definitions.

Function returned value: {cls}.{method}

Use 'failures' story method to define failure protocol.
""".strip()
