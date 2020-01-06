from typing import Callable
from typing import Dict
from typing import Union
from enum import Enum


Error = Union[str, Enum, Callable[[], Union[str, Enum]]]


def rescue(f: Callable, error: Error) -> Callable: ...
def get_rescues(f: Callable) -> Dict[Error, Callable]: ...
