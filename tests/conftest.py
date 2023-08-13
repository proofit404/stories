import pytest

from fixtures import asynchronous
from fixtures import S
from fixtures import synchronous


@pytest.fixture(params=[synchronous, asynchronous])
def s(request: pytest.FixtureRequest) -> S:
    result: S = request.param
    return result
