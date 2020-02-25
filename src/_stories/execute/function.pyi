from typing import Any
from typing import Callable
from typing import List
from typing import overload
from typing import Tuple
from typing import Union

from _stories.context import Context
from _stories.contract import NullContract
from _stories.contract import SpecContract
from _stories.failures import DisabledNullExecProtocol
from _stories.failures import NotNullExecProtocol
from _stories.failures import NullExecProtocol
from _stories.history import History
from _stories.marker import BeginningOfStory
from _stories.marker import EndOfStory
from _stories.returned import Failure
from _stories.returned import Result
from _stories.returned import Skip
from _stories.returned import Success
from _stories.run import Call
from _stories.run import Run
from _stories.summary import FailureSummary
from _stories.summary import SuccessSummary
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
