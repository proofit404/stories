from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from stories._contract import NullContract
from stories._failures import NullExecProtocol
from stories._marker import BeginningOfStory, EndOfStory
from stories._summary import FailureSummary, SuccessSummary


class ClassMountedStory:
    def __init__(
        self,
        cls: Any,
        name: str,
        collected: List[str],
        contract: Callable,
        failures: Callable,
    ) -> None: ...
    def __repr__(self) -> str: ...


class MountedStory:
    def __call__(self, **kwargs: Dict[str, Any]) -> Optional[Union[List[str], int]]: ...
    def __init__(
        self,
        obj: Any,
        cls_name: str,
        name: str,
        arguments: List[str],
        methods: Union[
            List[
                Union[
                    Tuple[BeginningOfStory, NullContract, NullExecProtocol],
                    Tuple[EndOfStory, NullContract, NullExecProtocol],
                ]
            ],
            List[
                Union[
                    Tuple[BeginningOfStory, NullContract, NullExecProtocol],
                    Tuple[Callable, NullContract, NullExecProtocol],
                    Tuple[EndOfStory, NullContract, NullExecProtocol],
                ]
            ],
        ],
        contract: NullContract,
        failures: None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def run(
        self, **kwargs: Dict[str, Any]
    ) -> Union[SuccessSummary, FailureSummary]: ...
