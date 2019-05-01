import pytest

from helpers import make_collector
from stories.exceptions import ContextContractError


# TODO:
#
# [ ] Show collected arguments of the story composition in the error
#     messages.
#
# [ ] Show violation values in validation error messages.
#
# [ ] Write correct and verbose docstrings for each test in this
#     module.


def test_assign_existed_variables(m):
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
        T().x(foo=1, bar=[2])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        T().x.run(foo=1, bar=[2])
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
    assert getter().bar == [2]

    getter = make_collector()
    T().x.run()
    assert getter().foo == 1
    assert getter().bar == [2]

    # Substory inheritance.

    getter = make_collector()
    Q().a()
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    Q().a.run()
    assert getter().foo == 1
    assert getter().bar == [2]

    # Substory DI.

    getter = make_collector()
    J().a()
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    J().a.run()
    assert getter().foo == 1
    assert getter().bar == [2]


def test_context_variables_normalization_conflict(m):
    """
    More than one substory can declare an argument with the same name.
    This means validators of both substories should return the same
    result.
    """

    # FIXME: Normalization conflict can consist of two
    # variables.  The first variable can be set by one
    # substory.  The second variable can be set by
    # another substory.

    class T(m.ParamChild, m.NormalMethod):
        pass

    class E(m.NextParamChildWithString, m.NormalNextMethod):
        pass

    class Q(m.SequentialParent, m.StringParentMethod, T, E):
        pass

    class J(m.SequentialParent, m.StringParentMethod):
        def __init__(self):
            self.x = T().x
            self.y = E().y

    # Substory inheritance.

    expected = """
These arguments have normalization conflict: 'bar', 'foo'

Story method: Q.x

Story normalization result:
 - bar: [2]
 - foo: 1

Story method: Q.y

Story normalization result:
 - bar: ['2']
 - foo: '1'
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These arguments have normalization conflict: 'bar', 'foo'

Story method: E.y

Story normalization result:
 - bar: ['2']
 - foo: '1'

Story method: T.x

Story normalization result:
 - bar: [2]
 - foo: 1
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


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
    T().x(foo="1", bar=["2"])
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    T().x.run(foo="1", bar=["2"])
    assert getter().foo == 1
    assert getter().bar == [2]

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


def test_story_arguments_normalization_many_levels(m):
    """
    We apply normalization to the story arguments on any levels of
    story composition.
    """

    class T(m.ParamChild, m.NormalMethod):
        pass

    class Q(m.ParamParent, m.NormalParentMethod, T):
        pass

    class J(m.ParamParent, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    class R(m.ParamRoot, m.NormalRootMethod, Q):
        pass

    class F(m.ParamRoot, m.NormalRootMethod):
        def __init__(self):
            self.a = J().a

    # Substory inheritance.

    getter = make_collector()
    Q().a(ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]

    getter = make_collector()
    Q().a.run(ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]

    getter = make_collector()
    R().i(fizz="0", ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().fizz == 0
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]

    getter = make_collector()
    R().i.run(fizz="0", ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().fizz == 0
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]

    # Substory DI.

    getter = make_collector()
    Q().a(ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]

    getter = make_collector()
    Q().a.run(ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]

    getter = make_collector()
    F().i(fizz="0", ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().fizz == 0
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]

    getter = make_collector()
    F().i.run(fizz="0", ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().fizz == 0
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]


def test_story_arguments_normalization_conflict(m):
    """
    Story and substory can have an argument with the same name.  They
    both will define validators for this argument.  If normalization
    result of both contracts will mismatch we should raise an error.
    """

    class T(m.ParamChild, m.NormalMethod):
        pass

    class Q(m.ParamParentWithSameWithString, m.NormalParentMethod, T):
        pass

    class J(m.ParamParentWithSameWithString, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
These arguments have normalization conflict: 'bar', 'foo'

Story method: Q.a

Story normalization result:
 - bar: ['2']
 - foo: '1'

Story method: Q.x

Story normalization result:
 - bar: [2]
 - foo: 1
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a(foo="1", bar=["2"])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run(foo="1", bar=["2"])
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These arguments have normalization conflict: 'bar', 'foo'

Story method: J.a

Story normalization result:
 - bar: ['2']
 - foo: '1'

Story method: T.x

Story normalization result:
 - bar: [2]
 - foo: 1
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a(foo="1", bar=["2"])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run(foo="1", bar=["2"])
    assert str(exc_info.value) == expected


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

    class T(m.ParamChild, m.ExceptionMethod):
        pass

    class Q(m.ParamParent, m.ExceptionParentMethod, m.Child, m.NormalMethod):
        pass

    class J(m.ParamParent, m.ExceptionParentMethod):
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
        T().x(foo="<boom>", bar=["<boom>"])
    assert str(exc_info.value).startswith(expected)

    with pytest.raises(ContextContractError) as exc_info:
        T().x.run(foo="<boom>", bar=["<boom>"])
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


def test_story_arguments_validation_many_levels(m):
    """
    We apply contract validation to the story arguments on any levels
    of story composition.
    """

    class T(m.ParamChild, m.NormalMethod):
        pass

    class Q(m.Parent, m.ExceptionParentMethod, T):
        pass

    class J(m.Parent, m.ExceptionParentMethod):
        def __init__(self):
            self.x = T().x

    class R(m.Root, m.ExceptionRootMethod, m.Parent, m.NormalParentMethod, T):
        pass

    class F(m.Root, m.ExceptionRootMethod):
        def __init__(self):
            class J(m.Parent, m.NormalParentMethod):
                def __init__(self):
                    self.x = T().x

            self.a = J().a

    # Substory inheritance.

    expected = """
