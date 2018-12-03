from ._api import story


def StoryFactory(failures=None):

    return type(story.__name__, (story,), {"failures": failures})
