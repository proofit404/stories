import pytest

from helpers import make_collector
from stories.exceptions import ContextContractError


# TODO:
#
# [ ] Apply substory validators of the substory arguments.
#
# [ ] Deny to normalize substory arguments set by parent story
#     methods.
#
# [ ] Deny unknown arguments to story call.
#
# [ ] Collect arguments from all substories.  Allow to pass arguments
#     to the substories through story call.
#
# [ ] Allow to normalize substory arguments passed to the story calls.
#
# [ ] Add `contract_in` shortcut.


def test_context_existed_variables(m):
    """
    We can not write a variable with the same name to the context
    twice.
    """

    class T(m.ParamChildWithNull, m.StringMethod):
        pass

    class Q(m.ParentWithNull, m.StringParentMethod, T):
        pass

    class J(m.ParentWithNull, m.StringParentMethod):
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
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These variables are already present in the context: 'bar', 'foo'

Function returned value: T.one

Use different names for Success() keyword arguments.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_context_variables_normalization(m):
    """
    We apply normalization to the context variables, if story defines
    context contract.  If story step returns a string holding a
    number, we should store a number in the context.
    """

    class T(m.Child, m.StringMethod):
        pass

    class Q(m.Parent, m.NormalParentMethod, T):
        pass

    class J(m.Parent, m.NormalParentMethod):
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


def test_story_arguments_normalization(m):
    """
    We apply normalization to the story arguments, if story defines
    context contract.  If story was called with a string argument
    holding a number, we should store a number in the context.
    """

    class T(m.ParamChild, m.NormalMethod):
        pass

    class Q(m.ParamParent, m.StringParentMethod, T):
        pass

    class J(m.ParamParent, m.StringParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    getter = make_collector()
    T().x(foo="1", bar="2")
    assert getter().foo == 1
    assert getter().bar == 2

    getter = make_collector()
    T().x.run(foo="1", bar="2")
    assert getter().foo == 1
    assert getter().bar == 2

    # Substory inheritance.

    getter = make_collector()
    Q().a(ham="1", eggs="2")
    assert getter().ham == 1
    assert getter().eggs == 2

    getter = make_collector()
    Q().a.run(ham="1", eggs="2")
    assert getter().ham == 1
    assert getter().eggs == 2

    # Substory DI.

    getter = make_collector()
    J().a(ham="1", eggs="2")
    assert getter().ham == 1
    assert getter().eggs == 2

    getter = make_collector()
    J().a.run(ham="1", eggs="2")
    assert getter().ham == 1
    assert getter().eggs == 2


def test_context_variables_validation(m):
    """
    We apply validators to the context variables, if story defines
    context contract.
    """

    class T(m.Child, m.WrongMethod):
        pass

    class Q(m.Parent, m.NormalParentMethod, T):
        pass

    class J(m.Parent, m.NormalParentMethod):
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


def test_story_arguments_validation(m):
    """
    We apply validators to the story arguments, if story defines
    context contract.  This is check performed during story call, not
    execution.
    """

    class T(m.ParamChild, m.NormalMethod):
        pass

    class Q(m.ParamParent, m.NormalParentMethod, m.Child, m.NormalMethod):
        pass

    class J(m.ParamParent, m.NormalParentMethod):
        def __init__(self):
            class T(m.Child, m.NormalMethod):
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
These arguments violates context contract: 'eggs', 'ham'

Story method: Q.a

Violations:

eggs:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a(ham="<boom>", eggs="<boom>")
    assert str(exc_info.value).startswith(expected)

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run(ham="<boom>", eggs="<boom>")
    assert str(exc_info.value).startswith(expected)

    # Substory DI.

    expected = """
These arguments violates context contract: 'eggs', 'ham'

Story method: J.a

Violations:

eggs:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a(ham="<boom>", eggs="<boom>")
    assert str(exc_info.value).startswith(expected)

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run(ham="<boom>", eggs="<boom>")
    assert str(exc_info.value).startswith(expected)


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


def test_composition_incompatible_contracts(m):
    """Deny to use different types in the story composition."""

    class T(m.Child, m.NormalMethod):
        pass

    class Q(m.ParentWithNull, m.NormalParentMethod, T):
        pass

    class J(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Story and substory context contracts has incompatible types:

Story method: Q.a

Story context contract: None

Substory method: Q.x

Substory context contract:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a
    assert str(exc_info.value).startswith(expected)

    # Substory DI.

    expected = """
Story and substory context contracts has incompatible types:

Story method: J.a

Story context contract: None

Substory method: T.x

Substory context contract:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a
    assert str(exc_info.value).startswith(expected)


def test_unknown_context_variable(m):
    """
    Step can't use Success argument name which was not specified in
    the contract.
    """

    class T(m.Child, m.UnknownMethod):
        pass

    class Q(m.Parent, m.NormalParentMethod, T):
        pass

    class J(m.Parent, m.NormalParentMethod):
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


@pytest.mark.parametrize("child", ["ParamChild", "ParamChildWithNull"])
@pytest.mark.parametrize(
    "parent,base", [("ParamParent", "Child"), ("ParamParentWithNull", "ChildWithNull")]
)
def test_unknown_story_arguments(m, child, parent, base):
    """
    Allow to pass known only story and substory arguments to the call.
    """

    class T(getattr(m, child), m.NormalMethod):
        pass

    class Q(getattr(m, parent), m.NormalParentMethod, getattr(m, base), m.NormalMethod):
        pass

    class J(getattr(m, parent), m.NormalParentMethod):
        def __init__(self):
            class T(getattr(m, base), m.NormalMethod):
                pass

            self.x = T().x

    # Simple.

    expected = """
These arguments are unknown: baz, fox

Story method: T.x

Story composition arguments: foo, bar
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        T().x(baz=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        T().x.run(baz=1, fox=2)
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
These arguments are unknown: beans, fox

Story method: Q.a

Story composition arguments: ham, eggs
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a(beans=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run(beans=1, fox=2)
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These arguments are unknown: beans, fox

Story method: J.a

Story composition arguments: ham, eggs
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a(beans=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run(beans=1, fox=2)
    assert str(exc_info.value) == expected


def test_missed_story_arguments(m):
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


def test_parent_steps_set_story_arguments(m):
    """
    Steps of parent stories should be able to set child stories
    arguments with `Success` marker keyword arguments.
    """

    class T(m.ParamChild, m.NormalMethod):
        pass

    class Q(m.Parent, m.StringParentMethod, T):
        pass

    class J(m.Parent, m.StringParentMethod):
        def __init__(self):
            self.x = T().x

    class R(m.Root, m.StringRootMethod, m.Parent, m.NormalParentMethod, T):
        pass

    class F(m.Root, m.StringRootMethod):
        def __init__(self):
            class J(m.Parent, m.NormalParentMethod):
                def __init__(self):
                    self.x = T().x

            self.a = J().a

    # Substory inheritance.

    getter = make_collector()
    Q().a()
    assert getter().foo == 1
    assert getter().bar == 2

    getter = make_collector()
    Q().a.run()
    assert getter().foo == 1
    assert getter().bar == 2

    getter = make_collector()
    R().i()
    assert getter().foo == 1
    assert getter().bar == 2

    getter = make_collector()
    R().i.run()
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

    getter = make_collector()
    F().i()
    assert getter().foo == 1
    assert getter().bar == 2

    getter = make_collector()
    F().i.run()
    assert getter().foo == 1
    assert getter().bar == 2


def test_arguments_should_be_declared_in_contract(m):
    """
    We should require all story arguments to be declared in the
    context contract.
    """

    class T(m.ParamChildWithShrink, m.NormalMethod):
        pass

    class Q(m.Parent, m.NormalParentMethod, T):
        pass

    class J(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
These arguments should be declared in the context contract: bar, foo

Story method: T.x

Story arguments: foo, bar, baz
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        T().x
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
These arguments should be declared in the context contract: bar, foo

Story method: Q.x

Story arguments: foo, bar, baz
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These arguments should be declared in the context contract: bar, foo

Story method: T.x

Story arguments: foo, bar, baz
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a
    assert str(exc_info.value) == expected
