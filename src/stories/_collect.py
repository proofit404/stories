from ._types import Collected, Spec


def collect_story(f):
    # type: (Spec) -> Collected
    calls = []

    class Collector(object):
        def __getattr__(self, name):
            # type: (str) -> None
            calls.append(name)

    f(Collector())

    return calls
