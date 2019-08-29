from typing import Any, Callable, List, Tuple, Union

from stories._contract import NullContract
from stories._failures import NullExecProtocol
from stories._marker import BeginningOfStory, EndOfStory

def wrap_story(
    arguments: List[str],
    collected: List[str],
    cls_name: str,
    story_name: str,
    obj: Any,
    spec: None,
    failures: None,
) -> Union[
    Tuple[
        List[
            Union[
                Tuple[BeginningOfStory, NullContract, NullExecProtocol],
                Tuple[Callable, NullContract, NullExecProtocol],
                Tuple[EndOfStory, NullContract, NullExecProtocol],
            ]
        ],
        NullContract,
        None,
    ],
    Tuple[
        List[
            Union[
                Tuple[BeginningOfStory, NullContract, NullExecProtocol],
                Tuple[EndOfStory, NullContract, NullExecProtocol],
            ]
        ],
        NullContract,
        None,
    ],
]: ...
