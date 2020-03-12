# -*- coding: utf-8 -*-
from _stories.returned import Failure
from _stories.returned import Result
from _stories.returned import Skip
from _stories.returned import Success


def combine_parallel_outcomes(results):
    result = None
    if not results:
        return result

    kwargs = {}
    for result in results:
        if isinstance(result, (Failure, Result, Skip)):
            return result

        kwargs.update(result.kwargs)

    result = Success(**kwargs)

    return result
