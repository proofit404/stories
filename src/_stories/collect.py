# -*- coding: utf-8 -*-
from _stories.compat import iscoroutinefunction
from _stories.exceptions import StoryDefinitionError
from _stories.marker import Parallel


def collect_story(f):
    if iscoroutinefunction(f):
        raise StoryDefinitionError("Story should be a regular function")

    calls = []

    class ParallelCollector(object):
        def __init__(self):
            self.calls = []

        def __getattr__(self, name):
            self.calls.append(name)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if not self.calls:
                raise StoryDefinitionError(
                    "A parallel step must have at least one step defined"
                )
            calls.append(Parallel(self.calls))

    class Collector(object):
        def __getattr__(self, name):
            calls.append(name)

        @property
        def parallel(self):
            return ParallelCollector()

    f(Collector())

    if not calls:
        raise StoryDefinitionError("Story should have at least one step defined")

    return calls
