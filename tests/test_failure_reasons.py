import enum

import pytest

import examples.failure_reasons as f
from stories import story
from stories.exceptions import FailureError, FailureProtocolError


# FIXME:
#
# Comparison of the Enum should work:
#
# T().a.failures.foo is T().a.run().failure_reason
#
# Story collected twice here.


# Story definition.


def test_wrong_definition():
    """We check types used in failures definition."""

    expected = "Unexpected type for story failure protocol: 'boom'"

    class T(object):
        @story
        def x(I):
            I.one

    with pytest.raises(FailureProtocolError) as exc_info:
        T.x.failures("boom")
    assert str(exc_info.value) == expected


# Arguments of the Failure class.


def test_reasons_defined_with_list():
    """We can use list of strings to define story failure protocol."""

    class T(f.ChildWithList, f.StringMethod):
        pass

    class Q(f.ParentWithList, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    assert T().x.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureError) as exc_info:
        T().x()
    assert exc_info.value.reason == "foo"
    assert repr(exc_info.value) == "FailureError('foo')"

    result = T().x.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason == "foo"
    assert result.failed_because("foo")

    # Substory inheritance.

    assert Q().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureError) as exc_info:
        Q().a()
    assert exc_info.value.reason == "foo"
    assert repr(exc_info.value) == "FailureError('foo')"

    result = Q().a.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason == "foo"
    assert result.failed_because("foo")

    # Substory DI.

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureError) as exc_info:
        J().a()
    assert exc_info.value.reason == "foo"
    assert repr(exc_info.value) == "FailureError('foo')"

    result = J().a.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason == "foo"
    assert result.failed_because("foo")


def test_reasons_defined_with_enum():
    """We can use enum class to define story failure protocol."""

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    class Q(f.ParentWithEnum, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    assert isinstance(T().x.failures, enum.EnumMeta)
    assert set(T().x.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureError) as exc_info:
        T().x()
    # assert exc_info.value.reason is T().x.failures.foo
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = T().x.run()
    assert not result.is_success
    assert result.is_failure
    # assert result.failure_reason is T().x.failures.foo
    assert result.failed_because(T().x.failures.foo)

    # Substory inheritance.

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureError) as exc_info:
        Q().a()
    # assert exc_info.value.reason is Q().a.failures.foo
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = Q().a.run()
    assert not result.is_success
    assert result.is_failure
    # assert result.failure_reason is Q().a.failures.foo
    assert result.failed_because(Q().a.failures.foo)

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureError) as exc_info:
        J().a()
    # assert exc_info.value.reason is J().a.failures.foo
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = J().a.run()
    assert not result.is_success
    assert result.is_failure
    # assert result.failure_reason is J().a.failures.foo
    assert result.failed_because(J().a.failures.foo)


