import pytest

from helpers import make_collector
from stories.exceptions import ContextContractError


# TODO: Show collected arguments of the story composition in the error
# messages.
#
# TODO: Show violation values in validation error messages.
#
# TODO: Write correct and verbose docstrings for each test in this
# module.
#
# TODO: Document test class names in the contribution guide.


def test_assign_existed_variables(r, m):
    """We can not write a variable with the same name to the context twice."""

    class A(m.ParamChildWithNull, m.StringMethod):
        pass

    class B(m.ParentWithNull, m.StringParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
This variable is already present in the context: 'foo'

Function returned value: A.one

Use a different name for context attribute.

A.x
  one

Context:
  bar: [2]  # Story argument
  foo: 1    # Story argument
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x)(foo=1, bar=[2])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x.run)(foo=1, bar=[2])
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
This variable is already present in the context: 'foo'

Function returned value: A.one

Use a different name for context attribute.

B.a
  before
  x (A.x)
    one

Context:
  foo: '1'    # Set by B.before
  bar: ['2']  # Set by B.before
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a.run)()
    assert str(exc_info.value) == expected


def test_context_variables_normalization(r, m):
    """We apply normalization to the context variables, if story defines context
    contract.

    If story step returns a string holding a number, we should store a number in the
    context.

    """

    class A(m.Child, m.StringMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    getter = make_collector()
    r(A().x)()
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    r(A().x.run)()
    assert getter().foo == 1
    assert getter().bar == [2]

    # Second level.

    getter = make_collector()
    r(B().a)()
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    r(B().a.run)()
    assert getter().foo == 1
    assert getter().bar == [2]


def test_context_variables_normalization_conflict(r, m):
    """More than one substory can declare an argument with the same name.

    This means validators of both substories should return the same result.

    """

    # FIXME: Normalization conflict can consist of two
    # variables.  The first variable can be set by one
    # substory.  The second variable can be set by
    # another substory.

    class A1(m.ParamChild, m.NormalMethod):
        pass

    class A2(m.NextParamChildWithString, m.NormalNextMethod):
        pass

    class B(m.SequentialParent, m.StringParentMethod):
        def __init__(self):
            self.x = A1().x
            self.y = A2().y

    # Second level.

    expected = """
These arguments have normalization conflict: 'foo'

A1.x:
 - foo: 1

A2.y:
 - foo: '1'

Contract:
  foo:
    {int_field_repr}  # Argument of A1.x
    {str_field_repr}  # Argument of A2.y
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a.run)()
    assert str(exc_info.value) == expected


def test_story_arguments_normalization(r, m):
    """We apply normalization to the story arguments, if story defines context contract.

    If story was called with a string argument holding a number, we should store a
    number in the context.

    """

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.ParamParent, m.StringParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    getter = make_collector()
    r(A().x)(foo="1", bar=["2"])
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    r(A().x.run)(foo="1", bar=["2"])
    assert getter().foo == 1
    assert getter().bar == [2]

    # Second level.

    getter = make_collector()
    r(B().a)(ham="1", eggs="2")
    assert getter().ham == 1
    assert getter().eggs == 2

    getter = make_collector()
    r(B().a.run)(ham="1", eggs="2")
    assert getter().ham == 1
    assert getter().eggs == 2


def test_story_arguments_normalization_many_levels(r, m):
    """We apply normalization to the story arguments on any levels of story
    composition."""

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.ParamParent, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    class C(m.ParamRoot, m.NormalRootMethod):
        def __init__(self):
            self.a = B().a

    # Second level.

    getter = make_collector()
    r(B().a)(ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]

    getter = make_collector()
    r(B().a.run)(ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]

    getter = make_collector()
    r(C().i)(fizz="0", ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().fizz == 0
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]

    getter = make_collector()
    r(C().i.run)(fizz="0", ham="1", eggs="2", foo="3", bar=["4"])
    assert getter().fizz == 0
    assert getter().ham == 1
    assert getter().eggs == 2
    assert getter().foo == 3
    assert getter().bar == [4]


def test_story_arguments_normalization_conflict(r, m):
    """Story and substory can have an argument with the same name.

    They both will define validators for this argument.  If normalization result of both
    contracts will mismatch we should raise an error.

    """

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.ParamParentWithSameWithString, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # Second level.

    expected = """
These arguments have normalization conflict: 'bar', 'foo'

A.x:
 - bar: [2]
 - foo: 1

B.a:
 - bar: ['2']
 - foo: '1'

Contract:
  bar:
    {list_of_int_field_repr}  # Argument of A.x
    {list_of_str_field_repr}  # Argument of B.a
  foo:
    {int_field_repr}  # Argument of A.x
    {str_field_repr}  # Argument of B.a
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a)(foo="1", bar=["2"])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a.run)(foo="1", bar=["2"])
    assert str(exc_info.value) == expected


def test_context_variables_validation(r, m):
    """We apply validators to the context variables, if story defines context
    contract."""

    class A(m.Child, m.WrongMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = (
        """
This variable violates context contract: 'foo'

Function returned value: A.one

Violations:

foo:
  '<boom>'
  {int_error}

Contract:
  foo: {int_field_repr}  # Variable in A.x
    """.strip()
        .format(**m.representations)
        .format("foo")
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x.run)()
    assert str(exc_info.value) == expected

    # Second level.

    expected = (
        """
This variable violates context contract: 'foo'

Function returned value: A.one

Violations:

foo:
  '<boom>'
  {int_error}

Contract:
  foo: {int_field_repr}  # Variable in A.x
    """.strip()
        .format(**m.representations)
        .format("foo")
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a.run)()
    assert str(exc_info.value) == expected


def test_story_arguments_validation(r, m):
    """We apply validators to the story arguments, if story defines context contract.

    This is check performed during story call, not execution.

    """

    class A(m.ParamChild, m.ExceptionMethod):
        pass

    class B(m.ParamParent, m.ExceptionParentMethod):
        def __init__(self):
            class A(m.Child, m.NormalMethod):
                pass

            self.x = A().x

    # First level.

    expected = (
        """
These arguments violates context contract: 'bar', 'foo'

Story method: A.x

Violations:

bar:
  ['<boom>']
  {list_of_int_error}

foo:
  '<boom>'
  {int_error}

Contract:
  bar: {list_of_int_field_repr}  # Argument of A.x
  foo: {int_field_repr}  # Argument of A.x
    """.strip()
        .format(**m.representations)
        .format("foo")
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x)(foo="<boom>", bar=["<boom>"])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x.run)(foo="<boom>", bar=["<boom>"])
    assert str(exc_info.value) == expected

    # Second level.

    expected = (
        """
These arguments violates context contract: 'eggs', 'ham'

Story method: B.a

Violations:

eggs:
  '<boom>'
  {int_error}

ham:
  '<boom>'
  {int_error}

Contract:
  eggs: {int_field_repr}  # Argument of B.a
  ham: {int_field_repr}  # Argument of B.a
    """.strip()
        .format(**m.representations)
        .format("eggs", "ham")
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a)(ham="<boom>", eggs="<boom>")
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a.run)(ham="<boom>", eggs="<boom>")
    assert str(exc_info.value) == expected


