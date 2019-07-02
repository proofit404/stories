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