def test_wrong_reason_with_list():
    """
    We deny to use wrong reason in stories defined with list of
    strings as its failure protocol.
    """

    class T(f.ChildWithList, f.WrongMethod):
        pass

    class Q(f.ParentWithList, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: T.one
    """.strip()

    assert T().x.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        T().x()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        T().x.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: Q.one
    """.strip()

    assert Q().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: T.one
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_wrong_reason_with_enum():
    """
    We deny to use wrong reason in stories defined with enum class as
    its failure protocol.
    """

    class T(f.ChildWithEnum, f.WrongMethod):
        pass

    class Q(f.ParentWithEnum, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: T.one
    """.strip()

    assert isinstance(T().x.failures, enum.EnumMeta)
    assert set(T().x.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        T().x()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        T().x.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: Q.one
    """.strip()

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: T.one
    """.strip()

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_null_reason_with_list():
    """
    We deny to use Failure() in stories defined with list of strings
    as its failure protocol.
    """

    class T(f.ChildWithList, f.NullMethod):
        pass

    class Q(f.ParentWithList, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: T.one

Use one of them as Failure() argument.
    """.strip()

    assert T().x.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        T().x()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        T().x.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: Q.one

Use one of them as Failure() argument.
    """.strip()

    assert Q().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: T.one

Use one of them as Failure() argument.
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_null_reason_with_enum():
    """
    We deny to use Failure() in stories defined with enum class as its
    failure protocol.
    """

    class T(f.ChildWithEnum, f.NullMethod):
        pass

    class Q(f.ParentWithEnum, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: T.one

Use one of them as Failure() argument.
    """.strip()

    assert isinstance(T().x.failures, enum.EnumMeta)
    assert set(T().x.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        T().x()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        T().x.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: Q.one

Use one of them as Failure() argument.
    """.strip()

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: T.one

Use one of them as Failure() argument.
    """.strip()

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_reason_without_protocol():
    """
    We deny to use Failure('reason') in stories defined without
    failure protocol.
    """

    class T(f.ChildWithNull, f.WrongMethod):
        pass

    class Q(f.ParentWithNull, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
Failure("'foo' is too big") can not be used in a story without failure protocol.

Function returned value: T.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert T().x.failures is None

    with pytest.raises(FailureProtocolError) as exc_info:
        T().x()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        T().x.run()
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Failure("'foo' is too big") can not be used in a story without failure protocol.

Function returned value: Q.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert Q().a.failures is None

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure("'foo' is too big") can not be used in a story without failure protocol.

Function returned value: T.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert J().a.failures is None

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


# Arguments of the result class methods.


@pytest.mark.parametrize("method", [f.NormalMethod, f.StringMethod])
def test_summary_wrong_reason_with_list(method):
    """
    Summary classes should verify failure reason passed to the
    `failed_because` method.
    """

    class T(f.ChildWithList, method):
        pass

    class Q(f.ParentWithList, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: 'foo', 'bar', 'baz'

Story returned result: T.x
    """.strip()

    assert T().x.failures == ["foo", "bar", "baz"]

    result = T().x.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: 'foo', 'bar', 'baz'

Story returned result: Q.a
    """.strip()

    assert Q().a.failures == ["foo", "bar", "baz"]

    result = Q().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: 'foo', 'bar', 'baz'

Story returned result: J.a
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    result = J().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


@pytest.mark.parametrize("method", [f.NormalMethod, f.EnumMethod])
def test_summary_wrong_reason_with_enum(method):
    """
    Summary classes should verify failure reason passed to the
    `failed_because` method.
    """

    class T(f.ChildWithEnum, method):
        pass

    class Q(f.ParentWithEnum, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Story returned result: T.x
    """.strip()

    assert isinstance(T().x.failures, enum.EnumMeta)
    assert set(T().x.failures.__members__.keys()) == {"foo", "bar", "baz"}

    result = T().x.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Story returned result: Q.a
    """.strip()

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    result = Q().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Story returned result: J.a
    """.strip()

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    result = J().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


@pytest.mark.parametrize("method", [f.NormalMethod, f.NullMethod])
def test_summary_reason_without_protocol(method):
    """
    Summary classes should deny to use `failed_because` method on
    stories defined without failure protocol.
    """

    class T(f.ChildWithNull, method):
        pass

    class Q(f.ParentWithNull, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
'failed_because' method can not be used with story defined without failure protocol.

Story returned result: T.x

Use 'failures' story method to define failure protocol.
    """.strip()

    assert T().x.failures is None

    result = T().x.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
'failed_because' method can not be used with story defined without failure protocol.

Story returned result: Q.a

Use 'failures' story method to define failure protocol.
    """.strip()

    assert Q().a.failures is None

    result = Q().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
'failed_because' method can not be used with story defined without failure protocol.

Story returned result: J.a

Use 'failures' story method to define failure protocol.
    """.strip()

    assert J().a.failures is None

    result = J().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


# Composition of the stories.


def test_substory_protocol_match_with_empty():
    """
    We should allow to use stories composition, if parent story and
    substory does not define failure protocols.
    """

    class T(f.ChildWithNull, f.NullMethod):
        pass

    class Q(f.ParentWithNull, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    Q().a.failures is None

    with pytest.raises(FailureError) as exc_info:
        Q().a()
    assert exc_info.value.reason is None

    result = Q().a.run()
    assert result.failure_reason is None

    # Substory DI.

    J().a.failures is None

    with pytest.raises(FailureError) as exc_info:
        J().a()
    assert exc_info.value.reason is None

    result = J().a.run()
    assert result.failure_reason is None


def test_substory_protocol_match_with_list():
    """
    We should allow to use stories composition, if parent story
    protocol is a superset of the substory protocol.
    """

    class T(f.ChildWithList, f.StringMethod):
        pass

    class Q(f.WideParentWithList, f.NormalParentMethod, T):
        pass

    class J(f.WideParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    assert Q().a.failures == ["foo", "bar", "baz", "quiz"]

    with pytest.raises(FailureError) as exc_info:
        Q().a()
    assert exc_info.value.reason == "foo"

    result = Q().a.run()
    assert result.failed_because("foo")

    # Substory DI.

    assert J().a.failures == ["foo", "bar", "baz", "quiz"]

    with pytest.raises(FailureError) as exc_info:
        J().a()
    assert exc_info.value.reason == "foo"

    result = J().a.run()
    assert result.failed_because("foo")


def test_substory_protocol_match_with_enum():
    """
    We should allow to use stories composition, if parent story
    protocol is a superset of the substory protocol.
    """

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    class Q(f.WideParentWithEnum, f.NormalParentMethod, T):
        pass

    class J(f.WideParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz", "quiz"}

    with pytest.raises(FailureError):
        Q().a()
    # assert exc_info.value.reason is Q().a.failures.foo

    result = Q().a.run()
    assert result.failed_because(Q().a.failures.foo)

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz", "quiz"}

    with pytest.raises(FailureError):
        J().a()
    # assert exc_info.value.reason is J().a.failures.foo

    result = J().a.run()
    assert result.failed_because(J().a.failures.foo)


def test_expand_substory_protocol_null_with_list():
    """
    We expand protocol of composed story, if substory does not define
    failure protocols and parent story define protocol with list of
    strings.
    """

    class T(f.ChildWithNull, f.NormalMethod):
        pass

    class Q(f.ParentWithList, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    assert Q().a.failures == ["foo", "bar", "baz"]

    result = Q().a()
    assert result is None

    result = Q().a.run()
    assert result.is_success
    assert result.value is None

    # Substory DI.

    assert J().a.failures == ["foo", "bar", "baz"]

    result = J().a()
    assert result is None

    result = J().a.run()
    assert result.is_success
    assert result.value is None


def test_expand_substory_protocol_null_with_enum():
    """
    We expand protocol of composed story, if substory does not define
    protocol and parent story define protocol with enum class.
    """

    class T(f.ChildWithNull, f.NormalMethod):
        pass

    class Q(f.ParentWithEnum, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    result = Q().a()
    assert result is None

    result = Q().a.run()
    assert result.is_success
    assert result.value is None

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    result = J().a()
    assert result is None

    result = J().a.run()
    assert result.is_success
    assert result.value is None


def test_deny_failure_substory_without_protocol_story_protocol_with_list():
    """
    Substory defined without failure protocol can not return Failure,
    if this substory was composed with parent story defined with list
    of strings as failure protocol.
    """

    class T(f.ChildWithNull, f.NullMethod):
        pass

    class Q(f.ParentWithList, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Failure() can not be used in a story composition.

Different types of failure protocol were used in parent and substory definitions.

Function returned value: Q.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert Q().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure() can not be used in a story composition.

Different types of failure protocol were used in parent and substory definitions.

Function returned value: T.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_deny_failure_substory_without_protocol_story_protocol_with_enum():
    """
    Substory defined without failure protocol can not return Failure,
    if this substory was composed with parent story defined with enum
    as failure protocol.
    """

    class T(f.ChildWithNull, f.NullMethod):
        pass

    class Q(f.ParentWithEnum, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Failure() can not be used in a story composition.

Different types of failure protocol were used in parent and substory definitions.

Function returned value: Q.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure() can not be used in a story composition.

Different types of failure protocol were used in parent and substory definitions.

Function returned value: T.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_deny_failure_story_without_protocol_substory_protocol_with_list():
    """
    Story defined without failure protocol can not return Failure, if
    this story was composed with substory defined with list of strings
    as failure protocol.
    """

    class T(f.ChildWithList, f.NormalMethod):
        pass

    class Q(f.ParentWithNull, f.NullParentMethod, T):
        pass

    class J(f.ParentWithNull, f.NullParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Failure() can not be used in a story composition.

Different types of failure protocol were used in parent and substory definitions.

Function returned value: Q.before

Use 'failures' story method to define failure protocol.
    """.strip()

    assert Q().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure() can not be used in a story composition.

Different types of failure protocol were used in parent and substory definitions.

Function returned value: J.before

Use 'failures' story method to define failure protocol.
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_deny_failure_story_without_protocol_substory_protocol_with_enum():
    """
    Story defined without failure protocol can not return Failure, if
    this story was composed with substory defined with enum as failure
    protocol.
    """

    class T(f.ChildWithEnum, f.NormalMethod):
        pass

    class Q(f.ParentWithNull, f.NullParentMethod, T):
        pass

    class J(f.ParentWithNull, f.NullParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Failure() can not be used in a story composition.

Different types of failure protocol were used in parent and substory definitions.

Function returned value: Q.before

Use 'failures' story method to define failure protocol.
    """.strip()

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure() can not be used in a story composition.

Different types of failure protocol were used in parent and substory definitions.

Function returned value: J.before

Use 'failures' story method to define failure protocol.
    """.strip()

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_expand_substory_protocol_list_with_null():
    """
    We expand protocol of composed story, if substory define protocol
    with list of strings and parent story does not define protocol.
    """

    class T(f.ChildWithList, f.NormalMethod):
        pass

    class Q(f.ParentWithNull, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    assert Q().a.failures == ["foo", "bar", "baz"]

    result = Q().a()
    assert result is None

    result = Q().a.run()
    assert result.is_success
    assert result.value is None

    # Substory DI.

    assert J().a.failures == ["foo", "bar", "baz"]

    result = J().a()
    assert result is None

    result = J().a.run()
    assert result.is_success
    assert result.value is None


def test_expand_substory_protocol_enum_with_null():
    """
    We expand protocol of composed story, if substory define protocol
    with enum class and parent story does not define protocol.
    """

    class T(f.ChildWithEnum, f.NormalMethod):
        pass

    class Q(f.ParentWithNull, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    result = Q().a()
    assert result is None

    result = Q().a.run()
    assert result.is_success
    assert result.value is None

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    result = J().a()
    assert result is None

    result = J().a.run()
    assert result.is_success
    assert result.value is None


def test_expand_substory_protocol_list_with_list():
    """
    We expand protocol of composed story, if substory and parent story
    define protocol with list of strings.
    """

    class T(f.ChildWithList, f.StringMethod):
        pass

    class Q(f.ShrinkParentWithList, f.NormalParentMethod, T):
        pass

    class J(f.ShrinkParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    assert Q().a.failures == ["foo", "quiz", "bar", "baz"]

    with pytest.raises(FailureError) as exc_info:
        Q().a()
    assert exc_info.value.reason == "foo"

    result = Q().a.run()
    assert result.failed_because("foo")

    # Substory DI.

    assert J().a.failures == ["foo", "quiz", "bar", "baz"]

    with pytest.raises(FailureError) as exc_info:
        J().a()
    assert exc_info.value.reason == "foo"

    result = J().a.run()
    assert result.failed_because("foo")


def test_expand_substory_protocol_enum_with_enum():
    """
    We expand protocol of composed story, if substory and parent story
    define protocol with enum class.
    """

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    class Q(f.ShrinkParentWithEnum, f.NormalParentMethod, T):
        pass

    class J(f.ShrinkParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz", "quiz"}

    with pytest.raises(FailureError):
        Q().a()
    # assert exc_info.value.reason is Q().a.failures.foo

    result = Q().a.run()
    assert result.failed_because(Q().a.failures.foo)

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz", "quiz"}

    with pytest.raises(FailureError):
        J().a()
    # assert exc_info.value.reason is J().a.failures.foo

    result = J().a.run()
    assert result.failed_because(J().a.failures.foo)


def test_composition_type_error_list_with_enum():
    """We can't combine different types of stories and substories."""

    class T(f.ChildWithList, f.StringMethod):
        pass

    class Q(f.ParentWithEnum, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Story and substory failure protocols has incompatible types:

Story method: Q.a

Story failure protocol: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Substory method: Q.x

Substory failure protocol: 'foo', 'bar', 'baz'
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Story and substory failure protocols has incompatible types:

Story method: J.a

Story failure protocol: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Substory method: T.x

Substory failure protocol: 'foo', 'bar', 'baz'
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a
    assert str(exc_info.value) == expected


def test_composition_type_error_enum_with_list():
    """We can't combine different types of stories and substories."""

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    class Q(f.ParentWithList, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Story and substory failure protocols has incompatible types:

Story method: Q.a

Story failure protocol: 'foo', 'bar', 'baz'

Substory method: Q.x

Substory failure protocol: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Story and substory failure protocols has incompatible types:

Story method: J.a

Story failure protocol: 'foo', 'bar', 'baz'

Substory method: T.x

Substory failure protocol: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a
    assert str(exc_info.value) == expected


def test_deny_substory_reason_parent_story_protocol_with_list():
    """
    We deny to use Failure reason from the parent story protocol in
    the substory method.
    """

    class T(f.ChildWithNull, f.StringMethod):
        pass

    class Q(f.ParentWithList, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Failure('foo') can not be used in a story without failure protocol.

Function returned value: Q.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert Q().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure('foo') can not be used in a story without failure protocol.

Function returned value: T.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_deny_substory_reason_parent_story_protocol_with_enum():
    """
    We deny to use Failure reason from the parent story protocol in
    the substory method.
    """

    class T(f.ChildWithNull, f.EnumMethod):
        pass

    class Q(f.ParentWithEnum, f.NormalParentMethod, T):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Failure(<Errors.foo: 1>) can not be used in a story without failure protocol.

Function returned value: Q.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure(<Errors.foo: 1>) can not be used in a story without failure protocol.

Function returned value: T.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_deny_story_reason_substory_protocol_with_list():
    """
    We deny to use Failure reason from the substory protocol in the
    parent story method.
    """

    class T(f.ChildWithList, f.NormalMethod):
        pass

    class Q(f.ParentWithNull, f.StringParentMethod, T):
        pass

    class J(f.ParentWithNull, f.StringParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Failure('foo') can not be used in a story without failure protocol.

Function returned value: Q.before

Use 'failures' story method to define failure protocol.
    """.strip()

    assert Q().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure('foo') can not be used in a story without failure protocol.

Function returned value: J.before

Use 'failures' story method to define failure protocol.
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


def test_deny_story_reason_substory_protocol_with_enum():
    """
    We deny to use Failure reason from the substory protocol in the
    parent story method.
    """

    class T(f.ChildWithEnum, f.NormalMethod):
        pass

    class Q(f.ParentWithNull, f.EnumParentMethod, T):
        pass

    class J(f.ParentWithNull, f.EnumParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Failure(<Errors.foo: 1>) can not be used in a story without failure protocol.

Function returned value: Q.before

Use 'failures' story method to define failure protocol.
    """.strip()

    assert isinstance(Q().a.failures, enum.EnumMeta)
    assert set(Q().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        Q().a.run()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure(<Errors.foo: 1>) can not be used in a story without failure protocol.

Function returned value: J.before

Use 'failures' story method to define failure protocol.
    """.strip()

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected
