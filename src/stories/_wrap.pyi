from typing import Any, Callable, List, Tuple, Union

from stories._contract import NullContract, SpecContract
from stories._failures import NotNullExecProtocol, NullExecProtocol
from stories._marker import BeginningOfStory, EndOfStory


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
