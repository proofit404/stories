import pytest

import examples
from stories.exceptions import FailureError


def test_empty():

    result = examples.methods.Empty().x()
    assert result is None

    result = examples.methods.Empty().x.run()
    assert result.is_success
    assert not result.is_failure
    assert result.value is None

    result = examples.methods.EmptySubstory().y()
    assert result is None

    result = examples.methods.EmptySubstory().y.run()
    assert result.is_success
    assert not result.is_failure
    assert result.value is None

    result = examples.methods.SubstoryDI(examples.methods.Empty().x).y(3)
    assert result == 6

    result = examples.methods.SubstoryDI(examples.methods.Empty().x).y.run(3)
    assert result.is_success
    assert not result.is_failure
    assert result.value == 6


def test_failure():

    # Simple.

    with pytest.raises(FailureError) as exc_info:
        examples.methods.Simple().x(2, 2)
    assert not exc_info.value.reason

    result = examples.methods.Simple().x.run(2, 2)
    assert not result.is_success
    assert result.is_failure
    assert not result.failure_reason
    assert result.ctx == {"foo": 2, "bar": 2}
    assert result.failed_on("two")
    assert not result.failed_on("one")
    with pytest.raises(AssertionError):
        result.value

    # Simple substory.

    with pytest.raises(FailureError) as exc_info:
        examples.methods.SimpleSubstory().y(3)
    assert not exc_info.value.reason

    result = examples.methods.SimpleSubstory().y.run(3)
    assert not result.is_success
    assert result.is_failure
    assert not result.failure_reason
    assert result.ctx == {"foo": 2, "bar": 4, "spam": 3}
    assert result.failed_on("two")
    assert not result.failed_on("one")
    with pytest.raises(AssertionError):
        result.value

    # Substory DI.

    with pytest.raises(FailureError) as exc_info:
        examples.methods.SubstoryDI(examples.methods.Simple().x).y(3)
    assert not exc_info.value.reason

    result = examples.methods.SubstoryDI(examples.methods.Simple().x).y.run(3)
    assert not result.is_success
    assert result.is_failure
    assert not result.failure_reason
    assert result.ctx == {"foo": 2, "bar": 4, "spam": 3}
    assert result.failed_on("two")
    assert not result.failed_on("one")
    with pytest.raises(AssertionError):
        result.value


def test_result():

    result = examples.methods.Simple().x(1, 3)
    assert result == -1

    result = examples.methods.Simple().x.run(1, 3)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert result.value == -1

    result = examples.methods.SimpleSubstory().y(2)
    assert result == -1

    result = examples.methods.SimpleSubstory().y.run(2)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert result.value == -1

    result = examples.methods.SubstoryDI(examples.methods.Simple().x).y(2)
    assert result == -1

    result = examples.methods.SubstoryDI(examples.methods.Simple().x).y.run(2)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert result.value == -1


def test_skip():

    result = examples.methods.Simple().x(1, -1)
    assert result is None

    result = examples.methods.Simple().x.run(1, -1)
    assert result.is_success
    assert not result.is_failure
    assert result.value is None

    result = examples.methods.SimpleSubstory().y(-2)
    assert result == -4

    result = examples.methods.SimpleSubstory().y.run(-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4

    result = examples.methods.SubstoryDI(examples.methods.Simple().x).y(-2)
    assert result == -4

    result = examples.methods.SubstoryDI(examples.methods.Simple().x).y.run(-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4

    result = examples.methods.SubstoryDI(examples.methods.SimpleSubstory().z).y(2)
    assert result == 4

    result = examples.methods.SubstoryDI(examples.methods.SimpleSubstory().z).y.run(2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == 4

    result = examples.methods.SubstoryDI(examples.methods.Pipe().y).y(-2)
    assert result == -4

    result = examples.methods.SubstoryDI(examples.methods.Pipe().y).y.run(-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4


def test_return_type():

    with pytest.raises(AssertionError):
        examples.methods.WrongResult().x()

    with pytest.raises(AssertionError):
        examples.methods.WrongResult().x.run()


def test_attribute_access():

    with pytest.raises(AssertionError):
        examples.methods.AttributeAccess().x()

    with pytest.raises(AssertionError):
        examples.methods.AttributeAccess().x.run()


def test_inject_implementation():

    result = examples.methods.ImplementationDI(f=lambda arg: arg + 1).x(1)
    assert result == 2

    result = examples.methods.ImplementationDI(f=lambda arg: arg + 1).x.run(1)
    assert result.is_success
    assert not result.is_failure
    assert result.value == 2
