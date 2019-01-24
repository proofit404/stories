import pytest

import examples
from stories.exceptions import ContextContractError, FailureError


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
    assert repr(exc_info.value) == "FailureError()"

    result = examples.methods.Simple().x.run(2, 2)
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
        examples.methods.SimpleSubstory().y(3)
    assert repr(exc_info.value) == "FailureError()"

    result = examples.methods.SimpleSubstory().y.run(3)
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
        examples.methods.SubstoryDI(examples.methods.Simple().x).y(3)
    assert repr(exc_info.value) == "FailureError()"

    result = examples.methods.SubstoryDI(examples.methods.Simple().x).y.run(3)
    assert not result.is_success
    assert result.is_failure
    assert result.ctx.foo == 2
    assert result.ctx.bar == 4
    assert result.ctx.spam == 3
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


def test_missing_substory_arguments():

    expected = """
These variables are missing from the context: bar, foo

Story method: MissingContextSubstory.x

Story arguments: foo, bar

MissingContextSubstory.y
  before
  x

Context()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        examples.methods.MissingContextSubstory().y()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        examples.methods.MissingContextSubstory().y.run()
    assert str(exc_info.value) == expected

    expected = """
These variables are missing from the context: bar, foo

Story method: Simple.x

Story arguments: foo, bar

MissingContextDI.y
  before
  x (Simple.x)

Context()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        examples.methods.MissingContextDI().y()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        examples.methods.MissingContextDI().y.run()
    assert str(exc_info.value) == expected
