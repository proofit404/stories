from asyncio import iscoroutinefunction

from _stories.exceptions import StoryDefinitionError


def collect_story(f):
    if iscoroutinefunction(f):
        raise StoryDefinitionError("Story should be a regular function")

    calls = []

    class Collector:
        def __getattr__(self, name):
            if name in calls:
                raise StoryDefinitionError("Story has repeated steps: " + name)
            calls.append(name)

    f(Collector())

    if not calls:
        raise StoryDefinitionError("Story should have at least one step defined")
    elif f.__name__ in calls:
        raise StoryDefinitionError("Story should not call itself recursively")

    return calls
