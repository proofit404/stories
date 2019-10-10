from enum import Enum
from typing import List
from typing import NoReturn
from typing import Optional
from typing import Union

from _stories.context import Context
from _stories.failures import NotNullRunProtocol
from _stories.failures import NullRunProtocol
from _stories.summary import FailureSummary
from _stories.summary import SuccessSummary

class Call:
    def got_failure(
        self, ctx: Context, method_name: str, reason: Optional[Union[str, Enum]]
    ) -> NoReturn: ...
    def got_result(self, value: Union[List[str], int]) -> Union[List[str], int]: ...
    def finished(self) -> None: ...

class Run:
    def __init__(
        self, protocol: Union[NotNullRunProtocol, NullRunProtocol]
    ) -> None: ...
    def got_failure(
        self, ctx: Context, method_name: str, reason: Optional[Union[str, Enum]]
    ) -> FailureSummary: ...
    def got_result(self, value: Union[List[str], int]) -> SuccessSummary: ...
    def finished(self) -> SuccessSummary: ...
