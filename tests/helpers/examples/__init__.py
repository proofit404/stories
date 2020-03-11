# -*- coding: utf-8 -*-
import sys

import pytest

import examples.methods  # noqa: F401


def runners():
    yield "function"
    if sys.version_info[:2] > (2, 7):
        yield "coroutine"


def contracts():
    yield "examples.contract.raw"
    if sys.version_info[:2] > (3, 5):
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
