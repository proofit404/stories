from enum import Enum
from typing import Any, Callable, List, Optional, Tuple, Type, Union

from stories._contract import NullContract, SpecContract
from stories._marker import BeginningOfStory, EndOfStory

def check_data_type(failures: Any) -> None: ...
def collection_compare(a: str, b: str) -> bool: ...
def collection_contains(reason: str, failures: List[str]) -> bool: ...
def combine_failures(
    first_failures: Optional[Union[List[str], Type[Enum]]],
    first_cls_name: str,
    first_method_name: str,
    second_failures: Optional[Union[List[str], Type[Enum]]],
    second_cls_name: str,
    second_method_name: str,
) -> Optional[Union[List[str], Type[Enum]]]: ...
def enumeration_compare(a: Enum, b: Enum) -> bool: ...
def enumeration_contains(reason: Union[str, Enum], failures: Type[Enum]) -> bool: ...
def failures_representation(failures: Union[List[str], Type[Enum]]) -> str: ...
def make_exec_protocol(
    failures: Optional[Union[Type[Enum], List[str], Type[Enum]]]
) -> Union[NotNullExecProtocol, NullExecProtocol]: ...
def make_run_protocol(
    failures: Optional[Union[List[str], Type[Enum]]], cls_name: str, method_name: str
) -> Union[NotNullRunProtocol, NullRunProtocol]: ...
def maybe_disable_null_protocol(
    methods: Union[
        List[
            Union[
                Tuple[BeginningOfStory, NullContract, NullExecProtocol],
                Tuple[Callable, NullContract, NullExecProtocol],
                Tuple[EndOfStory, NullContract, NullExecProtocol],
            ]
        ],
        List[
            Union[
                Tuple[BeginningOfStory, NullContract, NotNullExecProtocol],
                Tuple[Callable, NullContract, NotNullExecProtocol],
                Tuple[BeginningOfStory, NullContract, NullExecProtocol],
                Tuple[Callable, NullContract, NullExecProtocol],
                Tuple[EndOfStory, NullContract, NullExecProtocol],
                Tuple[EndOfStory, NullContract, NotNullExecProtocol],
            ]
        ],
        List[
            Union[
                Tuple[BeginningOfStory, NullContract, NullExecProtocol],
                Tuple[EndOfStory, NullContract, NullExecProtocol],
            ]
        ],
        List[
            Union[
                Tuple[BeginningOfStory, SpecContract, NullExecProtocol],
                Tuple[Callable, SpecContract, NullExecProtocol],
                Tuple[EndOfStory, SpecContract, NullExecProtocol],
            ]
        ],
        List[
            Union[
                Tuple[BeginningOfStory, NullContract, NotNullExecProtocol],
                Tuple[Callable, NullContract, NotNullExecProtocol],
                Tuple[EndOfStory, NullContract, NotNullExecProtocol],
            ]
        ],
    ],
    reasons: Optional[Union[Type[Enum], List[str], Type[Enum]]],
) -> Union[
    List[
        Union[
            Tuple[BeginningOfStory, NullContract, NotNullExecProtocol],
            Tuple[Callable, NullContract, NotNullExecProtocol],
            Tuple[BeginningOfStory, NullContract, DisabledNullExecProtocol],
            Tuple[Callable, NullContract, DisabledNullExecProtocol],
            Tuple[EndOfStory, NullContract, DisabledNullExecProtocol],
            Tuple[EndOfStory, NullContract, NotNullExecProtocol],
        ]
    ],
    List[
        Union[
            Tuple[BeginningOfStory, NullContract, NullExecProtocol],
            Tuple[Callable, NullContract, NullExecProtocol],
            Tuple[EndOfStory, NullContract, NullExecProtocol],
        ]
    ],
    List[
        Union[
            Tuple[BeginningOfStory, NullContract, NullExecProtocol],
            Tuple[EndOfStory, NullContract, NullExecProtocol],
        ]
    ],
    List[
        Union[
            Tuple[BeginningOfStory, SpecContract, NullExecProtocol],
            Tuple[Callable, SpecContract, NullExecProtocol],
            Tuple[EndOfStory, SpecContract, NullExecProtocol],
        ]
    ],
    List[
        Union[
            Tuple[BeginningOfStory, NullContract, NotNullExecProtocol],
            Tuple[Callable, NullContract, NotNullExecProtocol],
            Tuple[EndOfStory, NullContract, NotNullExecProtocol],
        ]
    ],
]: ...

class DisabledNullExecProtocol:
    def check_return_statement(
        self, method: Callable, reason: Optional[Union[str, Enum]]
    ): ...

class NotNullExecProtocol:
    def __init__(
        self,
        failures: Union[List[str], Type[Enum], Type[Enum]],
        contains_func: Callable,
    ) -> None: ...
    def check_return_statement(
        self, method: Callable, reason: Optional[Union[str, Enum]]
    ) -> None: ...

class NotNullRunProtocol:
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

class NullExecProtocol:
    def check_return_statement(
        self, method: Callable, reason: Optional[Union[str, Enum]]
    ) -> None: ...

class NullRunProtocol:
    def __init__(self, cls_name: str, method_name: str) -> None: ...
    def check_failed_because_argument(self, reason: str): ...
