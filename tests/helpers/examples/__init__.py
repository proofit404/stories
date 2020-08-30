import pytest


def runners():
    yield "function"
    yield "coroutine"


def contracts():
    yield "examples.contract.raw"
    yield "examples.contract.pydantic"
    yield "examples.contract.marshmallow"
    yield "examples.contract.cerberus"


# Fixtures.


@pytest.fixture(params=runners())
def r(request):
    import examples.runners

    return examples.runners.runners[request.param]


@pytest.fixture()
def c(r):
    return r.import_module("examples.context")


@pytest.fixture()
def f(r):
    return r.import_module("examples.failure_reasons")


@pytest.fixture()
def x(r):
    return r.import_module("examples.methods")


@pytest.fixture(params=contracts())
def m(r, request):
    return r.import_module(request.param)
