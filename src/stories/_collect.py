from .exceptions import StoryDefinitionError


def collect_story(f):

    calls = []

    class Collector(object):
        def __getattr__(self, name):
            calls.append(name)

    f(Collector())

    if not calls:
        raise StoryDefinitionError("Stories can not be empty")
    return calls
