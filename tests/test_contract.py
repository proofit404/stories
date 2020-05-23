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
    """We can not write b1 variable with the same name to the context twice."""

    class A(m.ParamChildWithNull, m.StringMethod):
        pass

    class B(m.ParentWithNull, m.StringParentMethod):
        def __init__(self):
            self.a1 = A().a1

    # First level.

    expected = """
This variable is already present in the context: 'a1v1'

Function returned value: A.a1s1

Use a different name for context attribute.

A.a1
  a1s1

Context:
  a1v1: 1    # Story argument
  a1v2: [2]  # Story argument
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1)(a1v1=1, a1v2=[2])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1.run)(a1v1=1, a1v2=[2])
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
This variable is already present in the context: 'a1v1'

Function returned value: A.a1s1

Use a different name for context attribute.

B.b1
  b1s1
  a1 (A.a1)
    a1s1

Context:
  a1v1: '1'    # Set by B.b1s1
  a1v2: ['2']  # Set by B.b1s1
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1.run)()
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
            self.a1 = A().a1

    # First level.

    getter = make_collector()
    r(A().a1)()
    assert getter().a1v1 == 1
    assert getter().a1v2 == [2]

    getter = make_collector()
    r(A().a1.run)()
    assert getter().a1v1 == 1
    assert getter().a1v2 == [2]

    # Second level.

    getter = make_collector()
    r(B().b1)()
    assert getter().a1v1 == 1
    assert getter().a1v2 == [2]

    getter = make_collector()
    r(B().b1.run)()
    assert getter().a1v1 == 1
    assert getter().a1v2 == [2]


def test_context_variables_normalization_conflict(r, m):
    """More than a1s1 substory can declare an argument with the same name.

    This means validators of both substories should return the same result.

    """

    # FIXME: Normalization conflict can consist of two
    # variables.  The first variable can be set by a1s1
    # substory.  The second variable can be set by
    # another substory.

    class A1(m.ParamChild, m.NormalMethod):
        pass

    class A2(m.NextParamChildWithString, m.NormalNextMethod):
        pass

    class B(m.SequentialParent, m.StringParentMethod):
        def __init__(self):
            self.a1 = A1().a1
            self.a2 = A2().a2

    # Second level.

    expected = """
These arguments have normalization conflict: 'a1v1'

A1.a1:
 - a1v1: 1

A2.a2:
 - a1v1: '1'

Contract:
  a1v1:
    {int_field_repr}  # Argument of A1.a1
    {str_field_repr}  # Argument of A2.a2
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1.run)()
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
            self.a1 = A().a1

    # First level.

    getter = make_collector()
    r(A().a1)(a1v1="1", a1v2=["2"])
    assert getter().a1v1 == 1
    assert getter().a1v2 == [2]

    getter = make_collector()
    r(A().a1.run)(a1v1="1", a1v2=["2"])
    assert getter().a1v1 == 1
    assert getter().a1v2 == [2]

    # Second level.

    getter = make_collector()
    r(B().b1)(b1v1="1", b1v2="2")
    assert getter().b1v1 == 1
    assert getter().b1v2 == 2

    getter = make_collector()
    r(B().b1.run)(b1v1="1", b1v2="2")
    assert getter().b1v1 == 1
    assert getter().b1v2 == 2


def test_story_arguments_normalization_many_levels(r, m):
    """We apply normalization to the story arguments on any levels of story
    composition."""

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.ParamParent, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    class C(m.ParamRoot, m.NormalRootMethod):
        def __init__(self):
            self.b1 = B().b1

    # Second level.

    getter = make_collector()
    r(B().b1)(b1v1="1", b1v2="2", a1v1="3", a1v2=["4"])
    assert getter().b1v1 == 1
    assert getter().b1v2 == 2
    assert getter().a1v1 == 3
    assert getter().a1v2 == [4]

    getter = make_collector()
    r(B().b1.run)(b1v1="1", b1v2="2", a1v1="3", a1v2=["4"])
    assert getter().b1v1 == 1
    assert getter().b1v2 == 2
    assert getter().a1v1 == 3
    assert getter().a1v2 == [4]

    getter = make_collector()
    r(C().c1)(c1v1="0", b1v1="1", b1v2="2", a1v1="3", a1v2=["4"])
    assert getter().c1v1 == 0
    assert getter().b1v1 == 1
    assert getter().b1v2 == 2
    assert getter().a1v1 == 3
    assert getter().a1v2 == [4]

    getter = make_collector()
    r(C().c1.run)(c1v1="0", b1v1="1", b1v2="2", a1v1="3", a1v2=["4"])
    assert getter().c1v1 == 0
    assert getter().b1v1 == 1
    assert getter().b1v2 == 2
    assert getter().a1v1 == 3
    assert getter().a1v2 == [4]