These arguments violates context contract: 'foo'

Story method: R.i

Violations:

foo:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        R().i(foo="<boom>", bar=[1])
    assert str(exc_info.value).startswith(expected)

    with pytest.raises(ContextContractError) as exc_info:
        R().i.run(foo="<boom>", bar=[1])
    assert str(exc_info.value).startswith(expected)

    # Substory DI.

    expected = """
These arguments violates context contract: 'foo'

Story method: F.i

Violations:

foo:
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        F().i(foo="<boom>", bar=[1])
    assert str(exc_info.value).startswith(expected)

    with pytest.raises(ContextContractError) as exc_info:
        F().i.run(foo="<boom>", bar=[1])
    assert str(exc_info.value).startswith(expected)


def test_composition_contract_variable_conflict(m):
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


def test_composition_contract_variable_conflict_many_levels(m):
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


def test_composition_contract_variable_conflict_sequential(m):
    """
    Story and substory contracts can not declare the same variable
    twice.
    """

    class T(m.Child, m.NormalMethod):
        pass

    class E(m.NextChildWithSame, m.NormalMethod):
        pass

    class Q(m.SequentialParent, m.StringParentMethod, T, E):
        pass

    class J(m.SequentialParent, m.StringParentMethod):
        def __init__(self):
            self.x = T().x
            self.y = E().y

    # Substory inheritance.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'bar', 'baz', 'foo'

Story method: Q.x

Substory method: Q.y

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        Q().a
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'bar', 'baz', 'foo'

Story method: T.x

Substory method: E.y

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a
    assert str(exc_info.value) == expected


def test_composition_contract_variable_conflict_sequential_reuse(m):
    """
    Story and substory can reuse the same contract.  Substory can have
    more arguments than story.  Another sequential substory can have
    the same arguments as previous substory.
    """

    class E(m.NextParamChildReuse, m.NormalMethod):
        pass

    class Q(m.ParamParentWithSame, m.NormalParentMethod):
        pass

    class V(m.NextParamParentReuse, m.NormalParentMethod, E):
        pass

    class R(m.SequentialRoot, m.StringWideRootMethod, Q, V):
        pass

    class F(m.SequentialRoot, m.StringWideRootMethod):
        def __init__(self):
            self.a = Q().a
            self.b = V().b

    # Substory inheritance.

    R().i()

    result = R().i.run()
    assert result.value is None

    # Substory DI.

    F().i()

    result = F().i.run()
    assert result.value is None


def test_composition_incompatible_contract_types(m):
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


def test_composition_use_same_contract_instance(m):
    """
    The same contract class or instance can be used in story and a
    substory.  This should not lead to the incompatible contract
    composition error.  Variable declared there can be assigned in one
    of the story.  And it will be declared once within the contract.
    """

    class T(m.ChildReuse, m.NormalMethod):
        pass

    class Q(m.ParentReuse, m.NormalParentMethod, T):
        pass

    class J(m.ParentReuse, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    Q().a

    # Substory DI.

    J().a


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


@pytest.mark.parametrize(
    "child,parent", [("Child", "Parent"), ("ChildWithNull", "ParentWithNull")]
)
def test_unknown_story_arguments_with_empty(m, child, parent):
    """
    Deny any arguments in the call, if story and substory has no
    arguments specified.
    """

    class T(getattr(m, child), m.NormalMethod):
        pass

    class Q(getattr(m, parent), m.NormalParentMethod, T):
        pass

    class J(getattr(m, parent), m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
These arguments are unknown: baz, fox

Story method: T.x

Story composition has no arguments.
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

Story composition has no arguments.
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

Story composition has no arguments.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a(beans=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run(beans=1, fox=2)
    assert str(exc_info.value) == expected


def test_require_story_arguments_present_in_context(m):
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
        T().x()  # FIXME: This should be arguments error (not substory call error).
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
    assert getter().bar == [2]

    getter = make_collector()
    Q().a.run()
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    R().i()
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    R().i.run()
    assert getter().foo == 1
    assert getter().bar == [2]

    # Substory DI.

    getter = make_collector()
    J().a()
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    J().a.run()
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    F().i()
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    F().i.run()
    assert getter().foo == 1
    assert getter().bar == [2]


def test_sequential_story_steps_set_story_arguments(m):
    """
    There are a few sequential substories with one common parent
    story.  One substory should be able to set variable to provide an
    argument to the next sequential story.
    """

    class T(m.ChildWithShrink, m.StringMethod):
        pass

    class E(m.NextParamChildWithString, m.NormalNextMethod):
        pass

    class Q(m.SequentialParent, m.NormalParentMethod, T, E):
        pass

    class J(m.SequentialParent, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x
            self.y = E().y

    # Substory inheritance.

    getter = make_collector()
    Q().a()
    assert getter().foo == "1"
    assert getter().bar == ["2"]

    getter = make_collector()
    Q().a.run()
    assert getter().foo == "1"
    assert getter().bar == ["2"]

    # Substory DI.

    getter = make_collector()
    J().a()
    assert getter().foo == "1"
    assert getter().bar == ["2"]

    getter = make_collector()
    J().a.run()
    assert getter().foo == "1"
    assert getter().bar == ["2"]


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


# Aliases.


def test_story_variable_alias_normalization_store_same_object(m):
    """
    When story step sets a set of variables some of them are aliases
    of each other.  If the type and the value of alias are equal to
    the origin value, we should preserve the same reference to the
    value.
    """

    class T(m.ChildAlias, m.AliasMethod):
        pass

    # Simple.

    getter = make_collector()
    T().x()
    assert getter().foo is getter().bar
    assert getter().foo == {"key": "1"}
    assert getter().bar == {"key": "1"}
    assert getter().baz == {"key": 1}

    getter = make_collector()
    T().x.run()
    assert getter().foo is getter().bar
    assert getter().foo == {"key": "1"}
    assert getter().bar == {"key": "1"}
    assert getter().baz == {"key": 1}

    # FIXME: Substory inheritance.

    # FIXME: Substory DI.


def test_story_argument_alias_normalization_store_same_object(m):
    """
    When story has a set of arguments some of them are aliases of each
    other.  If the type and the value of alias are equal to the origin
    value, we should preserve the same reference to the value.
    """

    class T(m.ParamChildAlias, m.NormalMethod):
        pass

    # Simple.

    value = {"key": "1"}

    getter = make_collector()
    T().x(foo=value, bar=value, baz=value)
    assert getter().foo is getter().bar
    assert getter().foo == {"key": "1"}
    assert getter().bar == {"key": "1"}
    assert getter().baz == {"key": 1}

    getter = make_collector()
    T().x.run(foo=value, bar=value, baz=value)
    assert getter().foo is getter().bar
    assert getter().foo == {"key": "1"}
    assert getter().bar == {"key": "1"}
    assert getter().baz == {"key": 1}

    # FIXME: Substory inheritance.

    # FIXME: Substory DI.


# Representation.


def test_story_contract_representation_with_spec(m):
    """
    Show collected story composition contract as mounted story
    attribute.
    """

    class T(m.Child, m.StringMethod):
        pass

    class Q(m.Parent, m.NormalParentMethod, T):
        pass

    class J(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    class R(m.Root, m.NormalRootMethod, Q):
        pass

    class F(m.Root, m.NormalRootMethod):
        def __init__(self):
            self.a = J().a

    # Simple.

    expected = """
