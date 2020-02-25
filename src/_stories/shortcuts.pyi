from enum import Enum
from typing import Callable
from typing import Dict
from typing import List
from typing import overload
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from cerberus.validator import Validator
from marshmallow import Schema
from pydantic.main import BaseModel

_T = TypeVar("_T")
@overload
def contract_in(
    cls: _T, *args: Tuple[()]
) -> Callable[[Union[BaseModel, Schema]], _T]: ...
@overload
def contract_in(cls: _T, *args: Tuple[Dict[str, Callable]]) -> Dict[str, Callable]: ...
@overload
def contract_in(cls: _T, *args: Tuple[Validator]) -> Validator: ...
@overload
def failures_in(cls: _T, *args: Tuple[()]) -> Callable[[Type[Enum]], _T]: ...
@overload
def failures_in(cls: _T, *args: Tuple[List[str]]) -> List[str]: ...