def test_story_arguments_normalization_conflict(r, m):
    """Story and substory can have an argument with the same name.

    They both will define validators for this argument.  If normalization result of both
    contracts will mismatch we should raise an error.

    """

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.ParamParentWithSameWithString, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    # Second level.

    expected = """
These arguments have normalization conflict: 'a1v2', 'a1v1'

A.a1:
 - a1v1: 1
 - a1v2: [2]

B.b1:
 - a1v1: '1'
 - a1v2: ['2']

Contract:
  a1v1:
    {int_field_repr}  # Argument of A.a1
    {str_field_repr}  # Argument of B.b1
  a1v2:
    {list_of_int_field_repr}  # Argument of A.a1
    {list_of_str_field_repr}  # Argument of B.b1
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1)(a1v1="1", a1v2=["2"])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1.run)(a1v1="1", a1v2=["2"])
    assert str(exc_info.value) == expected


def test_context_variables_validation(r, m):
    """We apply validators to the context variables, if story defines context
    contract."""

    class A(m.Child, m.WrongMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    # First level.

    expected = (
        """
This variable violates context contract: 'a1v1'

Function returned value: A.a1s1

Violations:

a1v1:
  '<boom>'
  {int_error}

Contract:
  a1v1: {int_field_repr}  # Variable in A.a1
    """.strip()
        .format(**m.representations)
        .format("a1v1")
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1.run)()
    assert str(exc_info.value) == expected

    # Second level.

    expected = (
        """
This variable violates context contract: 'a1v1'

Function returned value: A.a1s1

Violations:

a1v1:
  '<boom>'
  {int_error}

Contract:
  a1v1: {int_field_repr}  # Variable in A.a1
    """.strip()
        .format(**m.representations)
        .format("a1v1")
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1.run)()
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

            self.a1 = A().a1

    # First level.

    expected = (
        """
These arguments violates context contract: 'a1v2', 'a1v1'

Story method: A.a1

Violations:

a1v2:
  ['<boom>']
  {list_of_int_error}

a1v1:
  '<boom>'
  {int_error}

Contract:
  a1v2: {list_of_int_field_repr}  # Argument of A.a1
  a1v1: {int_field_repr}  # Argument of A.a1
    """.strip()
        .format(**m.representations)
        .format("a1v1")
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1)(a1v1="<boom>", a1v2=["<boom>"])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1.run)(a1v1="<boom>", a1v2=["<boom>"])
    assert str(exc_info.value) == expected

    # Second level.

    expected = (
        """
These arguments violates context contract: 'b1v2', 'b1v1'

Story method: B.b1

Violations:

b1v2:
  '<boom>'
  {int_error}

b1v1:
  '<boom>'
  {int_error}

Contract:
  b1v2: {int_field_repr}  # Argument of B.b1
  b1v1: {int_field_repr}  # Argument of B.b1
    """.strip()
        .format(**m.representations)
        .format("b1v2", "b1v1")
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1)(b1v1="<boom>", b1v2="<boom>")
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1.run)(b1v1="<boom>", b1v2="<boom>")
    assert str(exc_info.value) == expected


def test_story_arguments_validation_many_levels(r, m):
    """We apply contract validation to the story arguments on any levels of story
    composition."""

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    class C(m.Root, m.ExceptionRootMethod):
        def __init__(self):
            self.b1 = B().b1

    # Second level.

    expected = (
        """
