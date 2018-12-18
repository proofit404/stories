from ._compat import Enum, EnumMeta
from ._repr import failures_representation
from .exceptions import FailureProtocolError


def make_protocol(failures):
    if type(failures) not in {type(None), list, tuple, set, frozenset, EnumMeta}:
        message = wrong_type_template.format(failures=failures)
        raise FailureProtocolError(message)
    if isinstance(failures, EnumMeta):
        protocol_class = EnumProtocol
    elif failures is not None:
        protocol_class = CollectionProtocol
    else:
        protocol_class = NullProtocol
    return protocol_class(failures)


class Protocol(object):
    def __init__(self, failures):
        self.failures = failures
        self.available = failures_representation(failures)

    def check_return_statement(self, obj, method, reason):
        if not reason:
            message = null_reason_template.format(
                available=self.available,
                cls=obj.__class__.__name__,
                method=method.__name__,
            )
            raise FailureProtocolError(message)
        if not self.check_reason(reason):
            message = wrong_reason_template.format(
                reason=reason,
                available=self.available,
                cls=obj.__class__.__name__,
                method=method.__name__,
            )
            raise FailureProtocolError(message)

    def check_reason(self, reason):

        raise NotImplementedError

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

    def cast_reason(self, reason):

        raise NotImplementedError

    def combine(
        self, other, cls_name, method_name, other_cls, other_method, other_available
    ):

        raise NotImplementedError

    def compare(self, a, b):

        raise NotImplementedError


class NullProtocol(Protocol):
    def check_return_statement(self, obj, method, reason):
        if reason:
            message = null_protocol_template.format(
                reason=reason, cls=obj.__class__.__name__, method=method.__name__
            )
            raise FailureProtocolError(message)

    def summarize(self, cls_name, method_name, reason):
        message = null_summary_template.format(cls=cls_name, method=method_name)
        raise FailureProtocolError(message)

    def cast_reason(self, reason):
        return None

    def combine(
        self, other, cls_name, method_name, other_cls, other_method, other_available
    ):
        if other.failures is None:
            return self
        else:
            return other.combine(
                self, other_cls, other_method, cls_name, method_name, self.available
            )


class CollectionProtocol(Protocol):
    def check_reason(self, reason):
        return reason in self.failures

    def cast_reason(self, reason):
        return reason

    def combine(
        self, other, cls_name, method_name, other_cls, other_method, other_available
    ):
        if other.failures is None:
            return self
        elif isinstance(other.failures, EnumMeta):
            message = type_error_template.format(
                cls=cls_name,
                method=method_name,
                available=self.available,
                other_cls=other_cls,
                other_method=other_method,
                other_available=other_available,
            )
            raise FailureProtocolError(message)
        else:
            return CollectionProtocol(
                self.failures
                + [
                    failure
                    for failure in other.failures
                    if failure not in self.failures
                ]
            )

    def compare(self, a, b):

        return a == b


class EnumProtocol(Protocol):
    def __init__(self, failures):
        self.failures = failures
        self.available = ", ".join(map(repr, failures.__members__.values()))

    def check_reason(self, reason):
        return isinstance(reason, Enum) and reason.name in self.failures.__members__

    def cast_reason(self, reason):
        return self.failures.__members__[reason.name]

    def combine(
        self, other, cls_name, method_name, other_cls, other_method, other_available
    ):
        if other.failures is None:
            return self
        elif isinstance(other.failures, (list, tuple, set, frozenset)):
            message = type_error_template.format(
                cls=cls_name,
                method=method_name,
                available=self.available,
                other_cls=other_cls,
                other_method=other_method,
                other_available=other_available,
            )
            raise FailureProtocolError(message)
        else:
            return EnumProtocol(
                Enum(
                    self.failures.__name__,
                    ",".join(
                        list(self.failures.__members__.keys())
                        + [
                            failure
                            for failure in other.failures.__members__.keys()
                            if failure not in self.failures.__members__.keys()
                        ]
                    ),
                )
            )

    def compare(self, a, b):

        return a.name == b.name


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
