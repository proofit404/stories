from typing import Any, Callable, Dict, List, NoReturn, Union

from _stories.contract import NullContract, SpecContract
from _stories.history import History


def make_context(
    contract: Union[SpecContract, NullContract],
    kwargs: Dict[str, Any],
    history: History,
) -> Context: ...


class Context:
    def __getattr__(self, name: str) -> Any: ...

    def __setattr__(self, name: str, value: int) -> NoReturn: ...

    def __delattr__(self, name: str) -> NoReturn: ...

    def __repr__(self) -> str: ...

    def __dir__(self) -> List[str]: ...

    def __bool__(self) -> NoReturn: ...


def assign_namespace(
    ctx: Context, method: Callable, kwargs: Dict[str, Any]
) -> None: ...


def history_representation(ctx: Context) -> str: ...


def context_representation(ctx: Context, repr_func: Callable = ...) -> str: ...
