from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from stories._contract import NullContract, SpecContract
from stories._failures import NotNullExecProtocol, NullExecProtocol
from stories._marker import BeginningOfStory, EndOfStory
from stories._summary import FailureSummary, SuccessSummary


class ClassMountedStory:
    def __init__(
        self,
        cls: Any,
        name: str,
        collected: List[str],
        contract: Callable[[Any], Any],
        failures: Callable[[Any], Optional[Union[List[str], Type[Enum]]]],
    ) -> None: ...

    def __repr__(self) -> str: ...


class MountedStory:
    def __init__(
        self,
        obj: Any,
        cls_name: str,
        name: str,
        arguments: List[str],
        methods: List[
            Tuple[
                Union[BeginningOfStory, Callable, EndOfStory],
                Union[NullContract, SpecContract],
                Union[NullExecProtocol, NotNullExecProtocol],
            ],
        ],
        contract: NullContract,
        failures: Optional[Union[List[str], Type[Enum]]],
    ) -> None: ...

    def __call__(self, **kwargs: Dict[str, Any]) -> Optional[Union[List[str], int]]: ...

    def run(
        self, **kwargs: Dict[str, Any]
    ) -> Union[SuccessSummary, FailureSummary]: ...

    def __repr__(self) -> str: ...
