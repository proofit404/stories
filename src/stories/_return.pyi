from enum import Enum
from typing import Any, Dict, Optional, Union


class Result:
    def __init__(self, value: Any = ...) -> None: ...

    def __repr__(self) -> str: ...


class Success:
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...

    def __repr__(self) -> str: ...


class Failure:
    def __init__(self, reason: Optional[Union[str, Enum]] = ...) -> None: ...

    def __repr__(self) -> str: ...


class Skip:
    def __repr__(self) -> str: ...