These arguments violates context contract: 'a1v1'

Story method: C.c1

Violations:

a1v1:
  '<boom>'
  {int_error}

Contract:
  a1v1: {int_field_repr}  # Argument of A.a1
    """.strip()
        .format(**m.representations)
        .format("a1v1")
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(C().c1)(a1v1="<boom>", a1v2=[1])
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(C().c1.run)(a1v1="<boom>", a1v2=[1])
    assert str(exc_info.value) == expected


def test_composition_contract_variable_conflict(r, m):
    """Story and substory contracts can not declare the same variable twice."""

    class A(m.Child, m.NormalMethod):
        pass

    class B(m.ParentWithSame, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    # Second level.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'a1v1', 'a1v2', 'a1v3'

Story method: B.b1

Substory method: A.a1

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        B().b1
    assert str(exc_info.value) == expected


def test_composition_contract_variable_conflict_many_levels(r, m):
    """Story and substory contracts can not declare the same variable twice."""

    class A(m.Child, m.NormalMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    class C(m.RootWithSame, m.NormalRootMethod):
        def __init__(self):
            self.b1 = B().b1

    # Second level.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'a1v1', 'a1v2', 'a1v3'

Story method: C.c1

Substory method: A.a1

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        C().c1
    assert str(exc_info.value) == expected


def test_composition_contract_variable_conflict_sequential(r, m):
    """Story and substory contracts can not declare the same variable twice."""

    class A1(m.Child, m.NormalMethod):
        pass

    class A2(m.NextChildWithSame, m.NormalMethod):
        pass

    class B(m.SequentialParent, m.StringParentMethod):
        def __init__(self):
            self.a1 = A1().a1
            self.a2 = A2().a2

    # Second level.

    expected = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: 'a1v1', 'a1v2', 'a1v3'

Story method: A1.a1

Substory method: A2.a2

Use variables with different names.
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        B().b1
    assert str(exc_info.value) == expected


def test_composition_incompatible_contract_types(r, m):
    """Deny to use different types in the story composition."""

    class A(m.Child, m.NormalMethod):
        pass

    class B(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    # Second level.

    expected = """
Story and substory context contracts has incompatible types:

Story method: B.b1

Story context contract: None

Substory method: A.a1

Substory context contract: {contract_class_repr}
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        B().b1
    assert str(exc_info.value) == expected


def test_unknown_context_variable(r, m):
    """Step can't use Success argument name which was not specified in the contract."""

    class A(m.Child, m.UnknownMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    # First level.

    expected = """
This variable was not defined in the context contract: 'spam'

Function assigned value: A.a1s1

Use a different name for context attribute or add this name to the contract.

Contract:
  a1v1: {int_field_repr}  # Variable in A.a1
  a1v2: {list_of_int_field_repr}  # Variable in A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1.run)()
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
This variable was not defined in the context contract: 'spam'

Function assigned value: A.a1s1

Use a different name for context attribute or add this name to the contract.

Contract:
  a1v1: {int_field_repr}  # Variable in A.a1
  a1v2: {list_of_int_field_repr}  # Variable in A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1.run)()
    assert str(exc_info.value) == expected


def test_unknown_story_arguments_with_null(r, m):
    """Allow to pass known only story and substory arguments to the call."""

    class A(m.ParamChildWithNull, m.NormalMethod):
        pass

    class B(m.ParamParentWithNull, m.NormalParentMethod):
        def __init__(self):
            class A(m.ChildWithNull, m.NormalMethod):
                pass

            self.a1 = A().a1

    # First level.

    expected = """
These arguments are unknown: a1v3, fox

Story method: A.a1

Contract:
  a1v1  # Argument of A.a1
  a1v2  # Argument of A.a1
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1)(a1v3=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1.run)(a1v3=1, fox=2)
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These arguments are unknown: b1v3, fox

Story method: B.b1

Contract:
  b1v1  # Argument of B.b1
  b1v2  # Argument of B.b1
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1)(b1v3=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1.run)(b1v3=1, fox=2)
    assert str(exc_info.value) == expected


