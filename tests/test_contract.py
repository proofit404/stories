import pytest

import examples
from helpers import make_collector
from stories.exceptions import ContextContractError


def test_arguments_validation():

    with pytest.raises(AssertionError):
        examples.methods.Simple().x(1)

    with pytest.raises(AssertionError):
        examples.methods.Simple().x.run(1)

    with pytest.raises(AssertionError):
        examples.methods.Simple().x(1, b=2)

    with pytest.raises(AssertionError):
        examples.methods.Simple().x.run(1, b=2)


def test_context_immutability():

    # Simple.

    expected = """
These variables are already present in the context: 'bar', 'foo'

Function returned value: ExistedKey.one

Use different names for Success() keyword arguments.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.ExistedKey().x(1, 2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.ExistedKey().x.run(1, 2)
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
These variables are already present in the context: 'bar', 'foo'

Function returned value: SubstoryExistedKey.one

Use different names for Success() keyword arguments.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.SubstoryExistedKey().a(1, 2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.SubstoryExistedKey().a.run(1, 2)
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These variables are already present in the context: 'bar', 'foo'

Function returned value: ExistedKey.one

Use different names for Success() keyword arguments.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.ExistedKeyDI().a(1, 2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.ExistedKeyDI().a.run(1, 2)
    assert str(exc_info.value) == expected


def test_immutable_context_object():
    """
    we can't use attribute assignment and deletion with `Context`
    object.
    """

    # Assignment.

    expected = """
Context object is immutable.

Use Success() keyword arguments to expand its scope.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.AssignAttribute().x()
    assert str(exc_info.value) == expected

    # Deletion.

    expected = """
Context object is immutable.

Variables can not be removed from Context.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        examples.contract.DeleteAttribute().x(foo=1)
    assert str(exc_info.value) == expected


@pytest.mark.parametrize("m", examples.contract_modules)
def test_context_variables_normalization(m):
    """
    We apply normalization to the context variables, if story defines
    context contract.  If story step returns a string holding a
    number, we should store a number in the context.
    """

    class T(m.Child, m.StringMethod):
        pass

    class Q(m.ParentWithNull, m.NormalParentMethod, T):
        pass

    class J(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    getter = make_collector()
    T().x()
    assert getter().foo == 1
    assert getter().bar == 2

    # Substory inheritance.

    getter = make_collector()
    Q().x()
    assert getter().foo == 1
    assert getter().bar == 2

    # Substory DI.

    getter = make_collector()
    J().x()
    assert getter().foo == 1
    assert getter().bar == 2


@pytest.mark.parametrize("m", examples.contract_modules)
def test_context_variables_validation(m):
    """
    We apply validators to the context variables, if story defines
    context contract.
    """

    class T(m.Child, m.WrongMethod):
        pass

    class Q(m.ParentWithNull, m.NormalParentMethod, T):
        pass

    class J(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
These variables violates context contract: 'bar', 'foo'

Function returned value: T.one

Violations:

bar:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        T().x()
    assert str(exc_info.value).startswith(expected)

    # Substory inheritance.

    expected = """
These variables violates context contract: 'bar', 'foo'

Function returned value: Q.one

Violations:

bar:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().x()
    assert str(exc_info.value).startswith(expected)

    # Substory DI.

    expected = """
These variables violates context contract: 'bar', 'foo'

Function returned value: T.one

Violations:

bar:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().x()
    assert str(exc_info.value).startswith(expected)


@pytest.mark.parametrize("m", examples.contract_modules)
def test_context_unknown_variable(m):
    """
    Step can't use Success argument name which was not specified in
    the contract.
    """

    class T(m.Child, m.UnknownMethod):
        pass

    class Q(m.ParentWithNull, m.NormalParentMethod, T):
        pass

    class J(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
These variables were not defined in the context contract: 'quiz', 'spam'

Available variables are: 'bar', 'baz', 'foo'

Function returned value: T.one

Use different names for Success() keyword arguments or add these names to the contract.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        T().x()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
These variables were not defined in the context contract: 'quiz', 'spam'

Available variables are: 'bar', 'baz', 'foo'

Function returned value: Q.one

Use different names for Success() keyword arguments or add these names to the contract.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().x()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These variables were not defined in the context contract: 'quiz', 'spam'

Available variables are: 'bar', 'baz', 'foo'

Function returned value: T.one

Use different names for Success() keyword arguments or add these names to the contract.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().x()
    assert str(exc_info.value) == expected
