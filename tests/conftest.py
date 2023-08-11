import pytest

from fixtures import asynchronous
from fixtures import synchronous


@pytest.fixture(params=[synchronous, asynchronous])
def s(request: SubRequest):
    return request.param
