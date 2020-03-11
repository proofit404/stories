from enum import Enum
from typing import Any
from typing import NoReturn
from typing import Optional
from typing import Union

from _stories.failures import NotNullRunProtocol
from _stories.failures import NullRunProtocol

def make_failure_summary(
    protocol: Union[NullRunProtocol, NotNullRunProtocol],
    ctx: object,
    failed_method: str,
    reason: Optional[Union[str, Enum]],
) -> object: ...
def failure_value_method(self: object) -> NoReturn: ...
def failure_repr_method(self: object) -> str: ...
def make_success_summary(
    protocol: Union[NullRunProtocol, NotNullRunProtocol], value: Any
) -> object: ...
def success_failed_on_method(self: object, method_name: str) -> bool: ...
def success_repr_method(self: object) -> str: ...
