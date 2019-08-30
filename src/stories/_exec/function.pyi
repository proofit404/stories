from typing import Any, Callable, List, Tuple, Union, overload

from stories._context import Context
from stories._contract import NullContract, SpecContract
from stories._failures import (
    DisabledNullExecProtocol,
    NotNullExecProtocol,
    NullExecProtocol,
)
from stories._history import History
from stories._marker import BeginningOfStory, EndOfStory
from stories._return import Failure, Result, Skip, Success
from stories._run import Call, Run
from stories._summary import FailureSummary, SuccessSummary


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
