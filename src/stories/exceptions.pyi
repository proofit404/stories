from enum import Enum
from typing import Optional, Union


class FailureError:
    def __init__(self, reason: Optional[Union[str, Enum]]) -> None: ...

    def __repr__(self) -> str: ...