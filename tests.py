import examples
import pytest
from stories import Failure, Result, Success


def test_empty():

    result = examples.Empty().x()
    assert result is None

    result = examples.EmptySubstory().y()
    assert result is None

    result = examples.SubstoryDI(examples.Empty().x).y(3)
    assert result == 6


def test_failure():

    result = examples.Simple().x(2, 2)
    assert isinstance(result, Failure)

    result = examples.SimpleSubstory().y(3)
    assert isinstance(result, Failure)

    result = examples.SubstoryDI(examples.Simple().x).y(3)
    assert isinstance(result, Failure)


def test_result():

    result = examples.Simple().x(1, 3)
    assert result == -1

    result = examples.SimpleSubstory().y(2)
    assert result == -1

    result = examples.SubstoryDI(examples.Simple().x).y(2)
    assert result == -1


def test_skip():

    result = examples.Simple().x(1, -1)
    assert result is None

    result = examples.SimpleSubstory().y(-2)
    assert result == -4

    result = examples.SubstoryDI(examples.Simple().x).y(-2)
    assert result == -4


def test_arguments_validation():

    with pytest.raises(AssertionError):
        examples.Simple().x(1)

    with pytest.raises(AssertionError):
        examples.Simple().x(1, b=2)


def test_context_immutability():

    with pytest.raises(AssertionError):
        examples.ExistedKey().x(a=1)


def test_result_type():

    with pytest.raises(AssertionError):
        examples.WrongResult().x()


def test_attribute_access():

    result = examples.AttributeAccess().x()
    assert result is True


def test_inject_implementation():

    result = examples.ImplementationDI(f=lambda arg: arg + 1).x(1)
    assert result == 2