def test_story_arguments_validation_many_levels(r, m):
    """We apply contract validation to the story arguments on any levels of story
    composition."""

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    class C(m.Root, m.ExceptionRootMethod):
        def __init__(self):
            self.a = B().a

    # Second level.

    expected = (
        """
These arguments violates context contract: 'foo'

Story method: C.i

Violations:

foo:
  '<boom>'
  {int_error}

Contract:
  foo: {int_field_repr}  # Argument of A.x
    """.strip()
        .format(**m.representations)
        .format("foo")
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(C().i)(foo="<boom>", bar=[1])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(C().i.run)(foo="<boom>", bar=[1])
    assert str(exc_info.value) == expected


def test_composition_contract_variable_conflict(r, m):
    """Story and substory contracts can not declare the same variable twice."""

    class A(m.Child, m.NormalMethod):
        pass

    class B(m.ParentWithSame, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # Second level.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'bar', 'baz', 'foo'

Story method: B.a

Substory method: A.x

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        B().a
    assert str(exc_info.value) == expected


def test_composition_contract_variable_conflict_many_levels(r, m):
    """Story and substory contracts can not declare the same variable twice."""

    class A(m.Child, m.NormalMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    class C(m.RootWithSame, m.NormalRootMethod):
        def __init__(self):
            self.a = B().a

    # Second level.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'bar', 'baz', 'foo'

Story method: C.i

Substory method: A.x

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        C().i
    assert str(exc_info.value) == expected


def test_composition_contract_variable_conflict_sequential(r, m):
    """Story and substory contracts can not declare the same variable twice."""

    class A(m.Child, m.NormalMethod):
        pass

    class A2(m.NextChildWithSame, m.NormalMethod):
        pass

    class B(m.SequentialParent, m.StringParentMethod):
        def __init__(self):
            self.x = A().x
            self.y = A2().y

    # Second level.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'bar', 'baz', 'foo'

Story method: A.x

Substory method: A2.y

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        B().a
    assert str(exc_info.value) == expected


def test_composition_incompatible_contract_types(r, m):
    """Deny to use different types in the story composition."""

    class A(m.Child, m.NormalMethod):
        pass

    class B(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # Second level.

    expected = """
Story and substory context contracts has incompatible types:

Story method: B.a

Story context contract: None

Substory method: A.x

Substory context contract: {contract_class_repr}
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        B().a
    assert str(exc_info.value) == expected


def test_unknown_context_variable(r, m):
    """Step can't use Success argument name which was not specified in the contract."""

    class A(m.Child, m.UnknownMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
This variable was not defined in the context contract: 'spam'

Function assigned value: A.one

Use a different name for context attribute or add this name to the contract.

Contract:
  bar: {list_of_int_field_repr}  # Variable in A.x
  baz: {int_field_repr}  # Variable in A.x
  foo: {int_field_repr}  # Variable in A.x
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x.run)()
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
This variable was not defined in the context contract: 'spam'

Function assigned value: A.one

Use a different name for context attribute or add this name to the contract.

Contract:
  bar: {list_of_int_field_repr}  # Variable in A.x
  baz: {int_field_repr}  # Variable in A.x
  foo: {int_field_repr}  # Variable in A.x
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a.run)()
    assert str(exc_info.value) == expected


def test_unknown_story_arguments_with_null(r, m):
    """Allow to pass known only story and substory arguments to the call."""

    class A(m.ParamChildWithNull, m.NormalMethod):
        pass

    class B(m.ParamParentWithNull, m.NormalParentMethod):
        def __init__(self):
            class A(m.ChildWithNull, m.NormalMethod):
                pass

            self.x = A().x

    # First level.

    expected = """
These arguments are unknown: baz, fox

Story method: A.x

Contract:
  bar  # Argument of A.x
  foo  # Argument of A.x
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x)(baz=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x.run)(baz=1, fox=2)
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These arguments are unknown: beans, fox

Story method: B.a

Contract:
  eggs  # Argument of B.a
  ham  # Argument of B.a
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a)(beans=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a.run)(beans=1, fox=2)
    assert str(exc_info.value) == expected


def test_unknown_story_arguments(r, m):
    """Allow to pass known only story and substory arguments to the call."""

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.ParamParent, m.NormalParentMethod):
        def __init__(self):
            class A(m.Child, m.NormalMethod):
                pass

            self.x = A().x

    # First level.

    expected = """
These arguments are unknown: baz, fox

Story method: A.x

Contract:
  bar: {list_of_int_field_repr}  # Argument of A.x
  foo: {int_field_repr}  # Argument of A.x
  baz: {int_field_repr}  # Variable in A.x
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x)(baz=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x.run)(baz=1, fox=2)
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These arguments are unknown: beans, fox

Story method: B.a

Contract:
  eggs: {int_field_repr}  # Argument of B.a
  ham: {int_field_repr}  # Argument of B.a
  bar: {list_of_int_field_repr}  # Variable in A.x
  baz: {int_field_repr}  # Variable in A.x
  beans: {int_field_repr}  # Variable in B.a
  foo: {int_field_repr}  # Variable in A.x
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a)(beans=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a.run)(beans=1, fox=2)
    assert str(exc_info.value) == expected


def test_unknown_story_arguments_with_empty_with_null(r, m):
    """Deny any arguments in the call, if story and substory has no arguments
    specified."""

    class A(m.ChildWithNull, m.NormalMethod):
        pass

    class B(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
These arguments are unknown: baz, fox

Story method: A.x

Contract()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x)(baz=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x.run)(baz=1, fox=2)
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These arguments are unknown: beans, fox

Story method: B.a

Contract()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a)(beans=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a.run)(beans=1, fox=2)
    assert str(exc_info.value) == expected


def test_unknown_story_arguments_with_empty(r, m):
    """Deny any arguments in the call, if story and substory has no arguments
    specified."""

    class A(m.Child, m.NormalMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
These arguments are unknown: baz, fox

Story method: A.x

Contract:
  bar: {list_of_int_field_repr}  # Variable in A.x
  baz: {int_field_repr}  # Variable in A.x
  foo: {int_field_repr}  # Variable in A.x
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x)(baz=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x.run)(baz=1, fox=2)
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These arguments are unknown: beans, fox

Story method: B.a

