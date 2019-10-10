from typing import Any
from typing import Callable
from typing import List
from typing import Tuple
from typing import Union

from _stories.contract import NullContract
from _stories.contract import SpecContract
from _stories.failures import NotNullExecProtocol
from _stories.failures import NullExecProtocol
from _stories.marker import BeginningOfStory
from _stories.marker import EndOfStory

def wrap_story(
    arguments: List[str],
    collected: List[str],
    cls_name: str,
    story_name: str,
    obj: Any,
    spec: None,
    failures: None,
) -> Tuple[
    List[
        Tuple[
            Union[BeginningOfStory, Callable, EndOfStory],
            Union[NullContract, SpecContract],
            Union[NullExecProtocol, NotNullExecProtocol],
        ],
    ],
    NullContract,
    None,
]: ...
