from enum import Enum
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from _stories.contract import NullContract
from _stories.contract import SpecContract
from _stories.failures import NotNullExecProtocol
from _stories.failures import NullExecProtocol
from _stories.marker import BeginningOfStory
from _stories.marker import EndOfStory
from _stories.summary import FailureSummary
from _stories.summary import SuccessSummary

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
