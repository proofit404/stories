from enum import Enum
from typing import Any, Callable, List, Optional, Type, Union

from _stories.mounted import ClassMountedStory, MountedStory


class Story:
    def __init__(self, f: Callable) -> None: ...

    def __get__(self, obj: Any, cls: Any) -> Union[MountedStory, ClassMountedStory]: ...

    def contract(self, contract: Any) -> Any: ...

    def failures(self, failures: Any) -> Optional[Union[List[str], Type[Enum]]]: ...