Contract:
  bar: {list_of_int_field_repr}  # Variable in A.x
  baz: {int_field_repr}  # Variable in A.x
  beans: {int_field_repr}  # Variable in B.a
  eggs: {int_field_repr}  # Variable in B.a
  foo: {int_field_repr}  # Variable in A.x
  ham: {int_field_repr}  # Variable in B.a
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a)(beans=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a.run)(beans=1, fox=2)
    assert str(exc_info.value) == expected


def test_require_story_arguments_present_in_context(r, m):
    """Check story and substory arguments are present in the context."""

    class A(m.ParamChildWithNull, m.NormalMethod):
        pass

    class B(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
These variables are missing from the context: bar, foo

Story method: A.x

Story arguments: foo, bar

A.x

Context()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x)()  # FIXME: This should be arguments error (not substory call error).
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().x.run)()
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These variables are missing from the context: bar, foo

Story method: A.x

Story arguments: foo, bar

B.a
  before
  x (A.x)

Context()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().a.run)()
    assert str(exc_info.value) == expected


def test_parent_steps_set_story_arguments(r, m):
    """Steps of parent stories should be able to set child stories arguments with
    `Success` marker keyword arguments."""

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.Parent, m.StringParentMethod):
        def __init__(self):
            self.x = A().x

    class C(m.Root, m.StringRootMethod):
        def __init__(self):
            class B(m.Parent, m.NormalParentMethod):
                def __init__(self):
                    self.x = A().x
            self.a = B().a

    # Second level.

    getter = make_collector()
    r(B().a)()
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    r(B().a.run)()
    assert getter().foo == 1
    assert getter().bar == [2]

    # Third level.
    
    getter = make_collector()
    r(C().i)()
    assert getter().foo == 1
    assert getter().bar == [2]

    getter = make_collector()
    r(C().i.run)()
    assert getter().foo == 1
    assert getter().bar == [2]


def test_sequential_story_steps_set_story_arguments(r, m):
    """There are a few sequential substories with one common parent story.

    One substory should be able to set variable to provide an argument to the next
    sequential story.

    """

    class A1(m.ChildWithShrink, m.StringMethod):
        pass

    class A2(m.NextParamChildWithString, m.NormalNextMethod):
        pass

    class B(m.SequentialParent, m.NormalParentMethod):
        def __init__(self):
            self.x = A1().x
            self.y = A2().y

    # Second level.

    getter = make_collector()
    r(B().a)()
    assert getter().foo == "1"
    assert getter().bar == ["2"]

    getter = make_collector()
    r(B().a.run)()
    assert getter().foo == "1"
    assert getter().bar == ["2"]


