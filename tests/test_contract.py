import pytest

import examples
from helpers import make_collector
from stories.exceptions import ContextContractError


# TODO:
#
# [ ] Store normalized story arguments in the context.
#
# [ ] Apply substory validators of the substory arguments.
#
# [ ] Deny to normalize substory arguments set by parent story
#     methods.
#
# [ ] Context validators should present for every story argument.
#
# [ ] Deny unknown arguments to story call.
#
# [ ] Collect arguments from all substories.  Allow to pass arguments
#     to the substories through story call.
#
# [ ] Allow to normalize substory arguments passed to the story calls.
#
# [ ] Add `contract_in` shortcut.
#
# [ ] Raise `ContextContractError` if Root and Child contracts define
#     same variables in the composition Root -> Parent -> Child.
#
# [ ] Raise `ContextContractError` if contracts in the composition are
#     of different types.


@pytest.mark.parametrize("m", examples.contracts)
def test_context_existed_variables(m):
    """
    We can not write a variable with the same name to the context
    twice.
    """

    class T(m.ParamChildWithNull, m.StringMethod):
        pass

    class Q(m.ParamParentWithNull, m.NormalParentMethod, T):
        pass

    class J(m.ParamParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
These variables are already present in the context: 'bar', 'foo'

Function returned value: T.one

Use different names for Success() keyword arguments.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        T().x(foo=1, bar=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        T().x.run(foo=1, bar=2)
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
These variables are already present in the context: 'bar', 'foo'

Function returned value: Q.one

Use different names for Success() keyword arguments.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a(foo=1, bar=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run(foo=1, bar=2)
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These variables are already present in the context: 'bar', 'foo'

Function returned value: T.one

Use different names for Success() keyword arguments.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a(foo=1, bar=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run(foo=1, bar=2)
    assert str(exc_info.value) == expected


@pytest.mark.parametrize("m", examples.contracts)
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

    getter = make_collector()
    T().x.run()
    assert getter().foo == 1
    assert getter().bar == 2

    # Substory inheritance.

    getter = make_collector()
    Q().a()
    assert getter().foo == 1
    assert getter().bar == 2

    getter = make_collector()
    Q().a.run()
    assert getter().foo == 1
    assert getter().bar == 2

    # Substory DI.

    getter = make_collector()
    J().a()
    assert getter().foo == 1
    assert getter().bar == 2

    getter = make_collector()
    J().a.run()
    assert getter().foo == 1
    assert getter().bar == 2


@pytest.mark.parametrize("m", examples.contracts)
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

    with pytest.raises(ContextContractError) as exc_info:
        T().x.run()
    assert str(exc_info.value).startswith(expected)

    # Substory inheritance.

    expected = """
These variables violates context contract: 'bar', 'foo'

Function returned value: Q.one

Violations:

bar:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a()
    assert str(exc_info.value).startswith(expected)

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run()
    assert str(exc_info.value).startswith(expected)

    # Substory DI.

    expected = """
These variables violates context contract: 'bar', 'foo'

Function returned value: T.one

Violations:

bar:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a()
    assert str(exc_info.value).startswith(expected)

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run()
    assert str(exc_info.value).startswith(expected)


@pytest.mark.parametrize("m", examples.contracts)
def test_story_arguments_validation(m):
    """
    We apply validators to the story arguments, if story defines
    context contract.  This is check performed during story call, not
    execution.
    """

    class T(m.ParamChild, m.NormalMethod):
        pass

    class Q(m.ParamParent, m.NormalParentMethod, m.ChildWithNull, m.NormalMethod):
        pass

    class J(m.ParamParent, m.NormalParentMethod):
        def __init__(self):
            class T(m.ChildWithNull, m.NormalMethod):
                pass

            self.x = T().x

    # Simple.

    expected = """
These arguments violates context contract: 'bar', 'foo'

Story method: T.x

Violations:

bar:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        T().x(foo="<boom>", bar="<boom>")
    assert str(exc_info.value).startswith(expected)

    with pytest.raises(ContextContractError) as exc_info:
        T().x.run(foo="<boom>", bar="<boom>")
    assert str(exc_info.value).startswith(expected)

    # Substory inheritance.

    expected = """
These arguments violates context contract: 'bar', 'foo'

Story method: Q.a

Violations:

bar:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a(foo="<boom>", bar="<boom>")
    assert str(exc_info.value).startswith(expected)

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run(foo="<boom>", bar="<boom>")
    assert str(exc_info.value).startswith(expected)

    # Substory DI.

    expected = """
These arguments violates context contract: 'bar', 'foo'

Story method: J.a

Violations:

bar:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a(foo="<boom>", bar="<boom>")
    assert str(exc_info.value).startswith(expected)

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run(foo="<boom>", bar="<boom>")
    assert str(exc_info.value).startswith(expected)


@pytest.mark.paramparent("m", examples.contracts)
def test_composition_contract_conflict(m):
    """
    Story and substory contracts can not declare the same variable
    twice.
    """

    class T(m.Child, m.NormalMethod):
        pass

    class Q(m.ParentWithSame, m.NormalParentMethod, T):
        pass

    class J(m.ParentWithSame, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'bar', 'baz', 'foo'

Story method: Q.a

Substory method: Q.x

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'bar', 'baz', 'foo'

Story method: J.a

Substory method: T.x

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a
    assert str(exc_info.value) == expected


@pytest.mark.paramparent("m", examples.contracts)
def test_many_levels_composition_contract_conflict(m):
    """
    Story and substory contracts can not declare the same variable
    twice.
    """

    class T(m.Child, m.NormalMethod):
        pass

    class Q(m.Parent, m.NormalParentMethod, T):
        pass

    class J(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    class R(m.RootWithSame, m.NormalRootMethod, Q):
        pass

    class F(m.RootWithSame, m.NormalRootMethod):
        def __init__(self):
            self.a = J().a

    # Substory inheritance.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'bar', 'baz', 'foo'

Story method: R.i

Substory method: R.x

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        R().i
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'bar', 'baz', 'foo'

Story method: F.i

Substory method: T.x

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        F().i
    assert str(exc_info.value) == expected


@pytest.mark.parametrize("m", examples.contracts)
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

    with pytest.raises(ContextContractError) as exc_info:
        T().x.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
These variables were not defined in the context contract: 'quiz', 'spam'

Available variables are: 'bar', 'baz', 'foo'

Function returned value: Q.one

Use different names for Success() keyword arguments or add these names to the contract.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These variables were not defined in the context contract: 'quiz', 'spam'

Available variables are: 'bar', 'baz', 'foo'

Function returned value: T.one

Use different names for Success() keyword arguments or add these names to the contract.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


@pytest.mark.parametrize("m", examples.contracts)
def test_context_missing_arguments(m):
    """Check story and substory arguments are present in the context."""

    class T(m.ParamChildWithNull, m.NormalMethod):
        pass

    class Q(m.ParentWithNull, m.NormalParentMethod, T):
        pass

    class J(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
These variables are missing from the context: bar, foo

Story method: T.x

Story arguments: foo, bar

T.x

Context()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        T().x()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        T().x.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
These variables are missing from the context: bar, foo

Story method: Q.x

Story arguments: foo, bar

Q.a
  before
  x

Context()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These variables are missing from the context: bar, foo

Story method: T.x

Story arguments: foo, bar

J.a
  before
  x (T.x)

Context()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected
