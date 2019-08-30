from enum import Enum
from typing import List, Optional, Union

from stories._context import Context
from stories._failures import NotNullRunProtocol, NullRunProtocol
from stories._summary import FailureSummary, SuccessSummary


class Call:
    def got_failure(
        self, ctx: Context, method_name: str, reason: Optional[Union[str, Enum]]
    ): ...

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
