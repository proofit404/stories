from typing import Callable
from typing import Optional
from typing import Union

from _stories.returned import Failure
from _stories.returned import Result
from _stories.returned import Skip
from _stories.returned import Success

def get_executor(
    method: Callable[[object], Union[Result, Success, Failure, Skip]],
    previous: Optional[Callable],
    cls_name: str,
    story_name: str,
) -> Callable: ...
