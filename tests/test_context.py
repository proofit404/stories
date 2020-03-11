# -*- coding: utf-8 -*-
import decimal

import pytest

from helpers import make_collector
from stories.exceptions import ContextContractError
from stories.exceptions import FailureError
from stories.exceptions import FailureProtocolError
from stories.exceptions import MutationError


def test_context_private_fields(r, c):
    """Deny access to the private fields of the context object."""

    class T(c.Child, c.PrivateMethod):
        pass

    class Q(c.Parent, c.NormalParentMethod, T):
        pass

    class J(c.Parent, c.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    assert r(T().x)() == {}

    assert r(T().x.run)().value == {}

    # Substory inheritance.

    assert r(Q().a)() == {}

    assert r(Q().a.run)().value == {}

    # Substory DI.

    assert r(J().a)() == {}

    assert r(J().a.run)().value == {}


def test_context_dir(r, c):
    """Show context variables in the `dir` output."""

    class T(c.ParamChild, c.DirMethod):
        pass

    class Q(c.ParamParent, c.DirParentMethod, c.Child, c.NormalMethod):
        foo = 1

    class J(c.ParamParent, c.DirParentMethod):
        def __init__(self):
            class T(c.Child, c.NormalMethod):
                foo = 1

            self.x = T().x

    # Simple.

    class Ctx(object):
        bar = 2

    assert r(T().x)(bar=2) == dir(Ctx())

    assert r(T().x.run)(bar=2).value == dir(Ctx())

    # Substory inheritance.

    class Ctx(object):
        foo = 1
        bar = 2

    assert r(Q().a)(bar=2) == dir(Ctx())

    assert r(Q().a.run)(bar=2).value == dir(Ctx())

    # Substory DI.

    class Ctx(object):
        foo = 1
        bar = 2

    assert r(J().a)(bar=1) == dir(Ctx())

    assert r(J().a.run)(bar=1).value == dir(Ctx())


def test_deny_context_attribute_assignment(r, c):
    """We can't use attribute assignment with `Context` object."""

    class T(c.Child, c.AssignMethod):
        pass

    class Q(c.Parent, c.NormalParentMethod, T):
        pass

    class J(c.Parent, c.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    expected = """
Context object is immutable.

Use Success() keyword arguments to expand its scope.
    """.strip()

    # Simple.

    with pytest.raises(MutationError) as exc_info:
        r(T().x)()
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(T().x.run)()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    with pytest.raises(MutationError) as exc_info:
        r(Q().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(Q().a.run)()
    assert str(exc_info.value) == expected

    # Substory DI.

    with pytest.raises(MutationError) as exc_info:
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_deny_context_attribute_deletion(r, c):
    """We can't use attribute deletion with `Context` object."""

    class T(c.Child, c.DeleteMethod):
        pass

    class Q(c.Parent, c.NormalParentMethod, T):
        pass

    class J(c.Parent, c.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    expected = """
Context object is immutable.

Variables can not be removed from Context.
    """.strip()

    # Simple.

    with pytest.raises(MutationError) as exc_info:
        r(T().x)()
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(T().x.run)()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    with pytest.raises(MutationError) as exc_info:
        r(Q().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(Q().a.run)()
    assert str(exc_info.value) == expected

    # Substory DI.

    with pytest.raises(MutationError) as exc_info:
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_deny_context_boolean_comparison(r, c):
    class T(c.ParamChild, c.CompareMethod):
        pass

    class Q(c.ParamParent, c.NormalParentMethod, T):
        pass

    class J(c.ParamParent, c.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    expected = """
Context object can not be used in boolean comparison.

Available variables: 'bar'
    """.strip()

    # Simple.

    with pytest.raises(MutationError) as exc_info:
        r(T().x)(bar=1)
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(T().x.run)(bar=1)
    assert str(exc_info.value) == expected

    # Substory inheritance.

    with pytest.raises(MutationError) as exc_info:
        r(Q().a)(bar=1)
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(Q().a.run)(bar=1)
    assert str(exc_info.value) == expected

    # Substory DI.

    with pytest.raises(MutationError) as exc_info:
        r(J().a)(bar=1)
    assert str(exc_info.value) == expected

    with pytest.raises(MutationError) as exc_info:
        r(J().a.run)(bar=1)
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
SimpleSubstory.y
  start
  before
  x
    one
    two (failed)

Context:
  spam: 3  # Story argument
  foo: 2   # Set by SimpleSubstory.start
  bar: 4   # Set by SimpleSubstory.before
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(x.SimpleSubstory().y)(spam=3)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.SimpleSubstory().y.run)(spam=3)
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
    class T(f.ChildWithList, f.StringMethod):
        pass

    class Q(f.ParentWithList, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
T.x
  one (failed: 'foo')

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(T().x)()
    assert repr(getter()) == expected

    getter = make_collector()
    r(T().x.run)()
    assert repr(getter()) == expected

    # Substory inheritance.

    expected = """
Q.a
  before
  x
    one (failed: 'foo')

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(Q().a)()
    assert repr(getter()) == expected

    getter = make_collector()
    r(Q().a.run)()
    assert repr(getter()) == expected

    # Substory DI.

    expected = """
J.a
  before
  x (T.x)
    one (failed: 'foo')

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(J().a)()
    assert repr(getter()) == expected

    getter = make_collector()
    r(J().a.run)()
    assert repr(getter()) == expected


def test_context_representation_with_failure_reason_enum(r, f):
    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    class Q(f.ParentWithEnum, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
T.x
  one (failed: <Errors.foo: 1>)

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(T().x)()
    assert repr(getter()) == expected

    getter = make_collector()
    r(T().x.run)()
    assert repr(getter()) == expected

    # Substory inheritance.

    expected = """
Q.a
  before
  x
    one (failed: <Errors.foo: 1>)

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(Q().a)()
    assert repr(getter()) == expected

    getter = make_collector()
    r(Q().a.run)()
    assert repr(getter()) == expected

    # Substory DI.

    expected = """
J.a
  before
  x (T.x)
    one (failed: <Errors.foo: 1>)

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(FailureError):
        r(J().a)()
    assert repr(getter()) == expected

    getter = make_collector()
    r(J().a.run)()
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
SimpleSubstory.y
  start
  before
  x
    one
    two
    three (returned: -1)

Context:
  spam: 2  # Story argument
  foo: 1   # Set by SimpleSubstory.start
  bar: 3   # Set by SimpleSubstory.before
  baz: 4   # Set by SimpleSubstory.two
    """.strip()

    getter = make_collector()
    r(x.SimpleSubstory().y)(spam=2)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.SimpleSubstory().y.run)(spam=2)
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


def test_context_representation_with_skip(r, x):

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
SimpleSubstory.y
  start
  before
  x
    one
    two (skipped)
  after (returned: -4)

Context:
  spam: -2  # Story argument
  foo: -3   # Set by SimpleSubstory.start
  bar: -1   # Set by SimpleSubstory.before
    """.strip()

    getter = make_collector()
    r(x.SimpleSubstory().y)(spam=-2)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.SimpleSubstory().y.run)(spam=-2)
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

    expected = """
SubstoryDI.y
  start
  before
  x (SimpleSubstory.z)
    first (skipped)
  after (returned: 4)

Context:
  spam: 2  # Story argument
  foo: 1   # Set by SubstoryDI.start
  bar: 3   # Set by SubstoryDI.before
    """.strip()

    getter = make_collector()
    r(x.SubstoryDI(x.SimpleSubstory().z).y)(spam=2)
    assert repr(getter()) == expected

    getter = make_collector()
    r(x.SubstoryDI(x.SimpleSubstory().z).y.run)(spam=2)
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
T.x
  one (errored: FailureProtocolError)

Context()
    """.strip()

    class T(f.ChildWithList, f.WrongMethod):
        pass

    getter = make_collector()
    with pytest.raises(FailureProtocolError):
        r(T().x)()
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(FailureProtocolError):
        r(T().x.run)()
    assert repr(getter()) == expected


def test_context_representation_with_context_contract_error(r, m):
    class T(m.ParamChildWithNull, m.StringMethod):
        pass

    class Q(m.ParamParentWithNull, m.StringParentMethod, T):
        pass

    class J(m.ParamParentWithNull, m.StringParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
T.x
  one (errored: ContextContractError)

Context:
  bar: 2  # Story argument
  foo: 1  # Story argument
    """.strip()

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(T().x)(foo=1, bar=2)
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(T().x.run)(foo=1, bar=2)
    assert repr(getter()) == expected

    # Substory inheritance.

    expected = """
Q.a
  before
  x
    one (errored: ContextContractError)

Context:
  eggs: 2     # Story argument
  ham: 1      # Story argument
  bar: ['2']  # Set by Q.before
  foo: '1'    # Set by Q.before
    """.strip()

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(Q().a)(ham=1, eggs=2)
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(Q().a.run)(ham=1, eggs=2)
    assert repr(getter()) == expected

    # Substory DI.

    expected = """
J.a
  before
  x (T.x)
    one (errored: ContextContractError)

Context:
  eggs: 2     # Story argument
  ham: 1      # Story argument
  bar: ['2']  # Set by J.before
  foo: '1'    # Set by J.before
    """.strip()

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(J().a)(ham=1, eggs=2)
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(J().a.run)(ham=1, eggs=2)
    assert repr(getter()) == expected


def test_context_representation_with_missing_variables(r, m):
    class T(m.ParamChildWithNull, m.NormalMethod):
        pass

    class Q(m.ParentWithNull, m.NormalParentMethod, T):
        pass

    class J(m.ParentWithNull, m.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
T.x (errored: ContextContractError)

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(T().x)()
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(T().x.run)()
    assert repr(getter()) == expected

    # Substory inheritance.

    expected = """
Q.a
  before
  x (errored: ContextContractError)

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(Q().a)()
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(Q().a.run)()
    assert repr(getter()) == expected

    # Substory DI.

    expected = """
J.a
  before
  x (T.x) (errored: ContextContractError)

Context()
    """.strip()

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(J().a)()
    assert repr(getter()) == expected

    getter = make_collector()
    with pytest.raises(ContextContractError):
        r(J().a.run)()
    assert repr(getter()) == expected


def test_context_representation_arguments_order(r, x):

    # Simple.

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

    # FIXME: Substory inheritance.

    # FIXME: Substory DI.


def test_context_representation_long_variable(r, c):
    class T(c.ParamChild, c.NormalMethod):
        foo = list(range(23))

    class Q(c.ParamParent, c.NormalParentMethod, T):
        pass

    class J(c.ParamParent, c.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
T.x
  one

Context:
  bar: 'baz'  # Story argument
  foo:        # Set by T.one
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    """.strip()

    getter = make_collector()
    r(T().x)(bar="baz")
    assert repr(getter()) == expected

    getter = make_collector()
    r(T().x.run)(bar="baz")
    assert repr(getter()) == expected

    # Substory inheritance.

    expected = """
Q.a
  before
  x
    one
  after

Context:
  bar: 'baz'  # Story argument
  foo:        # Set by Q.one
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    """.strip()

    getter = make_collector()
    r(Q().a)(bar="baz")
    assert repr(getter()) == expected

    getter = make_collector()
    r(Q().a.run)(bar="baz")
    assert repr(getter()) == expected

    # Substory DI.

    expected = """
J.a
  before
  x (T.x)
    one
  after

Context:
  bar: 'baz'  # Story argument
  foo:        # Set by T.one
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    """.strip()

    getter = make_collector()
    r(J().a)(bar="baz")
    assert repr(getter()) == expected

    getter = make_collector()
    r(J().a.run)(bar="baz")
    assert repr(getter()) == expected


def test_context_representation_multiline_variable(r, c):
    class userlist(list):
        def __repr__(self):
            return "\n ".join(super(userlist, self).__repr__().split())

    class T(c.ParamChild, c.NormalMethod):
        foo = userlist(range(3))

    class Q(c.ParamParent, c.NormalParentMethod, T):
        pass

    class J(c.ParamParent, c.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
T.x
  one

Context:
  bar: 'baz'  # Story argument
  foo:        # Set by T.one
    [0,
     1,
     2]
    """.strip()

    getter = make_collector()
    r(T().x)(bar="baz")
    assert repr(getter()) == expected

    getter = make_collector()
    r(T().x.run)(bar="baz")
    assert repr(getter()) == expected

    # Substory inheritance.

    expected = """
Q.a
  before
  x
    one
  after

Context:
  bar: 'baz'  # Story argument
  foo:        # Set by Q.one
    [0,
     1,
     2]
    """.strip()

    getter = make_collector()
    r(Q().a)(bar="baz")
    assert repr(getter()) == expected

    getter = make_collector()
    r(Q().a.run)(bar="baz")
    assert repr(getter()) == expected

    # Substory DI.

    expected = """
J.a
  before
  x (T.x)
    one
  after

Context:
  bar: 'baz'  # Story argument
  foo:        # Set by T.one
    [0,
     1,
     2]
    """.strip()

    getter = make_collector()
    r(J().a)(bar="baz")
    assert repr(getter()) == expected

    getter = make_collector()
    r(J().a.run)(bar="baz")
    assert repr(getter()) == expected


def test_context_representation_variable_aliases(r, c):
    class T(c.ParamChild, c.NormalMethod):
        foo = "baz"

    class Q(c.ParamParent, c.NormalParentMethod, T):
        pass

    class J(c.ParamParent, c.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
T.x
  one

Context:
  bar: 'baz'        # Story argument
  foo: `bar` alias  # Set by T.one
    """.strip()

    getter = make_collector()
    r(T().x)(bar=T.foo)
    assert repr(getter()) == expected

    getter = make_collector()
    r(T().x.run)(bar=T.foo)
    assert repr(getter()) == expected

    # Substory inheritance.

    expected = """
Q.a
  before
  x
    one
  after

Context:
  bar: 'baz'        # Story argument
  foo: `bar` alias  # Set by Q.one
    """.strip()

    getter = make_collector()
    r(Q().a)(bar=T.foo)
    assert repr(getter()) == expected

    getter = make_collector()
    r(Q().a.run)(bar=T.foo)
    assert repr(getter()) == expected

    # Substory DI.

    expected = """
J.a
  before
  x (T.x)
    one
  after

Context:
  bar: 'baz'        # Story argument
  foo: `bar` alias  # Set by T.one
    """.strip()

    getter = make_collector()
    r(J().a)(bar=T.foo)
    assert repr(getter()) == expected

    getter = make_collector()
    r(J().a.run)(bar=T.foo)
    assert repr(getter()) == expected


@pytest.mark.parametrize("arg", [None, True, 1, 1.0, decimal.Decimal("1.0")])
def test_context_representation_variable_aliases_ignore(r, c, arg):
    class T(c.ParamChild, c.NormalMethod):
        foo = arg

    class Q(c.ParamParent, c.NormalParentMethod, T):
        pass

    class J(c.ParamParent, c.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
T.x
  one

Context:
  bar: %(arg)s  # Story argument
  foo: %(arg)s  # Set by T.one
    """.strip() % {
        "arg": repr(arg)
    }

    getter = make_collector()
    r(T().x)(bar=T.foo)
    assert repr(getter()) == expected

    getter = make_collector()
    r(T().x.run)(bar=T.foo)
    assert repr(getter()) == expected

    # Substory inheritance.

    expected = """
Q.a
  before
  x
    one
  after

Context:
  bar: %(arg)s  # Story argument
  foo: %(arg)s  # Set by Q.one
    """.strip() % {
        "arg": repr(arg)
    }

    getter = make_collector()
    r(Q().a)(bar=T.foo)
    assert repr(getter()) == expected

    getter = make_collector()
    r(Q().a.run)(bar=T.foo)
    assert repr(getter()) == expected

    # Substory DI.

    expected = """
J.a
  before
  x (T.x)
    one
  after

Context:
  bar: %(arg)s  # Story argument
  foo: %(arg)s  # Set by T.one
    """.strip() % {
        "arg": repr(arg)
    }

    getter = make_collector()
    r(J().a)(bar=T.foo)
    assert repr(getter()) == expected

    getter = make_collector()
    r(J().a.run)(bar=T.foo)
    assert repr(getter()) == expected