def test_arguments_should_be_declared_in_contract(r, m):
    """We should require all story arguments to be declared in the context contract."""

    class A(m.ParamChildWithShrink, m.NormalMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
These arguments should be declared in the context contract: bar, foo

Story method: A.x

Story arguments: foo, bar, baz
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        A().x
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These arguments should be declared in the context contract: bar, foo

Story method: A.x

Story arguments: foo, bar, baz
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        B().a
    assert str(exc_info.value) == expected


# Aliases.


def test_story_variable_alias_normalization_store_same_object(r, m):
    """When story step sets a set of variables some of them are aliases of each other.

    If the type and the value of alias are equal to the origin value, we should preserve
    the same reference to the value.

    """

    class A(m.ChildAlias, m.AliasMethod):
        pass

    # First level.

    getter = make_collector()
    r(A().x)()
    assert getter().foo is getter().bar
    assert getter().foo == {"key": "1"}
    assert getter().bar == {"key": "1"}
    assert getter().foo is not getter().baz
    assert getter().bar is not getter().baz
    assert getter().baz == {"key": 1}

    getter = make_collector()
    r(A().x.run)()
    assert getter().foo is getter().bar
    assert getter().foo == {"key": "1"}
    assert getter().bar == {"key": "1"}
    assert getter().foo is not getter().baz
    assert getter().bar is not getter().baz
    assert getter().baz == {"key": 1}

    # FIXME: Second level.


def test_story_argument_alias_normalization_store_same_object(r, m):
    """When story has a set of arguments some of them are aliases of each other.

    If the type and the value of alias are equal to the origin value, we should preserve
    the same reference to the value.

    """

    class A(m.ParamChildAlias, m.NormalMethod):
        pass

    # First level.

    value = {"key": "1"}

    getter = make_collector()
    r(A().x)(foo=value, bar=value, baz=value)
    assert getter().foo is getter().bar
    assert getter().foo == {"key": "1"}
    assert getter().bar == {"key": "1"}
    assert getter().foo is not getter().baz
    assert getter().bar is not getter().baz
    assert getter().baz == {"key": 1}

    getter = make_collector()
    r(A().x.run)(foo=value, bar=value, baz=value)
    assert getter().foo is getter().bar
    assert getter().foo == {"key": "1"}
    assert getter().bar == {"key": "1"}
    assert getter().foo is not getter().baz
    assert getter().bar is not getter().baz
    assert getter().baz == {"key": 1}

    # FIXME: Second level.


# Representation.


def test_story_contract_representation_with_spec(r, m):
    """Show collected story composition contract as mounted story attribute."""

    class A(m.Child, m.StringMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    class C(m.Root, m.NormalRootMethod):
        def __init__(self):
            self.a = B().a

    # First level.

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Variable in A.x
  baz: {int_field_repr}  # Variable in A.x
  foo: {int_field_repr}  # Variable in A.x
    """.strip().format(
        **m.representations
    )

    assert repr(A().x.contract) == expected

    # Second level.

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Variable in A.x
  baz: {int_field_repr}  # Variable in A.x
  beans: {int_field_repr}  # Variable in B.a
  eggs: {int_field_repr}  # Variable in B.a
  foo: {int_field_repr}  # Variable in A.x
  ham: {int_field_repr}  # Variable in B.a
    """.strip().format(
        **m.representations
    )

    assert repr(B().a.contract) == expected

    # Third level.

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Variable in A.x
  baz: {int_field_repr}  # Variable in A.x
  beans: {int_field_repr}  # Variable in B.a
  buzz: {int_field_repr}  # Variable in C.i
  eggs: {int_field_repr}  # Variable in B.a
  fizz: {int_field_repr}  # Variable in C.i
  foo: {int_field_repr}  # Variable in A.x
  ham: {int_field_repr}  # Variable in B.a
    """.strip().format(
        **m.representations
    )

    assert repr(C().i.contract) == expected


def test_story_contract_representation_with_spec_with_args(r, m):
    """Show collected story composition contract as mounted story attribute.

    We show each story arguments.

    """

    class A(m.ParamChild, m.StringMethod):
        pass

    class B(m.ParamParent, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    class C(m.ParamRoot, m.NormalRootMethod):
        def __init__(self):
            self.a = B().a

    # First level.

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Argument of A.x
  foo: {int_field_repr}  # Argument of A.x
  baz: {int_field_repr}  # Variable in A.x
    """.strip().format(
        **m.representations
    )

    assert repr(A().x.contract) == expected

    # Second level.

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Argument of A.x
  eggs: {int_field_repr}  # Argument of B.a
  foo: {int_field_repr}  # Argument of A.x
  ham: {int_field_repr}  # Argument of B.a
  baz: {int_field_repr}  # Variable in A.x
  beans: {int_field_repr}  # Variable in B.a
    """.strip().format(
        **m.representations
    )

    assert repr(B().a.contract) == expected

    # Third level.

    expected = """
Contract:
  bar: {list_of_int_field_repr}  # Argument of A.x
  eggs: {int_field_repr}  # Argument of B.a
  fizz: {int_field_repr}  # Argument of C.i
  foo: {int_field_repr}  # Argument of A.x
  ham: {int_field_repr}  # Argument of B.a
  baz: {int_field_repr}  # Variable in A.x
  beans: {int_field_repr}  # Variable in B.a
  buzz: {int_field_repr}  # Variable in C.i
    """.strip().format(
        **m.representations
    )

    assert repr(C().i.contract) == expected


def test_story_contract_representation_with_spec_with_args_conflict(r, m):
    """Show collected story composition contract as mounted story attribute.

    We show each story arguments in multiline mode if the same name was declared in
    multiple substories.

    """

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.ParamParentWithSameWithString, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # FIXME: Implement this.
    #
    # class C(..., m.NormalRootMethod):
    #     def __init__(self):
    #         self.a = B().a

    # Second level.

    expected = """
Contract:
  bar:
    {list_of_int_field_repr}  # Argument of A.x
    {list_of_str_field_repr}  # Argument of B.a
  foo:
    {int_field_repr}  # Argument of A.x
    {str_field_repr}  # Argument of B.a
  baz: {int_field_repr}  # Variable in A.x
    """.strip().format(
        **m.representations
    )

    assert repr(B().a.contract) == expected

    #     expected = """
    # Contract:
    #   fizz: ...  # C.i argument
    #   ham: ...   # B.a argument
    #   eggs: ...  # B.a argument
    #   foo: ...   # A.x argument
    #   bar: ...   # A.x argument
    #   buzz: ...  # C.i variable
    #   beans: ... # B.a variable
    #   baz: ...   # A.x variable
    #     """.strip()
    #
    #     assert repr(C().i.contract) == expected
