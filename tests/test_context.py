import decimal

import pytest

from helpers import make_collector
from stories.exceptions import ContextContractError
from stories.exceptions import FailureError
from stories.exceptions import FailureProtocolError
from stories.exceptions import MutationError


def test_context_private_fields(r, c):
    """Deny access to the private fields of the context object."""

    class A(c.Child, c.PrivateMethod):
        pass

    class B(c.Parent, c.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    assert r(A().x)() == {}

    assert r(A().x.run)().value == {}

    # Second level.

    assert r(B().a)() == {}

    assert r(B().a.run)().value == {}


def test_context_dir(r, c):
    """Show context variables in the `dir` output."""

    class A(c.ParamChild, c.DirMethod):
        pass

    class B(c.ParamParent, c.DirParentMethod):
        def __init__(self):
            class A(c.Child, c.NormalMethod):
                foo = 1

            self.x = A().x

    # First level.

    class Ctx:
        bar = 2

    assert r(A().x)(bar=2) == dir(Ctx())

    assert r(A().x.run)(bar=2).value == dir(Ctx())

    # Second level.

    class Ctx:
        foo = 1
        bar = 2

    assert r(B().a)(bar=1) == dir(Ctx())

    assert r(B().a.run)(bar=1).value == dir(Ctx())


def test_deny_context_attribute_deletion(r, c):
    """We can't use attribute deletion with `Context` object."""

    class A(c.Child, c.DeleteMethod):
        pass

    class B(c.Parent, c.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    expected = """
Context object is immutable.

Variables can not be removed from Context.
    """.strip()

    # First level.

    with pytest.raises(MutationError) as exc_info:
        r(A().x)()
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(A().x.run)()
    assert str(exc_info.value) == expected

    # Second level.

    with pytest.raises(MutationError) as exc_info:
        r(B().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(B().a.run)()
    assert str(exc_info.value) == expected


def test_deny_context_boolean_comparison(r, c):
    class A(c.ParamChild, c.CompareMethod):
        pass

    class B(c.ParamParent, c.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    expected = """
Context object can not be used in boolean comparison.

Available variables: 'bar'
    """.strip()

    # First level.

    with pytest.raises(MutationError) as exc_info:
        r(A().x)(bar=1)
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(A().x.run)(bar=1)
    assert str(exc_info.value) == expected

    # Second level.

    with pytest.raises(MutationError) as exc_info:
        r(B().a)(bar=1)
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(B().a.run)(bar=1)
    assert str(exc_info.value) == expected


def test_context_proper_getattr_behavior(r, x):
    expected = """
Branch.show_content
  age_lt_18
  age_gte_18
  load_content (returned: 'allowed')

Context:
  age: 18               # Story argument
  access_allowed: True  # Set by Branch.age_gte_18
    """.strip()
    getter = make_collector()
    r(x.Branch().show_content)(age=18)
    result = repr(getter())
    assert result == expected

    expected = """
Branch.show_content
  age_lt_18
  age_gte_18
  load_content (returned: 'denied')

Context:
  age: 1                 # Story argument
  access_allowed: False  # Set by Branch.age_lt_18
    """.strip()
    getter = make_collector()
    r(x.Branch().show_content)(age=1)
    result = repr(getter())
    assert result == expected


def test_context_attribute_error(r, x):
    expected = """
'Context' object has no attribute x

AttributeAccessError.x
  one

Context()
    """.strip()
    with pytest.raises(AttributeError) as err:
        r(x.AttributeAccessError().x)()
    result = str(err.value)
    assert result == expected


def test_context_representation_with_failure(r, x):

    expected = """
Simple.x
  one
  two (failed)

Context:
  bar: 2  # Story argument
  foo: 3  # Story argument
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(x.Simple().x)(foo=3, bar=2)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.Simple().x.run)(foo=3, bar=2)
    assert repr(getter()) == expected

    expected = """
SubstoryDI.y
  start
  before
  x (Simple.x)
    one
    two (failed)

Context:
  spam: 3  # Story argument
  foo: 2   # Set by SubstoryDI.start
  bar: 4   # Set by SubstoryDI.before
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(x.SubstoryDI(x.Simple().x).y)(spam=3)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.SubstoryDI(x.Simple().x).y.run)(spam=3)
    assert repr(getter()) == expected


def test_context_representation_with_failure_reason_list(r, f):
    class A(f.ChildWithList, f.StringMethod):
        pass

    class Q(f.ParentWithList, f.NormalParentMethod, A):
        pass

    class B(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
A.x
  one (failed: 'foo')

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(A().x)()
    assert repr(getter()) == expected

    getter = make_collector()
    r(A().x.run)()
    assert repr(getter()) == expected

    # Second level.

    expected = """
B.a
  before
  x (A.x)
    one (failed: 'foo')

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(B().a)()
    assert repr(getter()) == expected

    getter = make_collector()
    r(B().a.run)()
    assert repr(getter()) == expected


def test_context_representation_with_failure_reason_enum(r, f):
    class A(f.ChildWithEnum, f.EnumMethod):
        pass

    class B(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
A.x
  one (failed: <Errors.foo: 1>)

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(A().x)()
    assert repr(getter()) == expected

    getter = make_collector()
    r(A().x.run)()
    assert repr(getter()) == expected

    # Second level.

    expected = """
B.a
  before
  x (A.x)
    one (failed: <Errors.foo: 1>)

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(B().a)()
    assert repr(getter()) == expected

    getter = make_collector()
    r(B().a.run)()
    assert repr(getter()) == expected


def test_context_representation_with_result(r, x):

    expected = """
Simple.x
  one
  two
  three (returned: -1)

Context:
  bar: 3  # Story argument
  foo: 1  # Story argument
  baz: 4  # Set by Simple.two
    """.strip()

    getter = make_collector()
    r(x.Simple().x)(foo=1, bar=3)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.Simple().x.run)(foo=1, bar=3)
    assert repr(getter()) == expected

    expected = """
SubstoryDI.y
  start
  before
  x (Simple.x)
    one
    two
    three (returned: -1)

Context:
  spam: 2  # Story argument
  foo: 1   # Set by SubstoryDI.start
  bar: 3   # Set by SubstoryDI.before
  baz: 4   # Set by Simple.two
    """.strip()

    getter = make_collector()
    r(x.SubstoryDI(x.Simple().x).y)(spam=2)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.SubstoryDI(x.Simple().x).y.run)(spam=2)
    assert repr(getter()) == expected

    expected = """
SubstoryDI.y
  start
  before
  x (Pipe.x)
    one
    two
    three
  after (returned: 6)

Context:
  spam: 3  # Story argument
  foo: 2   # Set by SubstoryDI.start
  bar: 4   # Set by SubstoryDI.before
    """.strip()

    getter = make_collector()
    r(x.SubstoryDI(x.Pipe().x).y)(spam=3)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.SubstoryDI(x.Pipe().x).y.run)(spam=3)
    assert repr(getter()) == expected


def test_context_representation_with_next(r, x):

    expected = """
Simple.x
  one
  two (skipped)

Context:
  bar: -1  # Story argument
  foo: 1   # Story argument
    """.strip()

    getter = make_collector()
    r(x.Simple().x)(foo=1, bar=-1)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.Simple().x.run)(foo=1, bar=-1)
    assert repr(getter()) == expected

    expected = """
SubstoryDI.y
  start
  before
  x (Simple.x)
    one
    two (skipped)
  after (returned: -4)

Context:
  spam: -2  # Story argument
  foo: -3   # Set by SubstoryDI.start
  bar: -1   # Set by SubstoryDI.before
    """.strip()

    getter = make_collector()
    r(x.SubstoryDI(x.Simple().x).y)(spam=-2)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.SubstoryDI(x.Simple().x).y.run)(spam=-2)
    assert repr(getter()) == expected


