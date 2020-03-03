# -*- coding: utf-8 -*-
from _stories.compat import iscoroutinefunction
from _stories.exceptions import StoryDefinitionError
from _stories.marker import Parallel


def collect_story(f):
    if iscoroutinefunction(f):
        raise StoryDefinitionError("Story should be a regular function")

    calls = []

    class ParallelCollector(object):
        def __init__(self, workers=None):
            self._workers = workers
            self._calls = []

        def __getattr__(self, name):
            self._calls.append(name)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            calls.append(Parallel(self._calls, self._workers))

    class Collector(object):
        def parallel(self, workers=None):
            return ParallelCollector(workers)

        def __getattr__(self, name):
            if not name.startswith('__'):
                calls.append(name)

    f(Collector())

    if not calls:
        raise StoryDefinitionError("Story should have at least one step defined")

    return calls
