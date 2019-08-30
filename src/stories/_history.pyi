from enum import Enum
from typing import Any, Optional, Union


class History:
    def __init__(self) -> None: ...

    def before_call(self, method_name: str) -> None: ...

    def on_result(self, value: Any) -> None: ...

    def on_failure(self, reason: Optional[Union[str, Enum]]) -> None: ...

    def on_skip(self) -> None: ...

    def on_error(self, error_name: str) -> None: ...

    def on_substory_start(self) -> None: ...

    def on_substory_end(self) -> None: ...