Contract:
  foo: ...  # T.x variable
  bar: ...  # T.x variable
  baz: ...  # T.x variable
    """.strip()

    assert repr(T().x.contract) == expected

    # Substory inheritance.

    expected = """
Contract:
  ham: ...   # Q.a variable
  eggs: ...  # Q.a variable
  beans: ... # Q.a variable
  foo: ...   # Q.x variable
  bar: ...   # Q.x variable
  baz: ...   # Q.x variable
    """.strip()

    assert repr(Q().a.contract) == expected

    expected = """
Contract:
  fizz: ...  # R.i variable
  buzz: ...  # R.i variable
  ham: ...   # R.a variable
  eggs: ...  # R.a variable
  beans: ... # R.a variable
  foo: ...   # R.x variable
  bar: ...   # R.x variable
  baz: ...   # R.x variable
    """.strip()

    assert repr(R().i.contract) == expected

    # Substory DI.

    expected = """
Contract:
  ham: ...   # J.a variable
  eggs: ...  # J.a variable
  beans: ... # J.a variable
  foo: ...   # T.x variable
  bar: ...   # T.x variable
  baz: ...   # T.x variable
    """.strip()

    assert repr(J().a.contract) == expected

    expected = """
Contract:
  fizz: ...  # F.i variable
  buzz: ...  # F.i variable
  ham: ...   # J.a variable
  eggs: ...  # J.a variable
  beans: ... # J.a variable
  foo: ...   # T.x variable
  bar: ...   # T.x variable
  baz: ...   # T.x variable
    """.strip()

    assert repr(F().i.contract) == expected


def test_story_contract_representation_with_spec_with_args(m):
    """
    Show collected story composition contract as mounted story
    attribute.  We show each story arguments.
    """

    class T(m.ParamChild, m.StringMethod):
        pass

    class Q(m.ParamParent, m.NormalParentMethod, T):
        pass

    class J(m.ParamParent, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    class R(m.ParamRoot, m.NormalRootMethod, Q):
        pass

    class F(m.ParamRoot, m.NormalRootMethod):
        def __init__(self):
            self.a = J().a

    # Simple.

    expected = """
