# -*- coding: utf-8 -*-
from _stories.compat import iscoroutinefunction
from _stories.exceptions import StoryDefinitionError


def collect_story(f):
    if iscoroutinefunction(f):
        raise StoryDefinitionError("Story should be a regular function")

    calls = []

    class Collector(object):
        def __getattr__(self, name):
            if __debug__:
                # Workaround PyDev calling __len__ on the collector
                # instance
                import os

                if name == "__len__" and "PYDEVD_LOAD_VALUES_ASYNC" in os.environ:
                    return
            calls.append(name)

    f(Collector())

    if not calls:
        raise StoryDefinitionError("Story should have at least one step defined")

    return calls
