from typing import List
from typing import Union

from _stories.returned import Failure
from _stories.returned import Result
from _stories.returned import Skip
from _stories.returned import Success

def combine_parallel_outcomes(
    results: List[Union[Result, Success, Failure, Skip]]
) -> Union[Result, Success, Failure, Skip]: ...
