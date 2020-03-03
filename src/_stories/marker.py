# -*- coding: utf-8 -*-
from _stories.execute.parallel.threads import ThreadsStoryExecutor
from _stories.returned import Success, Failure, Result


class BeginningOfStory(object):
    def __init__(self, cls_name, name):
        self.cls_name = cls_name
        self.name = name
        self.parent_name = None
        self.same_object = None

    @property
    def story_name(self):
        if self.parent_name is None:
            return self.cls_name + "." + self.name
        elif self.same_object:
            return self.parent_name
        else:
            return self.parent_name + " (" + self.cls_name + "." + self.name + ")"

    def set_parent(self, parent_name, same_object):
        self.parent_name = parent_name
        self.same_object = same_object


class EndOfStory(object):
    pass


class Parallel(object):
    def __init__(self, calls, workers):
        self.calls = calls
        self.executor = ThreadsStoryExecutor(workers)
        self.methods = []

    def __call__(self, ctx):
        results = self.executor.submit(self.methods, ctx)
        if not results:
            return None

        if any(isinstance(result, Failure) for result in results):
            return Failure()

        if all(isinstance(result, Success) for result in results):
            return Success()

        return Result(results)

    @property
    def story_name(self):
        return ' & '.join(self.calls)

    def __str__(self):
        return self.__name__

    # TODO: Figure out why we need this in context
    __self__ = object
