from enum import Enum
from typing import Any, NoReturn, Optional, Union

from stories._context import Context
from stories._failures import NotNullRunProtocol, NullRunProtocol


class FailureSummary:
    def __init__(
        self,
        protocol: Union[NullRunProtocol, NotNullRunProtocol],
        ctx: Context,
        failed_method: str,
        reason: Optional[Union[str, Enum]],
    ) -> None: ...

    def failed_on(self, method_name: str) -> bool: ...

    def failed_because(self, reason: Union[str, Enum]) -> bool: ...

    @property
    def value(self) -> NoReturn: ...

    def __repr__(self) -> str: ...


class SuccessSummary:
    def __init__(
        self, protocol: Union[NullRunProtocol, NotNullRunProtocol], value: Any
    ) -> None: ...

    def failed_on(self, method_name: str) -> bool: ...

    def failed_because(self, reason: str) -> bool: ...

    def __repr__(self) -> str: ...