Contract:
  foo: ...  # T.x argument
  bar: ...  # T.x argument
  baz: ...  # T.x variable
    """.strip()

    assert repr(T().x.contract) == expected

    # Substory inheritance.

    expected = """
Contract:
  ham: ...   # Q.a argument
  eggs: ...  # Q.a argument
  foo: ...   # Q.x argument
  bar: ...   # Q.x argument
  beans: ... # Q.a variable
  baz: ...   # Q.x variable
    """.strip()

    assert repr(Q().a.contract) == expected

    expected = """
Contract:
  fizz: ...  # R.i argument
  ham: ...   # R.a argument
  eggs: ...  # R.a argument
  foo: ...   # R.x argument
  bar: ...   # R.x argument
  buzz: ...  # R.i variable
  beans: ... # R.a variable
  baz: ...   # R.x variable
    """.strip()

    assert repr(R().i.contract) == expected

    # Substory DI.

    expected = """
Contract:
  ham: ...   # J.a argument
  eggs: ...  # J.a argument
  foo: ...   # T.x argument
  bar: ...   # T.x argument
  beans: ... # J.a variable
  baz: ...   # T.x variable
    """.strip()

    assert repr(J().a.contract) == expected

    expected = """
Contract:
  fizz: ...  # F.i argument
  ham: ...   # J.a argument
  eggs: ...  # J.a argument
  foo: ...   # T.x argument
  bar: ...   # T.x argument
  buzz: ...  # F.i variable
  beans: ... # J.a variable
  baz: ...   # T.x variable
    """.strip()

    assert repr(F().i.contract) == expected


def test_story_contract_representation_with_spec_with_args_conflict(m):
    """
    Show collected story composition contract as mounted story
    attribute.  We show each story arguments in multiline mode if the
    same name was declared in multiple substories.
    """

    class T(m.ParamChild, m.NormalMethod):
        pass

    class Q(m.ParamParentWithSameWithString, m.NormalParentMethod, T):
        pass

    class J(m.ParamParentWithSameWithString, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # FIXME: Implement this.
    #
    # class R(..., m.NormalRootMethod, Q):
    #     pass
    #
    # class F(..., m.NormalRootMethod):
    #     def __init__(self):
    #         self.a = J().a

    # Substory inheritance.

    expected = """
Contract:
  foo:
    ...     # Q.a argument
    ...     # Q.x argument
  bar:
    ...     # Q.a argument
    ...     # Q.x argument
  baz: ...  # Q.x variable
    """.strip()

    assert repr(Q().a.contract) == expected

    #     expected = """
    # Contract:
    #   fizz: ...  # R.i argument
    #   ham: ...   # R.a argument
    #   eggs: ...  # R.a argument
    #   foo: ...   # R.x argument
    #   bar: ...   # R.x argument
    #   buzz: ...  # R.i variable
    #   beans: ... # R.a variable
    #   baz: ...   # R.x variable
    #     """.strip()
    #
    #     assert repr(R().i.contract) == expected

    # Substory DI.

    expected = """
Contract:
  foo:
    ...     # J.a argument
    ...     # T.x argument
  bar:
    ...     # J.a argument
    ...     # T.x argument
  baz: ...  # T.x variable
    """.strip()

    assert repr(J().a.contract) == expected

    #     expected = """
    # Contract:
    #   fizz: ...  # F.i argument
    #   ham: ...   # J.a argument
    #   eggs: ...  # J.a argument
    #   foo: ...   # T.x argument
    #   bar: ...   # T.x argument
    #   buzz: ...  # F.i variable
    #   beans: ... # J.a variable
    #   baz: ...   # T.x variable
    #     """.strip()
    #
    #     assert repr(F().i.contract) == expected
