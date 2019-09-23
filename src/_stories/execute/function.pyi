from typing import Any, Callable, List, Tuple, Union, overload

from _stories.context import Context
from _stories.contract import NullContract, SpecContract
from _stories.failures import (
    DisabledNullExecProtocol,
    NotNullExecProtocol,
    NullExecProtocol,
)
from _stories.history import History
from _stories.marker import BeginningOfStory, EndOfStory
from _stories.returned import Failure, Result, Skip, Success
from _stories.run import Call, Run
from _stories.summary import FailureSummary, SuccessSummary


@overload
def execute(
    runner: Call,
    ctx: Context,
    history: History,
    methods: List[
        Tuple[
            Union[
                BeginningOfStory,
                Callable[[Context], Union[Result, Success, Failure, Skip]],
                EndOfStory,
            ],
            Union[NullContract, SpecContract],
            Union[NullExecProtocol, DisabledNullExecProtocol, NotNullExecProtocol],
        ],
    ],
) -> Any: ...


@overload
def execute(
    runner: Run,
    ctx: Context,
    history: History,
    methods: List[
        Tuple[
            Union[
                BeginningOfStory,
                Callable[[Context], Union[Result, Success, Failure, Skip]],
                EndOfStory,
            ],
            Union[NullContract, SpecContract],
            Union[NullExecProtocol, DisabledNullExecProtocol, NotNullExecProtocol],
        ],
    ],
) -> Union[SuccessSummary, FailureSummary]: ...
