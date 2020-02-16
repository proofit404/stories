# -*- coding: utf-8 -*-
import sys

import pytest

import helpers


def runners():
    yield "function"
    if sys.version_info[:2] > (2, 7):
        yield "coroutine"


def contracts():
    yield "examples.contract.raw"
    if helpers.is_installed("pydantic"):
        yield "examples.contract.pydantic"
    if helpers.is_installed("marshmallow", 2):
        yield "examples.contract.marshmallow2"
    if helpers.is_installed("marshmallow", 3):
        yield "examples.contract.marshmallow3"
    if helpers.is_installed("cerberus"):
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
