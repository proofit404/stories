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

T.x
  one

Context:
  foo: 1    # Story argument
  bar: [2]  # Story argument
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

Q.a
  before
  x
    one

Context:
  bar: ['2']  # Set by Q.before
  foo: '1'    # Set by Q.before
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

J.a
  before
  x (T.x)
    one

Context:
  bar: ['2']  # Set by J.before
  foo: '1'    # Set by J.before
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

Q.x:
 - bar: [2]
 - foo: 1

Q.y:
 - bar: ['2']
 - foo: '1'

Contract:
  bar:
    {list_of_int_field_repr}  # Argument of Q.x
    {list_of_str_field_repr}  # Argument of Q.y
  foo:
    {int_field_repr}  # Argument of Q.x
    {str_field_repr}  # Argument of Q.y
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These arguments have normalization conflict: 'bar', 'foo'

E.y:
 - bar: ['2']
 - foo: '1'

T.x:
 - bar: [2]
 - foo: 1

Contract:
  bar:
    {list_of_str_field_repr}  # Argument of E.y
    {list_of_int_field_repr}  # Argument of T.x
  foo:
    {str_field_repr}  # Argument of E.y
    {int_field_repr}  # Argument of T.x
    """.strip().format(
        **m.representations
    )

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

Q.a:
 - bar: ['2']
 - foo: '1'

Q.x:
 - bar: [2]
 - foo: 1

Contract:
  bar:
    {list_of_str_field_repr}  # Argument of Q.a
    {list_of_int_field_repr}  # Argument of Q.x
  foo:
    {str_field_repr}  # Argument of Q.a
    {int_field_repr}  # Argument of Q.x
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        Q().a(foo="1", bar=["2"])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run(foo="1", bar=["2"])
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These arguments have normalization conflict: 'bar', 'foo'

J.a:
 - bar: ['2']
 - foo: '1'

T.x:
 - bar: [2]
 - foo: 1

Contract:
  bar:
    {list_of_str_field_repr}  # Argument of J.a
    {list_of_int_field_repr}  # Argument of T.x
  foo:
    {str_field_repr}  # Argument of J.a
    {int_field_repr}  # Argument of T.x
    """.strip().format(
        **m.representations
    )

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

    expected = (
        """
These variables violates context contract: 'bar', 'foo'

Function returned value: T.one

Violations:

bar:
  ['<boom>']
  {list_of_int_error}

foo:
  '<boom>'
  {int_error}

Contract:
  bar: {list_of_int_field_repr}  # Variable in T.x
  foo: {int_field_repr}  # Variable in T.x
    """.strip()
        .format(**m.representations)
        .format("foo")
    )

    with pytest.raises(ContextContractError) as exc_info:
        T().x()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        T().x.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = (
        """
These variables violates context contract: 'bar', 'foo'

Function returned value: Q.one

Violations:

bar:
  ['<boom>']
  {list_of_int_error}

foo:
  '<boom>'
  {int_error}

Contract:
  bar: {list_of_int_field_repr}  # Variable in Q.x
  foo: {int_field_repr}  # Variable in Q.x
    """.strip()
        .format(**m.representations)
        .format("foo")
    )

    with pytest.raises(ContextContractError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = (
        """
These variables violates context contract: 'bar', 'foo'

Function returned value: T.one

Violations:

bar:
  ['<boom>']
  {list_of_int_error}

foo:
  '<boom>'
  {int_error}

Contract:
  bar: {list_of_int_field_repr}  # Variable in T.x
  foo: {int_field_repr}  # Variable in T.x
    """.strip()
        .format(**m.representations)
        .format("foo")
    )

    with pytest.raises(ContextContractError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


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

    expected = (
        """
These arguments violates context contract: 'bar', 'foo'

Story method: T.x

Violations:

bar:
  ['<boom>']
  {list_of_int_error}

foo:
  '<boom>'
  {int_error}

Contract:
  bar: {list_of_int_field_repr}  # Argument of T.x
  foo: {int_field_repr}  # Argument of T.x
    """.strip()
        .format(**m.representations)
        .format("foo")
    )

    with pytest.raises(ContextContractError) as exc_info:
        T().x(foo="<boom>", bar=["<boom>"])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        T().x.run(foo="<boom>", bar=["<boom>"])
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = (
        """
These arguments violates context contract: 'eggs', 'ham'

Story method: Q.a

Violations:

eggs:
  '<boom>'
  {int_error}

ham:
  '<boom>'
  {int_error}

Contract:
  eggs: {int_field_repr}  # Argument of Q.a
  ham: {int_field_repr}  # Argument of Q.a
    """.strip()
        .format(**m.representations)
        .format("eggs", "ham")
    )

    with pytest.raises(ContextContractError) as exc_info:
        Q().a(ham="<boom>", eggs="<boom>")
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run(ham="<boom>", eggs="<boom>")
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = (
        """
These arguments violates context contract: 'eggs', 'ham'

Story method: J.a

Violations:

eggs:
  '<boom>'
  {int_error}

ham:
  '<boom>'
  {int_error}

Contract:
  eggs: {int_field_repr}  # Argument of J.a
  ham: {int_field_repr}  # Argument of J.a
    """.strip()
        .format(**m.representations)
        .format("eggs", "ham")
    )

    with pytest.raises(ContextContractError) as exc_info:
        J().a(ham="<boom>", eggs="<boom>")
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run(ham="<boom>", eggs="<boom>")
    assert str(exc_info.value) == expected


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

    expected = (
        """
These arguments violates context contract: 'foo'

Story method: R.i

Violations:

foo:
  '<boom>'
  {int_error}

Contract:
  foo: {int_field_repr}  # Argument of R.x
    """.strip()
        .format(**m.representations)
        .format("foo")
    )

    with pytest.raises(ContextContractError) as exc_info:
        R().i(foo="<boom>", bar=[1])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        R().i.run(foo="<boom>", bar=[1])
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = (
        """
These arguments violates context contract: 'foo'

Story method: F.i

Violations:

foo:
  '<boom>'
  {int_error}

Contract:
  foo: {int_field_repr}  # Argument of T.x
    """.strip()
        .format(**m.representations)
        .format("foo")
    )

    with pytest.raises(ContextContractError) as exc_info:
        F().i(foo="<boom>", bar=[1])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        F().i.run(foo="<boom>", bar=[1])
    assert str(exc_info.value) == expected


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

Substory context contract: {contract_class_repr}
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        Q().a
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Story and substory context contracts has incompatible types:

Story method: J.a

Story context contract: None

Substory method: T.x

Substory context contract: {contract_class_repr}
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        J().a
    assert str(exc_info.value) == expected


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

Function returned value: T.one

Use different names for Success() keyword arguments or add these names to the contract.

Contract:
  bar: {list_of_int_field_repr}  # Variable in T.x
  baz: {int_field_repr}  # Variable in T.x
  foo: {int_field_repr}  # Variable in T.x
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        T().x()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        T().x.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
These variables were not defined in the context contract: 'quiz', 'spam'

Function returned value: Q.one

Use different names for Success() keyword arguments or add these names to the contract.

Contract:
  bar: {list_of_int_field_repr}  # Variable in Q.x
  baz: {int_field_repr}  # Variable in Q.x
  foo: {int_field_repr}  # Variable in Q.x
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
These variables were not defined in the context contract: 'quiz', 'spam'

Function returned value: T.one

Use different names for Success() keyword arguments or add these names to the contract.

Contract:
  bar: {list_of_int_field_repr}  # Variable in T.x
  baz: {int_field_repr}  # Variable in T.x
  foo: {int_field_repr}  # Variable in T.x
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_unknown_story_arguments_with_null(m):
    """
    Allow to pass known only story and substory arguments to the call.
    """

    class T(m.ParamChildWithNull, m.NormalMethod):
        pass

    class Q(
        m.ParamParentWithNull, m.NormalParentMethod, m.ChildWithNull, m.NormalMethod
    ):
        pass

    class J(m.ParamParentWithNull, m.NormalParentMethod):
        def __init__(self):
            class T(m.ChildWithNull, m.NormalMethod):
                pass

            self.x = T().x

    # Simple.

    expected = """
These arguments are unknown: baz, fox

Story method: T.x

Contract:
  bar  # Argument of T.x
  foo  # Argument of T.x
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

Contract:
  eggs  # Argument of Q.a
  ham  # Argument of Q.a
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

Contract:
  eggs  # Argument of J.a
  ham  # Argument of J.a
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a(beans=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run(beans=1, fox=2)
    assert str(exc_info.value) == expected


def test_unknown_story_arguments(m):
    """
    Allow to pass known only story and substory arguments to the call.
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
These arguments are unknown: baz, fox

Story method: T.x

Contract:
  bar: {list_of_int_field_repr}  # Argument of T.x
  foo: {int_field_repr}  # Argument of T.x
  baz: {int_field_repr}  # Variable in T.x
    """.strip().format(
        **m.representations
    )

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

Contract:
  eggs: {int_field_repr}  # Argument of Q.a
  ham: {int_field_repr}  # Argument of Q.a
  bar: {list_of_int_field_repr}  # Variable in Q.x
  baz: {int_field_repr}  # Variable in Q.x
  beans: {int_field_repr}  # Variable in Q.a
  foo: {int_field_repr}  # Variable in Q.x
    """.strip().format(
        **m.representations
    )

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

Contract:
  eggs: {int_field_repr}  # Argument of J.a
  ham: {int_field_repr}  # Argument of J.a
  bar: {list_of_int_field_repr}  # Variable in T.x
  baz: {int_field_repr}  # Variable in T.x
  beans: {int_field_repr}  # Variable in J.a
  foo: {int_field_repr}  # Variable in T.x
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        J().a(beans=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run(beans=1, fox=2)
    assert str(exc_info.value) == expected


def test_unknown_story_arguments_with_empty_with_null(m):
    """
    Deny any arguments in the call, if story and substory has no
    arguments specified.
    """

    class T(m.ChildWithNull, m.NormalMethod):
        pass

    class Q(m.ParentWithNull, m.NormalParentMethod, T):
        pass

    class J(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
These arguments are unknown: baz, fox

Story method: T.x

Contract()
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

Contract()
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

Contract()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        J().a(beans=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        J().a.run(beans=1, fox=2)
    assert str(exc_info.value) == expected


def test_unknown_story_arguments_with_empty(m):
    """
    Deny any arguments in the call, if story and substory has no
    arguments specified.
    """

    class T(m.Child, m.NormalMethod):
        pass

    class Q(m.Parent, m.NormalParentMethod, T):
        pass

    class J(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
These arguments are unknown: baz, fox

Story method: T.x

Contract:
  bar: {list_of_int_field_repr}  # Variable in T.x
  baz: {int_field_repr}  # Variable in T.x
  foo: {int_field_repr}  # Variable in T.x
    """.strip().format(
        **m.representations
    )

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

Contract:
  bar: {list_of_int_field_repr}  # Variable in Q.x
  baz: {int_field_repr}  # Variable in Q.x
  beans: {int_field_repr}  # Variable in Q.a
  eggs: {int_field_repr}  # Variable in Q.a
  foo: {int_field_repr}  # Variable in Q.x
  ham: {int_field_repr}  # Variable in Q.a
    """.strip().format(
        **m.representations
    )

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

Contract:
  bar: {list_of_int_field_repr}  # Variable in T.x
  baz: {int_field_repr}  # Variable in T.x
  beans: {int_field_repr}  # Variable in J.a
  eggs: {int_field_repr}  # Variable in J.a
  foo: {int_field_repr}  # Variable in T.x
  ham: {int_field_repr}  # Variable in J.a
    """.strip().format(
        **m.representations
    )

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
  bar: {list_of_int_field_repr}  # Variable in T.x
  baz: {int_field_repr}  # Variable in T.x
  foo: {int_field_repr}  # Variable in T.x
    """.strip().format(
        **m.representations
    )

    assert repr(T().x.contract) == expected

    # Substory inheritance.

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Variable in Q.x
  baz: {int_field_repr}  # Variable in Q.x
  beans: {int_field_repr}  # Variable in Q.a
  eggs: {int_field_repr}  # Variable in Q.a
  foo: {int_field_repr}  # Variable in Q.x
  ham: {int_field_repr}  # Variable in Q.a
    """.strip().format(
        **m.representations
    )

    assert repr(Q().a.contract) == expected

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Variable in R.x
  baz: {int_field_repr}  # Variable in R.x
  beans: {int_field_repr}  # Variable in R.a
  buzz: {int_field_repr}  # Variable in R.i
  eggs: {int_field_repr}  # Variable in R.a
  fizz: {int_field_repr}  # Variable in R.i
  foo: {int_field_repr}  # Variable in R.x
  ham: {int_field_repr}  # Variable in R.a
    """.strip().format(
        **m.representations
    )

    assert repr(R().i.contract) == expected

    # Substory DI.

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Variable in T.x
  baz: {int_field_repr}  # Variable in T.x
  beans: {int_field_repr}  # Variable in J.a
  eggs: {int_field_repr}  # Variable in J.a
  foo: {int_field_repr}  # Variable in T.x
  ham: {int_field_repr}  # Variable in J.a
    """.strip().format(
        **m.representations
    )

    assert repr(J().a.contract) == expected

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Variable in T.x
  baz: {int_field_repr}  # Variable in T.x
  beans: {int_field_repr}  # Variable in J.a
  buzz: {int_field_repr}  # Variable in F.i
  eggs: {int_field_repr}  # Variable in J.a
  fizz: {int_field_repr}  # Variable in F.i
  foo: {int_field_repr}  # Variable in T.x
  ham: {int_field_repr}  # Variable in J.a
    """.strip().format(
        **m.representations
    )

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
  bar: {list_of_int_field_repr}  # Argument of T.x
  foo: {int_field_repr}  # Argument of T.x
  baz: {int_field_repr}  # Variable in T.x
    """.strip().format(
        **m.representations
    )

    assert repr(T().x.contract) == expected

    # Substory inheritance.

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Argument of Q.x
  eggs: {int_field_repr}  # Argument of Q.a
  foo: {int_field_repr}  # Argument of Q.x
  ham: {int_field_repr}  # Argument of Q.a
  baz: {int_field_repr}  # Variable in Q.x
  beans: {int_field_repr}  # Variable in Q.a
    """.strip().format(
        **m.representations
    )

    assert repr(Q().a.contract) == expected

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Argument of R.x
  eggs: {int_field_repr}  # Argument of R.a
  fizz: {int_field_repr}  # Argument of R.i
  foo: {int_field_repr}  # Argument of R.x
  ham: {int_field_repr}  # Argument of R.a
  baz: {int_field_repr}  # Variable in R.x
  beans: {int_field_repr}  # Variable in R.a
  buzz: {int_field_repr}  # Variable in R.i
    """.strip().format(
        **m.representations
    )

    assert repr(R().i.contract) == expected

    # Substory DI.

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Argument of T.x
  eggs: {int_field_repr}  # Argument of J.a
  foo: {int_field_repr}  # Argument of T.x
  ham: {int_field_repr}  # Argument of J.a
  baz: {int_field_repr}  # Variable in T.x
  beans: {int_field_repr}  # Variable in J.a
    """.strip().format(
        **m.representations
    )

    assert repr(J().a.contract) == expected

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Argument of T.x
  eggs: {int_field_repr}  # Argument of J.a
  fizz: {int_field_repr}  # Argument of F.i
  foo: {int_field_repr}  # Argument of T.x
  ham: {int_field_repr}  # Argument of J.a
  baz: {int_field_repr}  # Variable in T.x
  beans: {int_field_repr}  # Variable in J.a
  buzz: {int_field_repr}  # Variable in F.i
    """.strip().format(
        **m.representations
    )

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
  bar:
    {list_of_str_field_repr}  # Argument of Q.a
    {list_of_int_field_repr}  # Argument of Q.x
  foo:
    {str_field_repr}  # Argument of Q.a
    {int_field_repr}  # Argument of Q.x
  baz: {int_field_repr}  # Variable in Q.x
    """.strip().format(
        **m.representations
    )

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
  bar:
    {list_of_str_field_repr}  # Argument of J.a
    {list_of_int_field_repr}  # Argument of T.x
  foo:
    {str_field_repr}  # Argument of J.a
    {int_field_repr}  # Argument of T.x
  baz: {int_field_repr}  # Variable in T.x
    """.strip().format(
        **m.representations
    )

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
