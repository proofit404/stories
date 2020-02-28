# -*- coding: utf-8 -*-
from _stories.exceptions import StoryDefinitionError


def collect_story(f):

    calls = []

    class Collector(object):
        def __getattr__(self, name):
            calls.append(name)

    f(Collector())

    if not calls:
        raise StoryDefinitionError("Story should have at least one step defined")

    return calls
