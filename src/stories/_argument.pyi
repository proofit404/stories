from typing import Callable, List, Tuple


def arguments(*names: Tuple[str]) -> Callable: ...


def get_arguments(f: Callable) -> List[str]: ...
