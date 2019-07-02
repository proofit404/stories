from typing import Any, Callable, Dict, List, Type, Union

from ._compat import CerberusSpec, Enum, MarshmallowSpec, PydanticSpec


ClassWithSpec = Any

Spec = Callable

Arguments = List[str]

Collected = List[str]

ContextContract = Union[
    PydanticSpec, MarshmallowSpec, CerberusSpec, Dict[str, Callable], None
]

FailureProtocol = Union[List[str], Type[Enum], None]

ValueVariant = Any

FailureVariant = Union[str, Enum]
