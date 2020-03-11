from enum import Enum
from typing import List
from typing import NoReturn
from typing import Optional
from typing import Union

from _stories.failures import NotNullRunProtocol
from _stories.failures import NullRunProtocol

class Call:
    def got_failure(
        self, ctx: object, method_name: str, reason: Optional[Union[str, Enum]]
    ) -> NoReturn: ...
    def got_result(self, value: Union[List[str], int]) -> Union[List[str], int]: ...
    def finished(self) -> None: ...

class Run:
    def __init__(
        self, protocol: Union[NotNullRunProtocol, NullRunProtocol]
    ) -> None: ...
    def got_failure(
        self, ctx: object, method_name: str, reason: Optional[Union[str, Enum]]
    ) -> object: ...
    def got_result(self, value: Union[List[str], int]) -> object: ...
    def finished(self) -> object: ...
