from typing import Any, Callable, Dict, List, NewType, Type

from ._compat import CerberusSpec, Enum, MarshmallowSpec, PydanticSpec


ClassWithSpec = NewType("ClassWithSpec", Any)

Spec = NewType("Spec", Callable)

Arguments = NewType("Arguments", List[str])

Collected = NewType("Collected", List[str])

ContextContract = NewType(
    "ContextContract",
    (PydanticSpec, MarshmallowSpec, CerberusSpec, Dict[str, Callable], None),
)

FailureProtocol = NewType("FailureProtocol", (List[str], Type[Enum], None))

ValueVariant = NewType("ValueVariant", Any)

FailureVariant = NewType("FailureVariant", (str, Enum))
