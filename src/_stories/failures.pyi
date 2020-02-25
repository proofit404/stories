from enum import Enum
from typing import Any
from typing import Callable
from typing import List
from typing import NoReturn
from typing import Optional
from typing import overload
from typing import Tuple
from typing import Type
from typing import Union

from _stories.contract import NullContract
from _stories.contract import SpecContract
from _stories.marker import BeginningOfStory
from _stories.marker import EndOfStory

def check_data_type(failures: Any) -> None: ...
def failures_representation(failures: Union[List[str], Type[Enum]]) -> str: ...
def collection_contains(reason: str, failures: List[str]) -> bool: ...
def collection_compare(a: str, b: str) -> bool: ...
def enumeration_contains(reason: Enum, failures: Type[Enum]) -> bool: ...
def enumeration_compare(a: Enum, b: Enum) -> bool: ...
@overload
def make_exec_protocol(failures: None) -> NullExecProtocol: ...
@overload
def make_exec_protocol(failures: List[str]) -> NotNullExecProtocol: ...
@overload
def make_exec_protocol(failures: Type[Enum]) -> NotNullExecProtocol: ...

class NullExecProtocol:
    def check_return_statement(
        self, method: Callable, reason: Optional[Union[str, Enum]]
    ) -> None: ...

class DisabledNullExecProtocol:
    def check_return_statement(
        self, method: Callable, reason: Optional[Union[str, Enum]]
    ) -> None: ...

class NotNullExecProtocol:  # FIXME: Generic.
    def __init__(
        self,
        failures: Union[List[str], Type[Enum], Type[Enum]],
        contains_func: Callable,
    ) -> None: ...
    def check_return_statement(
        self, method: Callable, reason: Optional[Union[str, Enum]]
    ) -> None: ...

@overload
def make_run_protocol(
    failures: None, cls_name: str, method_name: str
) -> NullRunProtocol: ...
@overload
def make_run_protocol(
    failures: List[str], cls_name: str, method_name: str
) -> NotNullRunProtocol: ...
@overload
def make_run_protocol(
    failures: Type[Enum], cls_name: str, method_name: str
) -> NotNullRunProtocol: ...

class NullRunProtocol:
    def __init__(self, cls_name: str, method_name: str) -> None: ...
    def check_failed_because_argument(self, reason: str) -> NoReturn: ...

class NotNullRunProtocol:  # FIXME: Generic.
    def __init__(
        self,
        cls_name: str,
        method_name: str,
        failures: Union[List[str], Type[Enum]],
        contains_func: Callable,
        compare_func: Callable,
    ) -> None: ...
    def check_failed_because_argument(self, reason: Union[str, Enum]) -> None: ...
    def compare_failed_because_argument(
        self, argument: Union[str, Enum], failure_reason: Union[str, Enum]
    ) -> bool: ...

def combine_failures(
    first_failures: Optional[Union[List[str], Type[Enum]]],
    first_cls_name: str,
    first_method_name: str,
    second_failures: Optional[Union[List[str], Type[Enum]]],
    second_cls_name: str,
    second_method_name: str,
) -> Optional[Union[List[str], Type[Enum]]]: ...
def maybe_disable_null_protocol(
    methods: List[
        Tuple[
            Union[BeginningOfStory, Callable, EndOfStory],
            Union[NullContract, SpecContract],
            Union[NullExecProtocol, NotNullExecProtocol],
        ],
    ],
    reasons: Optional[Union[List[str], Type[Enum]]],
) -> List[
    Tuple[
        Union[BeginningOfStory, Callable, EndOfStory],
        Union[NullContract, SpecContract],
        Union[NullExecProtocol, DisabledNullExecProtocol, NotNullExecProtocol],
    ],
]: ...