def test_unknown_story_arguments(r, m):
    """Allow to pass known only story and substory arguments to the call."""

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.ParamParent, m.NormalParentMethod):
        def __init__(self):
            class A(m.Child, m.NormalMethod):
                pass

            self.a1 = A().a1

    # First level.

    expected = """
These arguments are unknown: a1v3, fox

Story method: A.a1

Contract:
  a1v1: {int_field_repr}  # Argument of A.a1
  a1v2: {list_of_int_field_repr}  # Argument of A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1)(a1v3=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1.run)(a1v3=1, fox=2)
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These arguments are unknown: b1v3, fox

Story method: B.b1

Contract:
  b1v1: {int_field_repr}  # Argument of B.b1
  b1v2: {int_field_repr}  # Argument of B.b1
  a1v1: {int_field_repr}  # Variable in A.a1
  a1v2: {list_of_int_field_repr}  # Variable in A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
  b1v3: {int_field_repr}  # Variable in B.b1
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1)(b1v3=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1.run)(b1v3=1, fox=2)
    assert str(exc_info.value) == expected


def test_unknown_story_arguments_with_empty_with_null(r, m):
    """Deny any arguments in the call, if story and substory has no arguments
    specified."""

    class A(m.ChildWithNull, m.NormalMethod):
        pass

    class B(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    # First level.

    expected = """
These arguments are unknown: a1v3, fox

Story method: A.a1

Contract()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1)(a1v3=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1.run)(a1v3=1, fox=2)
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These arguments are unknown: b1v3, fox

Story method: B.b1

Contract()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1)(b1v3=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1.run)(b1v3=1, fox=2)
    assert str(exc_info.value) == expected


def test_unknown_story_arguments_with_empty(r, m):
    """Deny any arguments in the call, if story and substory has no arguments
    specified."""

    class A(m.Child, m.NormalMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    # First level.

    expected = """
These arguments are unknown: a1v3, fox

Story method: A.a1

Contract:
  a1v1: {int_field_repr}  # Variable in A.a1
  a1v2: {list_of_int_field_repr}  # Variable in A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1)(a1v3=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1.run)(a1v3=1, fox=2)
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These arguments are unknown: b1v3, fox

Story method: B.b1

Contract:
  a1v1: {int_field_repr}  # Variable in A.a1
  a1v2: {list_of_int_field_repr}  # Variable in A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
  b1v1: {int_field_repr}  # Variable in B.b1
  b1v2: {int_field_repr}  # Variable in B.b1
  b1v3: {int_field_repr}  # Variable in B.b1
    """.strip().format(
        **m.representations
    )

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1)(b1v3=1, fox=2)
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1.run)(b1v3=1, fox=2)
    assert str(exc_info.value) == expected


