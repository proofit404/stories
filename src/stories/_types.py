from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Tuple, Type, Union

from ._compat import CerberusSpec, Enum, MarshmallowSpec, PydanticSpec


ClassWithSpec = Any

Spec = Callable

Arguments = List[str]

Collected = List[str]

Namespace = Dict[str, Any]


class AbstractContext(ABC):
    _Context__ns = None  # type: Namespace


ContextContract = Union[
    PydanticSpec, MarshmallowSpec, CerberusSpec, Dict[str, Callable], None
]

FailureProtocol = Union[List[str], Type[Enum], None]

ValueVariant = Any

FailureVariant = Union[str, Enum]


class ExecContract(ABC):
    @abstractmethod
    def check_story_call(self, kwargs):
        # type: (Namespace) -> Namespace
        pass

    @abstractmethod
    def check_substory_call(self, ctx):
        # type: (AbstractContext) -> None
        pass

    @abstractmethod
    def check_success_statement(self, method, ctx, ns):
        # type: (Callable, AbstractContext, Namespace) -> Namespace
        pass


class ExecProtocol(ABC):
    @abstractmethod
    def check_return_statement(self, method, reason):
        # type: (Callable, FailureVariant) -> None
        pass


Method = Callable

Methods = List[Tuple[Method, ExecContract, ExecProtocol]]

Wrapped = Tuple[Methods, ExecContract, FailureProtocol]


class AbstractRunner(ABC):
    @abstractmethod
    def got_failure(self, ctx, method_name, reason):
        # type: (AbstractContext, str, FailureVariant) -> Any
        pass

    @abstractmethod
    def got_result(self, value):
        # type: (ValueVariant) -> Any
        pass

    @abstractmethod
    def finished(self):
        # type: () -> Any
        pass


class AbstractSummary(ABC):
    @abstractmethod
    def failed_on(self, method_name):
        # type: (str) -> bool
        pass

    @abstractmethod
    def failed_because(self, reason):
        # type: (FailureVariant) -> bool
        pass


class AbstractHistory(ABC):
    @abstractmethod
    def before_call(self, method_name):
        # type: (str) -> None
        pass

    @abstractmethod
    def on_result(self, value):
        # type: (ValueVariant) -> None
        pass

    @abstractmethod
    def on_failure(self, reason):
        # type: (FailureVariant) -> None
        pass

    @abstractmethod
    def on_skip(self):
        # type: () -> None
        pass

    @abstractmethod
    def on_error(self, error_name):
        # type: (str) -> None
        pass

    @abstractmethod
    def on_substory_start(self):
        # type: () -> None
        pass

    @abstractmethod
    def on_substory_end(self):
        # type: () -> None
        pass
