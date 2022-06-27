import pytest


# Fixtures.


@pytest.fixture(params=["function", "coroutine"])
def r(request):
    """Execute stories in synchronous and asynchronous environments."""
    import examples.runners

    return examples.runners.runners[request.param]


@pytest.fixture()
def m(r):
    """Story method definitions."""
    return r.import_module("examples.methods")
