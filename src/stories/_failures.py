from typing import Callable, NoReturn, Optional, Sequence, Type, Union

from ._compat import Enum, EnumMeta
from ._types import ExecProtocol, FailureProtocol, FailureVariant, Methods, RunProtocol
from .exceptions import FailureProtocolError


# Data type.


def check_data_type(failures):
    # type: (FailureProtocol) -> None
    if failures is None:
        return
    if isinstance(failures, EnumMeta):
        return
    if isinstance(failures, (list, tuple, set, frozenset)) and all(
        isinstance(failure, str) for failure in failures
    ):
        return
    message = wrong_type_template.format(failures=failures)
    raise FailureProtocolError(message)


def failures_representation(failures):
    # type: (FailureProtocol) -> str
    if isinstance(failures, EnumMeta):
        return ", ".join(map(repr, failures.__members__.values()))
    elif isinstance(failures, (list, tuple, set, frozenset)):
        return ", ".join(map(repr, failures))
    elif failures is None:
        return "None"
    else:
        raise RuntimeError  # pragma: no cover


def collection_contains(reason, failures):
    # type: (str, Sequence[str]) -> bool
    return reason in failures


def collection_compare(a, b):
    # type: (str, str) -> bool
    return a == b


def enumeration_contains(reason, failures):
    # type: (Enum, Type[Enum]) -> bool
    return isinstance(reason, Enum) and reason.name in failures.__members__


def enumeration_compare(a, b):
    # type: (Enum, Enum) -> bool
    return a.name == b.name


ContainsFunc = Union[
    Callable[[str, Sequence[str]], bool], Callable[[Enum, Type[Enum]], bool]
]
CompareFunc = Union[Callable[[str, str], bool], Callable[[Enum, Enum], bool]]


# Execute.


def make_exec_protocol(failures):
    # type: (FailureProtocol) -> ExecProtocol
    if isinstance(failures, EnumMeta):
        return NotNullExecProtocol(failures, enumeration_contains)
    elif isinstance(failures, (list, tuple, set, frozenset)):
        return NotNullExecProtocol(failures, collection_contains)
    elif failures is None:
        return NullExecProtocol()
    else:
        raise RuntimeError  # pragma: no cover


class NullExecProtocol(object):
    def check_return_statement(self, method, reason):
        # type: (Callable, Optional[FailureVariant]) -> None
        if reason:
            message = null_protocol_template.format(
                reason=reason,
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
            )
            raise FailureProtocolError(message)


class DisabledNullExecProtocol(NullExecProtocol):
    def check_return_statement(self, method, reason):
        # type: (Callable, Optional[FailureVariant]) -> None
        if not reason:
            message = disabled_null_template.format(
                cls=method.__self__.__class__.__name__, method=method.__name__
            )
            raise FailureProtocolError(message)
        super(DisabledNullExecProtocol, self).check_return_statement(method, reason)


class NotNullExecProtocol(object):
    def __init__(self, failures, contains_func):
        # type: (FailureProtocol, ContainsFunc) -> None
        self.failures = failures
        self.contains_func = contains_func

    def check_return_statement(self, method, reason):
        # type: (Callable, Optional[FailureVariant]) -> None
        if not reason:
            message = null_reason_template.format(
                available=failures_representation(self.failures),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
            )
            raise FailureProtocolError(message)
        if not self.contains_func(reason, self.failures):
            message = wrong_reason_template.format(
                reason=reason,
                available=failures_representation(self.failures),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
            )
            raise FailureProtocolError(message)


# Run.


def make_run_protocol(failures, cls_name, method_name):
    # type: (FailureProtocol, str, str) -> RunProtocol
    if isinstance(failures, EnumMeta):
        return NotNullRunProtocol(
            cls_name, method_name, failures, enumeration_contains, enumeration_compare
        )
    elif isinstance(failures, (list, tuple, set, frozenset)):
        return NotNullRunProtocol(
            cls_name, method_name, failures, collection_contains, collection_compare
        )
    elif failures is None:
        return NullRunProtocol(cls_name, method_name)
    else:
        raise RuntimeError  # pragma: no cover


class NullRunProtocol(object):
    def __init__(self, cls_name, method_name):
        # type: (str, str) -> None
        self.cls_name = cls_name
        self.method_name = method_name

    def check_failed_because_argument(self, reason):
        # type: (FailureVariant) -> NoReturn
        message = null_summary_template.format(
            cls=self.cls_name, method=self.method_name
        )
        raise FailureProtocolError(message)


class NotNullRunProtocol(object):
    def __init__(
        self,
        cls_name,  # type: str
        method_name,  # type: str
        failures,  # type: FailureProtocol
        contains_func,  # type: ContainsFunc
        compare_func,  # type: CompareFunc
    ):
        # type: (...) -> None
        self.cls_name = cls_name
        self.method_name = method_name
        self.failures = failures
        self.contains_func = contains_func
        self.compare_func = compare_func

    def check_failed_because_argument(self, reason):
        # type: (FailureVariant) -> None
        if not self.contains_func(reason, self.failures):
            message = wrong_summary_template.format(
                reason=reason,
                available=failures_representation(self.failures),
                cls=self.cls_name,
                method=self.method_name,
            )
            raise FailureProtocolError(message)

    def compare_failed_because_argument(self, argument, failure_reason):
        # type: (FailureVariant, FailureVariant) -> bool
        return self.compare_func(argument, failure_reason)


# Wrap.


def combine_failures(
    first_failures,  # type: FailureProtocol
    first_cls_name,  # type: str
    first_method_name,  # type: str
    second_failures,  # type: FailureProtocol
    second_cls_name,  # type: str
    second_method_name,  # type: str
):
    # type: (...) -> FailureProtocol
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


def maybe_disable_null_protocol(methods, reasons):
    # type: (Methods, FailureProtocol) -> Methods
    if reasons is None:
        return methods
    disabled = DisabledNullExecProtocol()
    return [
        (method, contract, disabled if type(protocol) is NullExecProtocol else protocol)
        for method, contract, protocol in methods
    ]


# Messages.


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
