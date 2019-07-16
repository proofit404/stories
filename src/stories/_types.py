from typing import Any, Callable, Dict, List, Tuple, Type, Union

from typing_extensions import Protocol

from ._compat import CerberusSpec, Enum, MarshmallowSpec, PydanticSpec


ClassWithSpec = Type[object]

Spec = Callable[[object], None]

Arguments = List[str]

Collected = List[str]

Namespace = Dict[str, Any]


class AbstractContext(Protocol):
    _Context__ns = None  # type: Namespace
    _Context__history = None  # type: AbstractHistory
    _Context__lines = None  # type: List[str]


ContextContract = Union[
    PydanticSpec, MarshmallowSpec, CerberusSpec, Dict[str, Callable], None
]

FailureProtocol = Union[List[str], Type[Enum], None]

ValueVariant = Any

FailureVariant = Union[str, Enum]


class ExecContract(Protocol):
    cls_name = None  # type: str
    name = None  # type: str

    def check_story_call(self, kwargs):
        # type: (Namespace) -> Namespace
        pass

    def check_substory_call(self, ctx):
        # type: (AbstractContext) -> None
        pass

    def check_success_statement(self, method, ctx, ns):
        # type: (Method, AbstractContext, Namespace) -> Namespace
        pass


class ExecProtocol(Protocol):
    def check_return_statement(self, method, reason):
        # type: (Method, FailureVariant) -> None
        pass


class RunProtocol(Protocol):
    def check_failed_because_argument(self, reason):
        # type: (FailureVariant) -> None
        pass

    def compare_failed_because_argument(self, argument, failure_reason):
        # type: (FailureVariant, FailureVariant) -> bool
        pass


class MethodResult(Protocol):
    pass


class Method(Protocol):
    __self__ = None  # type: Type[object]
    __name__ = None  # type: str

    def __call__(self, ctx):
        # type: (AbstractContext) -> MethodResult
        pass


Methods = List[Tuple[Method, ExecContract, ExecProtocol]]

Wrapped = Tuple[Methods, ExecContract, FailureProtocol]


class AbstractRunner(Protocol):
    def got_failure(self, ctx, method_name, reason):
        # type: (AbstractContext, str, FailureVariant) -> Any
        pass

    def got_result(self, value):
        # type: (ValueVariant) -> Any
        pass

    def finished(self):
        # type: () -> Any
        pass


class AbstractSummary(Protocol):
    def failed_on(self, method_name):
        # type: (str) -> bool
        pass

    def failed_because(self, reason):
        # type: (FailureVariant) -> bool
        pass


class AbstractHistory(Protocol):
    lines = None  # type: List[str]

    def before_call(self, method_name):
        # type: (str) -> None
        pass

    def on_result(self, value):
        # type: (ValueVariant) -> None
        pass

    def on_failure(self, reason):
        # type: (FailureVariant) -> None
        pass

    def on_skip(self):
        # type: () -> None
        pass

    def on_error(self, error_name):
        # type: (str) -> None
        pass

    def on_substory_start(self):
        # type: () -> None
        pass

    def on_substory_end(self):
        # type: () -> None
        pass


ExecResult = Union[ValueVariant, AbstractSummary]