def test_require_story_arguments_present_in_context(r, m):
    """Check story and substory arguments are present in the context."""

    class A(m.ParamChildWithNull, m.NormalMethod):
        pass

    class B(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    # First level.

    expected = """
These variables are missing from the context: a1v1, a1v2

Story method: A.a1

Story arguments: a1v1, a1v2

A.a1

Context()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1)()  # FIXME: This should be arguments error (not substory call error).
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(A().a1.run)()
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These variables are missing from the context: a1v1, a1v2

Story method: A.a1

Story arguments: a1v1, a1v2

B.b1
  b1s1
  a1 (A.a1)

Context()
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1)()
    assert str(exc_info.value) == expected

    with pytest.raises(ContextContractError) as exc_info:
        r(B().b1.run)()
    assert str(exc_info.value) == expected


def test_parent_steps_set_story_arguments(r, m):
    """Steps of parent stories should be able to set child stories arguments with
    `Success` marker keyword arguments."""

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.Parent, m.StringParentMethod):
        def __init__(self):
            self.a1 = A().a1

    class C(m.Root, m.StringRootMethod):
        def __init__(self):
            class B(m.Parent, m.NormalParentMethod):
                def __init__(self):
                    self.a1 = A().a1
            self.b1 = B().b1

    # Second level.

    getter = make_collector()
    r(B().b1)()
    assert getter().a1v1 == 1
    assert getter().a1v2 == [2]

    getter = make_collector()
    r(B().b1.run)()
    assert getter().a1v1 == 1
    assert getter().a1v2 == [2]

    # Third level.

    getter = make_collector()
    r(C().c1)()
    assert getter().a1v1 == 1
    assert getter().a1v2 == [2]

    getter = make_collector()
    r(C().c1.run)()
    assert getter().a1v1 == 1
    assert getter().a1v2 == [2]


def test_sequential_story_steps_set_story_arguments(r, m):
    """There are b1 few sequential substories with a1s1 common parent story.

    One substory should be able to set variable to provide an argument to the next
    sequential story.

    """

    class A1(m.ChildWithShrink, m.StringMethod):
        pass

    class A2(m.NextParamChildWithString, m.NormalNextMethod):
        pass

    class B(m.SequentialParent, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A1().a1
            self.a2 = A2().a2

    # Second level.

    getter = make_collector()
    r(B().b1)()
    assert getter().a1v1 == "1"
    assert getter().a1v2 == ["2"]

    getter = make_collector()
    r(B().b1.run)()
    assert getter().a1v1 == "1"
    assert getter().a1v2 == ["2"]


def test_arguments_should_be_declared_in_contract(r, m):
    """We should require all story arguments to be declared in the context contract."""

    class A(m.ParamChildWithShrink, m.NormalMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    # First level.

    expected = """
These arguments should be declared in the context contract: a1v1, a1v2

Story method: A.a1

Story arguments: a1v1, a1v2, a1v3
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        A().a1
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
These arguments should be declared in the context contract: a1v1, a1v2

Story method: A.a1

Story arguments: a1v1, a1v2, a1v3
    """.strip()

    with pytest.raises(ContextContractError) as exc_info:
        B().b1
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
    r(A().a1)()
    assert getter().a1v1 is getter().a1v2
    assert getter().a1v1 == {"key": "1"}
    assert getter().a1v2 == {"key": "1"}
    assert getter().a1v1 is not getter().a1v3
    assert getter().a1v2 is not getter().a1v3
    assert getter().a1v3 == {"key": 1}

    getter = make_collector()
    r(A().a1.run)()
    assert getter().a1v1 is getter().a1v2
    assert getter().a1v1 == {"key": "1"}
    assert getter().a1v2 == {"key": "1"}
    assert getter().a1v1 is not getter().a1v3
    assert getter().a1v2 is not getter().a1v3
    assert getter().a1v3 == {"key": 1}

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
    r(A().a1)(a1v1=value, a1v2=value, a1v3=value)
    assert getter().a1v1 is getter().a1v2
    assert getter().a1v1 == {"key": "1"}
    assert getter().a1v2 == {"key": "1"}
    assert getter().a1v1 is not getter().a1v3
    assert getter().a1v2 is not getter().a1v3
    assert getter().a1v3 == {"key": 1}

    getter = make_collector()
    r(A().a1.run)(a1v1=value, a1v2=value, a1v3=value)
    assert getter().a1v1 is getter().a1v2
    assert getter().a1v1 == {"key": "1"}
    assert getter().a1v2 == {"key": "1"}
    assert getter().a1v1 is not getter().a1v3
    assert getter().a1v2 is not getter().a1v3
    assert getter().a1v3 == {"key": 1}

    # FIXME: Second level.


# Representation.


def test_story_contract_representation_with_spec(r, m):
    """Show collected story composition contract as mounted story attribute."""

    class A(m.Child, m.StringMethod):
        pass

    class B(m.Parent, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    class C(m.Root, m.NormalRootMethod):
        def __init__(self):
            self.b1 = B().b1

    # First level.

    expected = """
Contract:
  a1v2: {list_of_int_field_repr}  # Variable in A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
  a1v1: {int_field_repr}  # Variable in A.a1
    """.strip().format(
        **m.representations
    )

    assert repr(A().a1.contract) == expected

    # Second level.

    expected = """
Contract:
  a1v2: {list_of_int_field_repr}  # Variable in A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
  b1v3: {int_field_repr}  # Variable in B.b1
  b1v2: {int_field_repr}  # Variable in B.b1
  a1v1: {int_field_repr}  # Variable in A.a1
  b1v1: {int_field_repr}  # Variable in B.b1
    """.strip().format(
        **m.representations
    )

    assert repr(B().b1.contract) == expected

    # Third level.

    expected = """
Contract:
  a1v2: {list_of_int_field_repr}  # Variable in A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
  b1v3: {int_field_repr}  # Variable in B.b1
  c1v2: {int_field_repr}  # Variable in C.c1
  b1v2: {int_field_repr}  # Variable in B.b1
  c1v1: {int_field_repr}  # Variable in C.c1
  a1v1: {int_field_repr}  # Variable in A.a1
  b1v1: {int_field_repr}  # Variable in B.b1
    """.strip().format(
        **m.representations
    )

    assert repr(C().c1.contract) == expected


def test_story_contract_representation_with_spec_with_args(r, m):
    """Show collected story composition contract as mounted story attribute.

    We show each story arguments.

    """

    class A(m.ParamChild, m.StringMethod):
        pass

    class B(m.ParamParent, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    class C(m.ParamRoot, m.NormalRootMethod):
        def __init__(self):
            self.b1 = B().b1

    # First level.

    expected = """
Contract:
  a1v1: {int_field_repr}  # Argument of A.a1
  a1v2: {list_of_int_field_repr}  # Argument of A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
    """.strip().format(
        **m.representations
    )

    assert repr(A().a1.contract) == expected

    # Second level.

    expected = """
Contract:
  a1v1: {int_field_repr}  # Argument of A.a1
  a1v2: {list_of_int_field_repr}  # Argument of A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
  b1v1: {int_field_repr}  # Argument of B.b1
  b1v2: {int_field_repr}  # Argument of B.b1
  b1v3: {int_field_repr}  # Variable in B.b1
    """.strip().format(
        **m.representations
    )

    assert repr(B().b1.contract) == expected

    # Third level.

    expected = """
Contract:
  a1v1: {int_field_repr}  # Argument of A.a1
  a1v2: {list_of_int_field_repr}  # Argument of A.a1
  a1v3: {int_field_repr}  # Variable in A.a1
  b1v1: {int_field_repr}  # Argument of B.b1
  b1v2: {int_field_repr}  # Argument of B.b1
  b1v3: {int_field_repr}  # Variable in B.b1
  c1v1: {int_field_repr}  # Argument of C.c1
  c1v2: {int_field_repr}  # Variable in C.c1
    """.strip().format(
        **m.representations
    )

    assert repr(C().c1.contract) == expected


def test_story_contract_representation_with_spec_with_args_conflict(r, m):
    """Show collected story composition contract as mounted story attribute.

    We show each story arguments in multiline mode if the same name was declared in
    multiple substories.

    """

    class A(m.ParamChild, m.NormalMethod):
        pass

    class B(m.ParamParentWithSameWithString, m.NormalParentMethod):
        def __init__(self):
            self.a1 = A().a1

    # FIXME: Implement this.
    #
    # class C(..., m.NormalRootMethod):
    #     def __init__(self):
    #         self.b1 = B().b1

    # Second level.

    expected = """
Contract:
  a1v1:
    {int_field_repr}  # Argument of A.a1
    {str_field_repr}  # Argument of B.b1
  a1v2:
    {list_of_int_field_repr}  # Argument of A.a1
    {list_of_str_field_repr}  # Argument of B.b1
  a1v3: {int_field_repr}  # Variable in A.a1
    """.strip().format(
        **m.representations
    )

    assert repr(B().b1.contract) == expected

    #     expected = """
    # Contract:
    #   c1v1: ...  # C.c1 argument
    #   b1v1: ...   # B.b1 argument
    #   b1v2: ...  # B.b1 argument
    #   a1v1: ...   # A.a1 argument
    #   a1v2: ...   # A.a1 argument
    #   c1v2: ...  # C.c1 variable
    #   b1v3: ... # B.b1 variable
    #   a1v3: ...   # A.a1 variable
    #     """.strip()
    #
    #     assert repr(C().c1.contract) == expected
