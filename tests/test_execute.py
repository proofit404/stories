# FIXME: Trace actual execution path.
import pytest

from stories.exceptions import FailureError


def test_signatures(r, x):
    """Story signature should not allow positional arguments."""

    class A(x.Child, x.NormalMethod):
        pass

    class B(x.Parent, x.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    class C(x.Root, x.NormalRootMethod):
        def __init__(self):
            self.b1 = B().b1

    # First level.

    expected = "__call__() takes 1 positional argument but 2 were given",

    with pytest.raises(TypeError) as exc_info:
        r(A().a1)(1)
    assert str(exc_info.value) == expected

    expected = "run() takes 1 positional argument but 2 were given"

    with pytest.raises(TypeError) as exc_info:
        r(A().a1.run)(1)
    assert str(exc_info.value) == expected

    # Second level.

    expected = "__call__() takes 1 positional argument but 2 were given"

    with pytest.raises(TypeError) as exc_info:
        r(B().b1)(1)
    assert str(exc_info.value) == expected

    expected = "run() takes 1 positional argument but 2 were given"

    with pytest.raises(TypeError) as exc_info:
        r(B().b1.run)(1)
    assert str(exc_info.value) == expected

    # Third level.

    expected = "__call__() takes 1 positional argument but 2 were given"

    with pytest.raises(TypeError) as exc_info:
        r(C().c1)(1)
    assert str(exc_info.value) == expected

    expected = "run() takes 1 positional argument but 2 were given"

    with pytest.raises(TypeError) as exc_info:
        r(C().c1.run)(1)
    assert str(exc_info.value) == expected


def test_success(r, x):
    """Success marker semantics.

    If story contains only success markers, it should execute every step sequentially
    one by one.

    """

    class A(x.Child, x.NormalMethod):
        pass

    class B(x.Parent, x.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    class C(x.Root, x.NormalRootMethod):
        def __init__(self):
            self.b1 = B().b1

    # First level.

    result = r(A().a1)()
    assert result is None

    result = r(A().a1.run)()
    assert result.is_success
    assert not result.is_failure
    assert result.value is None

    # Second level.

    result = r(B().b1)()
    assert result is None

    result = r(B().b1.run)()
    assert result.is_success
    assert not result.is_failure
    assert result.value is None

    # Third level.

    result = r(C().c1)()
    assert result is None

    result = r(C().c1.run)()
    assert result.is_success
    assert not result.is_failure
    assert result.value is None


def test_failure(r, x):
    """Failure marker semantics."""

    class A(x.ParamChild, x.FailureMethod):
        pass

    class B(x.ParamParent, x.AssignParentMethod):
        def __init__(self):
            self.a1 = A().a1

    class C(x.ParamRoot, x.AssignRootMethod):
        def __init__(self):
            self.b1 = B().b1

    # First level.

    with pytest.raises(FailureError) as exc_info:
        r(A().a1)(a1v1=2, a1v2=2)
    assert repr(exc_info.value) == "FailureError()"

    result = r(A().a1.run)(a1v1=2, a1v2=2)
    assert not result.is_success
    assert result.is_failure
    assert result.ctx.a1v1 == 2
    assert result.ctx.a1v2 == 2
    assert result.failed_on("a1s2")
    assert not result.failed_on("a1s1")
    with pytest.raises(AssertionError):
        result.value

    # Second level.

    with pytest.raises(FailureError) as exc_info:
        r(B().b1)(b1v1=3)
    assert repr(exc_info.value) == "FailureError()"

    result = r(B().b1.run)(b1v1=3)
    assert not result.is_success
    assert result.is_failure
    assert result.ctx.a1v1 == 2
    assert result.ctx.a1v2 == 4
    assert result.ctx.b1v1 == 3
    assert result.failed_on("a1s2")
    assert not result.failed_on("b1s1")
    with pytest.raises(AssertionError):
        result.value

    # Third level.

    with pytest.raises(FailureError) as exc_info:
        r(C().c1)(c1v1=5)
    assert repr(exc_info.value) == "FailureError()"

    result = r(C().c1.run)(c1v1=5)
    assert not result.is_success
    assert result.is_failure
    assert result.ctx.a1v1 == 2
    assert result.ctx.a1v2 == 4
    assert result.ctx.b1v1 == 3
    assert result.ctx.c1v1 == 5
    assert result.failed_on("a1s2")
    assert not result.failed_on("c1s1")
    with pytest.raises(AssertionError):
        result.value


def test_failure_error_private_fields(r, x):
    """Deny access to the private fields of the `FailureError` exception."""

    class A(x.ParamChild, x.FailureMethod):
        pass

    with pytest.raises(FailureError) as exc_info:
        r(A().a1)(a1v1=2, a1v2=2)
    assert exc_info.value.__dict__ == {}


def test_result(r, x):
    """Result marker semantics."""

    class A(x.ParamChild, x.ResultMethod):
        pass

    class B(x.ParamParent, x.AssignParentMethod):
        def __init__(self):
            self.a1 = A().a1

    class C(x.ParamRoot, x.AssignRootMethod):
        def __init__(self):
            self.b1 = B().b1

    # First level.

    result = r(A().a1)(a1v1=1, a1v2=3)
    assert result == -1

    result = r(A().a1.run)(a1v1=1, a1v2=3)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("a1s2")
    assert result.value == -1

    # Second level.

    result = r(B().b1)(b1v1=2)
    assert result == -1

    result = r(B().b1.run)(b1v1=2)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("a1s2")
    assert result.value == -1

    # Third level.

    result = r(C().c1)(c1v1=2)
    assert result == -1

    result = r(C().c1.run)(c1v1=2)
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_on("a1s2")
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


def test_return_type(r, x):
    """Story steps should return a marker.

    Any other value is denied.

    """

    class A(x.Child, x.PassMethod):
        pass

    class B(x.Parent, x.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    class C(x.Root, x.NormalRootMethod):
        def __init__(self):
            self.b1 = B().b1

    # First level.

    with pytest.raises(AssertionError):
        r(A().a1)()

    with pytest.raises(AssertionError):
        r(A().a1.run)()

    # Second level.

    with pytest.raises(AssertionError):
        r(B().b1)()

    with pytest.raises(AssertionError):
        r(B().b1.run)()

    # Third level.

    with pytest.raises(AssertionError):
        r(C().c1)()

    with pytest.raises(AssertionError):
        r(C().c1.run)()


def test_inject_implementation(r, x):
    """Story steps should has access to the attributes of the instance.

    The class of the instance is the same where story defined in.

    """

    class A(x.ParamChild, x.DependencyMethod):
        def __init__(self):
            self.f = lambda i, j: i + j

    class B(x.ParamParent, x.DependencyParentMethod):
        def __init__(self):
            self.a1 = A().a1
            self.f = lambda arg: arg * 2

    class C(x.ParamRoot, x.DependencyRootMethod):
        def __init__(self):
            self.b1 = B().b1
            self.f = lambda arg: arg ** 2

    # First level.

    result = r(A().a1)(a1v1=1, a1v2=2)
    assert result == 3

    result = r(A().a1.run)(a1v1=1, a1v2=2)
    assert result.is_success
    assert not result.is_failure
    assert result.value == 3

    # Second level.

    result = r(B().b1)(b1v1=7)
    assert result == 42

    result = r(B().b1.run)(b1v1=7)
    assert result.is_success
    assert not result.is_failure
    assert result.value == 42

    # Third level.

    result = r(C().c1)(c1v1=3)
    assert result == 54

    result = r(C().c1.run)(c1v1=3)
    assert result.is_success
    assert not result.is_failure
    assert result.value == 54
