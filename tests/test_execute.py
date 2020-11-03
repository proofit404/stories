import pytest

from stories.exceptions import FailureError


def test_signatures(r, x):
    """Story signature should not allow positional arguments."""

    expected = "__call__() takes 1 positional argument but 2 were given"

    with pytest.raises(TypeError) as exc_info:
        r(x.Simple().x)(1)
    assert str(exc_info.value) == expected

    expected = "run() takes 1 positional argument but 2 were given"

    with pytest.raises(TypeError) as exc_info:
        r(x.Simple().x.run)(1)
    assert str(exc_info.value) == expected


def test_success(r, x):
    """Success marker semantics.

    If story contains only success markers, it should execute every step sequentially
    one by one.

    """

    class T(x.Child, x.NormalMethod):
        pass

    class J(x.Parent, x.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    result = r(T().x)()
    assert result is None

    result = r(T().x.run)()
    assert result.is_success
    assert not result.is_failure
    assert result.value is None

    # Substory DI.

    result = r(J().a)()
    assert result is None

    result = r(J().a.run)()
    assert result.is_success
    assert not result.is_failure
    assert result.value is None


def test_failure(r, x):
    """Failure marker semantics."""

    # Simple.

    with pytest.raises(FailureError) as exc_info:
        r(x.Simple().x)(foo=2, bar=2)
    assert repr(exc_info.value) == "FailureError()"

    result = r(x.Simple().x.run)(foo=2, bar=2)
    assert not result.is_success
    assert result.is_failure
    assert result.ctx.foo == 2
    assert result.ctx.bar == 2
    assert result.failed_on("two")
    assert not result.failed_on("one")
    with pytest.raises(AssertionError):
        result.value

    # Substory DI.

    with pytest.raises(FailureError) as exc_info:
        r(x.SubstoryDI(x.Simple().x).y)(spam=3)
    assert repr(exc_info.value) == "FailureError()"

    result = r(x.SubstoryDI(x.Simple().x).y.run)(spam=3)
    assert not result.is_success
    assert result.is_failure
    assert result.ctx.foo == 2
    assert result.ctx.bar == 4
    assert result.ctx.spam == 3
    assert result.failed_on("two")
    assert not result.failed_on("one")
    with pytest.raises(AssertionError):
        result.value


def test_failure_error_private_fields(r, x):
    """Deny access to the private fields of the `FailureError` exception."""

    with pytest.raises(FailureError) as exc_info:
        r(x.Simple().x)(foo=2, bar=2)
    assert exc_info.value.__dict__ == {}


def test_result(r, x):
    """Result marker semantics."""

    result = r(x.Simple().x)(foo=1, bar=3)
    assert result == -1

    result = r(x.Simple().x.run)(foo=1, bar=3)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert result.value == -1

    result = r(x.SubstoryDI(x.Simple().x).y)(spam=2)
    assert result == -1

    result = r(x.SubstoryDI(x.Simple().x).y.run)(spam=2)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert result.value == -1


def test_next(r, x):
    """Next marker semantics."""

    result = r(x.Simple().x)(foo=1, bar=-1)
    assert result is None

    result = r(x.Simple().x.run)(foo=1, bar=-1)
    assert result.is_success
    assert not result.is_failure
    assert result.value is None

    result = r(x.SubstoryDI(x.Simple().x).y)(spam=-2)
    assert result == -4

    result = r(x.SubstoryDI(x.Simple().x).y.run)(spam=-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4

    result = r(x.SubstoryDI(x.Pipe().y).y)(spam=-2)
    assert result == -4

    result = r(x.SubstoryDI(x.Pipe().y).y.run)(spam=-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4


def test_next_return_value(r, x):
    """Next marker semantics return value."""

    result = r(x.Simple().x)(foo=1, bar=10)
    assert result == 20

    result = r(x.Simple().x.run)(foo=1, bar=10)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("two")
    assert result.value == 20

    result = r(x.SubstoryDI(x.Simple().x).y)(spam=-2)
    assert result == -4

    result = r(x.SubstoryDI(x.Simple().x).y.run)(spam=-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4

    result = r(x.SubstoryDI(x.Pipe().y).y)(spam=-2)
    assert result == -4

    result = r(x.SubstoryDI(x.Pipe().y).y.run)(spam=-2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == -4


def test_return_type(r, x):
    """Story steps should return a marker.

    Any other value is denied.

    """

    with pytest.raises(AssertionError):
        r(x.WrongResult().x)()

    with pytest.raises(AssertionError):
        r(x.WrongResult().x.run)()


def test_inject_implementation(r, x):
    """Story steps should has access to the attributes of the instance.

    The class of the instance is the same where story defined in.

    """

    result = r(x.ImplementationDI(f=lambda arg: arg + 1).x)(foo=1)
    assert result == 2

    result = r(x.ImplementationDI(f=lambda arg: arg + 1).x.run)(foo=1)
    assert result.is_success
    assert not result.is_failure
    assert result.value == 2