def test_context_representation_with_error(r, x):

    expected = """
StepError.x
  one (errored: ExpectedException)

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(x.ExpectedException):
        r(x.StepError().x)()
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(x.ExpectedException):
        r(x.StepError().x.run)()
    assert repr(getter()) == expected


def test_context_representation_with_failure_protocol_error(r, f):

    expected = """
A.x
  one (errored: FailureProtocolError)

Context()
    """.strip()

    class A(f.ChildWithList, f.WrongMethod):
        pass

    getter = make_collector()
    with pytest.raises(FailureProtocolError):
        r(A().x)()
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(FailureProtocolError):
        r(A().x.run)()
    assert repr(getter()) == expected


def test_context_representation_with_context_contract_error(r, m):
    class A(m.ParamChildWithNull, m.StringMethod):
        pass

    class B(m.ParamParentWithNull, m.StringParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
A.x
  one (errored: ContextContractError)

Context:
  bar: 2  # Story argument
  foo: 1  # Story argument
    """.strip()

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(A().x)(foo=1, bar=2)
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(A().x.run)(foo=1, bar=2)
    assert repr(getter()) == expected

    # Second level.

    expected = """
B.a
  before
  x (A.x)
    one (errored: ContextContractError)

Context:
  eggs: 2     # Story argument
  ham: 1      # Story argument
  foo: '1'    # Set by B.before
  bar: ['2']  # Set by B.before
    """.strip()

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(B().a)(ham=1, eggs=2)
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(B().a.run)(ham=1, eggs=2)
    assert repr(getter()) == expected


