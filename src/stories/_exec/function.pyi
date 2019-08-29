from typing import Callable, List, Optional, Tuple, Union

from stories._context import Context
from stories._contract import NullContract, SpecContract
from stories._failures import (
    DisabledNullExecProtocol,
    NotNullExecProtocol,
    NullExecProtocol,
)
from stories._history import History
from stories._marker import BeginningOfStory, EndOfStory
from stories._run import Call, Run
from stories._summary import FailureSummary, SuccessSummary


def execute(
    runner: Union[Call, Run],
    ctx: Context,
    history: History,
    methods: Union[
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
                Tuple[BeginningOfStory, NullContract, DisabledNullExecProtocol],
                Tuple[Callable, NullContract, DisabledNullExecProtocol],
                Tuple[EndOfStory, NullContract, DisabledNullExecProtocol],
                Tuple[EndOfStory, NullContract, NotNullExecProtocol],
            ]
        ],
        List[
            Union[
                Tuple[BeginningOfStory, NullContract, NotNullExecProtocol],
                Tuple[Callable, NullContract, NotNullExecProtocol],
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
                Tuple[BeginningOfStory, NullContract, NullExecProtocol],
                Tuple[Callable, NullContract, NullExecProtocol],
                Tuple[EndOfStory, NullContract, NullExecProtocol],
            ]
        ],
    ],
) -> Optional[Union[List[str], SuccessSummary, FailureSummary, int]]: ...
