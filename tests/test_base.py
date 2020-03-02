# -*- coding: utf-8 -*-
import pytest

import examples
from stories.exceptions import FailureError


def test_signatures():

    expected = {
        "__call__() takes 1 positional argument but 2 were given",
        "__call__() takes exactly 1 argument (2 given)",  # Python 2.
    }

    with pytest.raises(TypeError) as exc_info:
        examples.methods.Simple().x(1)
    assert str(exc_info.value) in expected

    expected = {
        "run() takes 1 positional argument but 2 were given",
        "run() takes exactly 1 argument (2 given)",  # Python 2.
    }

    with pytest.raises(TypeError) as exc_info:
        examples.methods.Simple().x.run(1)
    assert str(exc_info.value) in expected


def test_failure():

    # Simple.

    with pytest.raises(FailureError) as exc_info:
        examples.methods.Simple().x(foo=2, bar=2)
    assert repr(exc_info.value) == "FailureError()"

    result = examples.methods.Simple().x.run(foo=2, bar=2)
    assert not result.is_success
    assert result.is_failure
    assert result.ctx.foo == 2
    assert result.ctx.bar == 2
    assert result.failed_on("two")
    assert not result.failed_on("one")
    with pytest.raises(AssertionError):
        result.value

    # Simple substory.

    with pytest.raises(FailureError) as exc_info:
        examples.methods.SimpleSubstory().y(spam=3)
    assert repr(exc_info.value) == "FailureError()"

    result = examples.methods.SimpleSubstory().y.run(spam=3)
    assert not result.is_success
    assert result.is_failure
    assert result.ctx.foo == 2
    assert result.ctx.bar == 4
    assert result.ctx.spam == 3
    assert result.failed_on("two")
    assert not result.failed_on("one")
    with pytest.raises(AssertionError):
        result.value

    # Substory DI.

    with pytest.raises(FailureError) as exc_info:
        examples.methods.SubstoryDI(examples.methods.Simple().x).y(spam=3)
    assert repr(exc_info.value) == "FailureError()"

    result = examples.methods.SubstoryDI(examples.methods.Simple().x).y.run(spam=3)
    assert not result.is_success
    assert result.is_failure
    assert result.ctx.foo == 2
    assert result.ctx.bar == 4
    assert result.ctx.spam == 3
    assert result.failed_on("two")
    assert not result.failed_on("one")
    with pytest.raises(AssertionError):
        result.value


def test_failure_error_private_fields():
    """Deny access to the private fields of the `FailureError` exception."""

    with pytest.raises(FailureError) as exc_info:
        examples.methods.Simple().x(foo=2, bar=2)
    assert exc_info.value.__dict__ == {}


def test_result():

    result = examples.methods.Simple().x(foo=1, bar=3)
    assert result == -1

    result = examples.methods.Simple().x.run(foo=1, bar=3)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert result.value == -1

    result = examples.methods.SimpleSubstory().y(spam=2)
    assert result == -1

    result = examples.methods.SimpleSubstory().y.run(spam=2)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert result.value == -1

    result = examples.methods.SubstoryDI(examples.methods.Simple().x).y(spam=2)
    assert result == -1

    result = examples.methods.SubstoryDI(examples.methods.Simple().x).y.run(spam=2)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert result.value == -1


def test_skip():

    result = examples.methods.Simple().x(foo=1, bar=-1)
    assert result is None

    result = examples.methods.Simple().x.run(foo=1, bar=-1)
    assert result.is_success
    assert not result.is_failure
    assert result.value is None

    result = examples.methods.SimpleSubstory().y(spam=-2)
    assert result == -4

    result = examples.methods.SimpleSubstory().y.run(spam=-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4

    result = examples.methods.SubstoryDI(examples.methods.Simple().x).y(spam=-2)
    assert result == -4

    result = examples.methods.SubstoryDI(examples.methods.Simple().x).y.run(spam=-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4

    result = examples.methods.SubstoryDI(examples.methods.SimpleSubstory().z).y(spam=2)
    assert result == 4

    result = examples.methods.SubstoryDI(examples.methods.SimpleSubstory().z).y.run(
        spam=2
    )
    assert result.is_success
    assert not result.is_failure
    assert result.value == 4

    result = examples.methods.SubstoryDI(examples.methods.Pipe().y).y(spam=-2)
    assert result == -4

    result = examples.methods.SubstoryDI(examples.methods.Pipe().y).y.run(spam=-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4


def test_return_type():

    with pytest.raises(AssertionError):
        examples.methods.WrongResult().x()

    with pytest.raises(AssertionError):
        examples.methods.WrongResult().x.run()


def test_inject_implementation():

    result = examples.methods.ImplementationDI(f=lambda arg: arg + 1).x(foo=1)
    assert result == 2

    result = examples.methods.ImplementationDI(f=lambda arg: arg + 1).x.run(foo=1)
    assert result.is_success
    assert not result.is_failure
    assert result.value == 2
