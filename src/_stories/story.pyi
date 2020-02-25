from enum import Enum
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Type
from typing import Union

from _stories.mounted import ClassMountedStory
from _stories.mounted import MountedStory

class Story:
    def __init__(self, f: Callable) -> None: ...
    def __get__(self, obj: Any, cls: Any) -> Union[MountedStory, ClassMountedStory]: ...
    def contract(self, contract: Any) -> Any: ...
    def failures(self, failures: Any) -> Optional[Union[List[str], Type[Enum]]]: ...
