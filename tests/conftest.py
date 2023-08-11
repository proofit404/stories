import pytest
from _pytest.fixtures import SubRequest

from fixtures import asynchronous
from fixtures import synchronous


@pytest.fixture(params=[synchronous, asynchronous])
def s(request: SubRequest):
    return request.param
