import pytest
from stories._base import Context


context_init = Context.__init__


def track_context(storage):

    def wrapper(self, ns):

        context_init(self, ns)
        storage.append(self)

    return wrapper


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    contexts = []
    Context.__init__ = track_context(contexts)
    yield
    Context.__init__ = context_init
    item.add_report_section("call", "stories", "\n\n".join(map(repr, contexts)))