def test_context_representation_with_missing_variables(r, m):
    class A(m.ParamChildWithNull, m.NormalMethod):
        pass

    class B(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
A.x (errored: ContextContractError)

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(A().x)()
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(A().x.run)()
    assert repr(getter()) == expected

    # Second level.

    expected = """
B.a
  before
  x (A.x) (errored: ContextContractError)

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(B().a)()
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(B().a.run)()
    assert repr(getter()) == expected


def test_context_representation_arguments_order(r, x):

    # First level.

    expected = """
Simple.x
  one
  two
  three (returned: -1)

Context:
  bar: 3  # Story argument
  foo: 1  # Story argument
  baz: 4  # Set by Simple.two
    """.strip()

    getter = make_collector()
    r(x.Simple().x)(bar=3, foo=1)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.Simple().x.run)(bar=3, foo=1)
    assert repr(getter()) == expected

    # FIXME: Second level.


def test_context_representation_long_variable(r, c):
    class A(c.ParamChild, c.NormalMethod):
        foo = list(range(23))

    class B(c.ParamParent, c.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
A.x
  one

Context:
  bar: 'baz'  # Story argument
  foo:        # Set by A.one
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    """.strip()

    getter = make_collector()
    r(A().x)(bar="baz")
    assert repr(getter()) == expected

    getter = make_collector()
    r(A().x.run)(bar="baz")
    assert repr(getter()) == expected

    # Second level.

    expected = """
B.a
  before
  x (A.x)
    one
  after

Context:
  bar: 'baz'  # Story argument
  foo:        # Set by A.one
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    """.strip()

    getter = make_collector()
    r(B().a)(bar="baz")
    assert repr(getter()) == expected

    getter = make_collector()
    r(B().a.run)(bar="baz")
    assert repr(getter()) == expected


def test_context_representation_multiline_variable(r, c):
    class userlist(list):
        def __repr__(self):
            return "\n ".join(super().__repr__().split())

    class A(c.ParamChild, c.NormalMethod):
        foo = userlist(range(3))

    class B(c.ParamParent, c.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
A.x
  one

Context:
  bar: 'baz'  # Story argument
  foo:        # Set by A.one
    [0,
     1,
     2]
    """.strip()

    getter = make_collector()
    r(A().x)(bar="baz")
    assert repr(getter()) == expected

    getter = make_collector()
    r(A().x.run)(bar="baz")
    assert repr(getter()) == expected

    # Second level.

    expected = """
B.a
  before
  x (A.x)
    one
  after

Context:
  bar: 'baz'  # Story argument
  foo:        # Set by A.one
    [0,
     1,
     2]
    """.strip()

    getter = make_collector()
    r(B().a)(bar="baz")
    assert repr(getter()) == expected

    getter = make_collector()
    r(B().a.run)(bar="baz")
    assert repr(getter()) == expected


def test_context_representation_variable_aliases(r, c):
    class A(c.ParamChild, c.NormalMethod):
        foo = "baz"

    class B(c.ParamParent, c.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
A.x
  one

Context:
  bar: 'baz'        # Story argument
  foo: `bar` alias  # Set by A.one
    """.strip()

    getter = make_collector()
    r(A().x)(bar=A.foo)
    assert repr(getter()) == expected

    getter = make_collector()
    r(A().x.run)(bar=A.foo)
    assert repr(getter()) == expected

    # Second level.

    expected = """
B.a
  before
  x (A.x)
    one
  after

Context:
  bar: 'baz'        # Story argument
  foo: `bar` alias  # Set by A.one
    """.strip()

    getter = make_collector()
    r(B().a)(bar=A.foo)
    assert repr(getter()) == expected

    getter = make_collector()
    r(B().a.run)(bar=A.foo)
    assert repr(getter()) == expected


@pytest.mark.parametrize("arg", [None, True, 1, 1.0, decimal.Decimal("1.0")])
def test_context_representation_variable_aliases_ignore(r, c, arg):
    class A(c.ParamChild, c.NormalMethod):
        foo = arg

    class B(c.ParamParent, c.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
A.x
  one

Context:
  bar: %(arg)s  # Story argument
  foo: %(arg)s  # Set by A.one
    """.strip() % {
        "arg": repr(arg)
    }

    getter = make_collector()
    r(A().x)(bar=A.foo)
    assert repr(getter()) == expected

    getter = make_collector()
    r(A().x.run)(bar=A.foo)
    assert repr(getter()) == expected

    # Second level.

    expected = """
B.a
  before
  x (A.x)
    one
  after

Context:
  bar: %(arg)s  # Story argument
  foo: %(arg)s  # Set by A.one
    """.strip() % {
        "arg": repr(arg)
    }

    getter = make_collector()
    r(B().a)(bar=A.foo)
    assert repr(getter()) == expected

    getter = make_collector()
    r(B().a.run)(bar=A.foo)
    assert repr(getter()) == expected
