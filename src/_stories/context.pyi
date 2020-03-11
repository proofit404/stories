from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Union

from _stories.contract import NullContract
from _stories.contract import SpecContract
from _stories.history import History

def make_context(
    contract: Union[SpecContract, NullContract],
    kwargs: Dict[str, Any],
    history: History,
) -> object: ...
def setattr_method(self: object, name: str, value: Any) -> NoReturn: ...
def delattr_method(self: object, name: str) -> NoReturn: ...
def assign_namespace(
    ns: Dict[str, Any], lines: List[str], method: Callable, kwargs: Dict[str, Any]
) -> None: ...
def history_representation(history: History) -> str: ...
def context_representation(
    ns: Dict[str, Any], lines: List[str], repr_func: Callable = ...
) -> str: ...
