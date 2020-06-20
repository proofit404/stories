# -*- coding: utf-8 -*-
import enum

import pytest

from stories import story
from stories.exceptions import FailureError
from stories.exceptions import FailureProtocolError


# Story definition.


def test_wrong_definition():
    """We check types used in failures definition."""

    class T(object):
        @story
        def x(I):
            I.one

    expected = "Unexpected type for story failure protocol: 'boom'"

    with pytest.raises(FailureProtocolError) as exc_info:
        T.x.failures("boom")
    assert str(exc_info.value) == expected

    expected = "Unexpected type for story failure protocol: ['foo', 'bar', None]"

    with pytest.raises(FailureProtocolError) as exc_info:
        T.x.failures(["foo", "bar", None])
    assert str(exc_info.value) == expected


# Arguments of the Failure class.


def test_reasons_defined_with_list(r, f):
    """We can use list of strings to define story failure protocol."""

    class T(f.ChildWithList, f.StringMethod):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    assert T().x.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureError) as exc_info:
        r(T().x)()
    assert repr(exc_info.value) == "FailureError('foo')"

    result = r(T().x.run)()
    assert not result.is_success
    assert result.is_failure
    assert result.failed_because("foo")

    # Substory DI.

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureError) as exc_info:
        r(J().a)()
    assert repr(exc_info.value) == "FailureError('foo')"

    result = r(J().a.run)()
    assert not result.is_success
    assert result.is_failure
    assert result.failed_because("foo")


def test_reasons_defined_with_enum(r, f):
    """We can use enum class to define story failure protocol."""

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    assert isinstance(T().x.failures, enum.EnumMeta)
    assert set(T().x.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureError) as exc_info:
        r(T().x)()
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = r(T().x.run)()
    assert not result.is_success
    assert result.is_failure
    assert result.failed_because(T().x.failures.foo)

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureError) as exc_info:
        r(J().a)()
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = r(J().a.run)()
    assert not result.is_success
    assert result.is_failure
    assert result.failed_because(J().a.failures.foo)


def test_wrong_reason_with_list(r, f):
    """We deny to use wrong reason in stories defined with list of strings as its
    failure protocol."""

    class T(f.ChildWithList, f.WrongMethod):
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
        r(T().x)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(T().x.run)()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: T.one
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_wrong_reason_with_enum(r, f):
    """We deny to use wrong reason in stories defined with enum class as its failure
    protocol."""

    class T(f.ChildWithEnum, f.WrongMethod):
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
        r(T().x)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(T().x.run)()
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
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_null_reason_with_list(r, f):
    """We deny to use Failure() in stories defined with list of strings as its failure
    protocol."""

    class T(f.ChildWithList, f.NullMethod):
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
        r(T().x)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(T().x.run)()
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
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_null_reason_with_enum(r, f):
    """We deny to use Failure() in stories defined with enum class as its failure
    protocol."""

    class T(f.ChildWithEnum, f.NullMethod):
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
        r(T().x)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(T().x.run)()
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
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_reason_without_protocol(r, f):
    """We deny to use Failure('reason') in stories defined without failure protocol."""

    class T(f.ChildWithNull, f.WrongMethod):
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
        r(T().x)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(T().x.run)()
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Failure("'foo' is too big") can not be used in a story without failure protocol.

Function returned value: T.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert J().a.failures is None

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


# Arguments of the result class methods.


@pytest.mark.parametrize("method", ["NormalMethod", "StringMethod"])
def test_summary_wrong_reason_with_list(r, f, method):
    """Summary classes should verify failure reason passed to the `failed_because`
    method."""

    class T(f.ChildWithList, getattr(f, method)):
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

    result = r(T().x.run)()

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

    result = r(J().a.run)()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


@pytest.mark.parametrize("method", ["NormalMethod", "EnumMethod"])
def test_summary_wrong_reason_with_enum(r, f, method):
    """Summary classes should verify failure reason passed to the `failed_because`
    method."""

    class T(f.ChildWithEnum, getattr(f, method)):
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

    result = r(T().x.run)()

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

    result = r(J().a.run)()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


@pytest.mark.parametrize("method", ["NormalMethod", "NullMethod"])
def test_summary_reason_without_protocol(r, f, method):
    """Summary classes should deny to use `failed_because` method on stories defined
    without failure protocol."""

    class T(f.ChildWithNull, getattr(f, method)):
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

    result = r(T().x.run)()

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

    result = r(J().a.run)()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


def test_use_expanded_protocol_in_summary_result_with_list(r, f):
    """We should allow to use `failed_because` method with expanded protocol."""

    class T(f.ChildWithList, f.NormalMethod):
        pass

    class J(f.ShrinkParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    result = r(J().a.run)()
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_because("foo")
    assert not result.failed_because("bar")
    assert not result.failed_because("baz")
    assert not result.failed_because("quiz")


def test_use_expanded_protocol_in_summary_result_with_enum(r, f):
    """We should allow to use `failed_because` method with expanded protocol."""

    class T(f.ChildWithEnum, f.NormalMethod):
        pass

    class J(f.ShrinkParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    result = r(J().a.run)()
    assert result.is_success
    assert not result.is_failure
    assert not result.failed_because(J().a.failures.foo)
    assert not result.failed_because(J().a.failures.bar)
    assert not result.failed_because(J().a.failures.baz)
    assert not result.failed_because(J().a.failures.quiz)


# Composition of the stories.


def test_substory_protocol_match_with_empty(r, f):
    """We should allow to use stories composition, if parent story and substory does not
    define failure protocols."""

    class T(f.ChildWithNull, f.NullMethod):
        pass

    class J(f.ParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    J().a.failures is None

    with pytest.raises(FailureError) as exc_info:
        r(J().a)()
    assert repr(exc_info.value) == "FailureError()"

    result = r(J().a.run)()
    assert result.is_failure


def test_substory_protocol_match_with_list(r, f):
    """We should allow to use stories composition, if parent story protocol is a
    superset of the substory protocol."""

    class T(f.ChildWithList, f.StringMethod):
        pass

    class J(f.WideParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    assert J().a.failures == ["foo", "bar", "baz", "quiz"]

    with pytest.raises(FailureError) as exc_info:
        r(J().a)()
    assert repr(exc_info.value) == "FailureError('foo')"

    result = r(J().a.run)()
    assert result.failed_because("foo")


def test_substory_protocol_match_with_enum(r, f):
    """We should allow to use stories composition, if parent story protocol is a
    superset of the substory protocol."""

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    class J(f.WideParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz", "quiz"}

    with pytest.raises(FailureError) as exc_info:
        r(J().a)()
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = r(J().a.run)()
    assert result.failed_because(J().a.failures.foo)


def test_expand_substory_protocol_null_with_list(r, f):
    """We expand protocol of composed story, if substory does not define failure
    protocols and parent story define protocol with list of strings."""

    class T(f.ChildWithNull, f.NormalMethod):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    assert J().a.failures == ["foo", "bar", "baz"]

    result = r(J().a)()
    assert result is None

    result = r(J().a.run)()
    assert result.is_success
    assert result.value is None


def test_expand_substory_protocol_null_with_enum(r, f):
    """We expand protocol of composed story, if substory does not define protocol and
    parent story define protocol with enum class."""

    class T(f.ChildWithNull, f.NormalMethod):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    result = r(J().a)()
    assert result is None

    result = r(J().a.run)()
    assert result.is_success
    assert result.value is None


def test_deny_failure_substory_without_protocol_story_protocol_with_list(r, f):
    """Substory defined without failure protocol can not return Failure, if this
    substory was composed with parent story defined with list of strings as failure
    protocol."""

    class T(f.ChildWithNull, f.NullMethod):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    expected = """
Failure() can not be used in a story composition.

Different types of failure protocol were used in parent and substory definitions.

Function returned value: T.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_deny_failure_substory_without_protocol_story_protocol_with_enum(r, f):
    """Substory defined without failure protocol can not return Failure, if this
    substory was composed with parent story defined with enum as failure protocol."""

    class T(f.ChildWithNull, f.NullMethod):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

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
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_deny_failure_story_without_protocol_substory_protocol_with_list(r, f):
    """Story defined without failure protocol can not return Failure, if this story was
    composed with substory defined with list of strings as failure protocol."""

    class T(f.ChildWithList, f.NormalMethod):
        pass

    class J(f.ParentWithNull, f.NullParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    expected = """
Failure() can not be used in a story composition.

Different types of failure protocol were used in parent and substory definitions.

Function returned value: J.before

Use 'failures' story method to define failure protocol.
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_deny_failure_story_without_protocol_substory_protocol_with_enum(r, f):
    """Story defined without failure protocol can not return Failure, if this story was
    composed with substory defined with enum as failure protocol."""

    class T(f.ChildWithEnum, f.NormalMethod):
        pass

    class J(f.ParentWithNull, f.NullParentMethod):
        def __init__(self):
            self.x = T().x

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
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_expand_substory_protocol_list_with_null(r, f):
    """We expand protocol of composed story, if substory define protocol with list of
    strings and parent story does not define protocol."""

    class T(f.ChildWithList, f.NormalMethod):
        pass

    class J(f.ParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    assert J().a.failures == ["foo", "bar", "baz"]

    result = r(J().a)()
    assert result is None

    result = r(J().a.run)()
    assert result.is_success
    assert result.value is None


def test_expand_substory_protocol_enum_with_null(r, f):
    """We expand protocol of composed story, if substory define protocol with enum class
    and parent story does not define protocol."""

    class T(f.ChildWithEnum, f.NormalMethod):
        pass

    class J(f.ParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    result = r(J().a)()
    assert result is None

    result = r(J().a.run)()
    assert result.is_success
    assert result.value is None


def test_expand_substory_protocol_list_with_list(r, f):
    """We expand protocol of composed story, if substory and parent story define
    protocol with list of strings."""

    class T(f.ChildWithList, f.StringMethod):
        pass

    class J(f.ShrinkParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    assert J().a.failures == ["foo", "quiz", "bar", "baz"]

    with pytest.raises(FailureError) as exc_info:
        r(J().a)()
    assert repr(exc_info.value) == "FailureError('foo')"

    result = r(J().a.run)()
    assert result.failed_because("foo")


def test_expand_substory_protocol_enum_with_enum(r, f):
    """We expand protocol of composed story, if substory and parent story define
    protocol with enum class."""

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    class J(f.ShrinkParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz", "quiz"}

    with pytest.raises(FailureError) as exc_info:
        r(J().a)()
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = r(J().a.run)()
    assert result.failed_because(J().a.failures.foo)


def test_expand_sequential_substory_protocol_list_with_null(r, f):
    """If parent story consist from sequential substories, we should merge their failure
    protocols together."""

    class T(f.ChildWithList, f.StringMethod):
        pass

    class E(f.NextChildWithNull, f.NormalMethod):
        pass

    class J(f.SequenceParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x
            self.y = E().y

    # Substory DI.

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureError) as exc_info:
        r(J().a)()
    assert repr(exc_info.value) == "FailureError('foo')"

    result = r(J().a.run)()
    assert result.failed_because("foo")


def test_expand_sequential_substory_protocol_enum_with_null(r, f):
    """If parent story consist from sequential substories, we should merge their failure
    protocols together."""

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    class E(f.NextChildWithNull, f.NormalMethod):
        pass

    class J(f.SequenceParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x
            self.y = E().y

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureError) as exc_info:
        r(J().a)()
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = r(J().a.run)()
    assert result.failed_because(J().a.failures.foo)


def test_expand_sequential_substory_protocol_list_with_list(r, f):
    """If parent story consist from sequential substories, we should merge their failure
    protocols together."""

    class T(f.ChildWithList, f.StringMethod):
        pass

    class E(f.NextChildWithList, f.StringMethod):
        pass

    class J(f.SequenceParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x
            self.y = E().y

    # Substory DI.

    assert J().a.failures == ["foo", "bar", "baz", "spam", "ham", "eggs"]

    with pytest.raises(FailureError) as exc_info:
        r(J().a)()
    assert repr(exc_info.value) == "FailureError('foo')"

    result = r(J().a.run)()
    assert result.failed_because("foo")


def test_expand_sequential_substory_protocol_enum_with_enum(r, f):
    """If parent story consist from sequential substories, we should merge their failure
    protocols together."""

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    class E(f.NextChildWithEnum, f.EnumMethod):
        pass

    class J(f.SequenceParentWithNull, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x
            self.y = E().y

    # Substory DI.

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {
        "foo",
        "bar",
        "baz",
        "spam",
        "ham",
        "eggs",
    }

    with pytest.raises(FailureError) as exc_info:
        r(J().a)()
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = r(J().a.run)()
    assert result.failed_because(J().a.failures.foo)


def test_composition_type_error_list_with_enum(r, f):
    """We can't combine different types of stories and substories."""

    class T(f.ChildWithList, f.StringMethod):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

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


def test_composition_type_error_enum_with_list(r, f):
    """We can't combine different types of stories and substories."""

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

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


def test_deny_substory_reason_parent_story_protocol_with_list(r, f):
    """We deny to use Failure reason from the parent story protocol in the substory
    method."""

    class T(f.ChildWithNull, f.StringMethod):
        pass

    class J(f.ParentWithList, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    expected = """
Failure('foo') can not be used in a story without failure protocol.

Function returned value: T.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_deny_substory_reason_parent_story_protocol_with_enum(r, f):
    """We deny to use Failure reason from the parent story protocol in the substory
    method."""

    class T(f.ChildWithNull, f.EnumMethod):
        pass

    class J(f.ParentWithEnum, f.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    expected = """
Failure(<Errors.foo: 1>) can not be used in a story without failure protocol.

Function returned value: T.one

Use 'failures' story method to define failure protocol.
    """.strip()

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_deny_story_reason_substory_protocol_with_list(r, f):
    """We deny to use Failure reason from the substory protocol in the parent story
    method."""

    class T(f.ChildWithList, f.NormalMethod):
        pass

    class J(f.ParentWithNull, f.StringParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    expected = """
Failure('foo') can not be used in a story without failure protocol.

Function returned value: J.before

Use 'failures' story method to define failure protocol.
    """.strip()

    assert J().a.failures == ["foo", "bar", "baz"]

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected


def test_deny_story_reason_substory_protocol_with_enum(r, f):
    """We deny to use Failure reason from the substory protocol in the parent story
    method."""

    class T(f.ChildWithEnum, f.NormalMethod):
        pass

    class J(f.ParentWithNull, f.EnumParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory DI.

    expected = """
Failure(<Errors.foo: 1>) can not be used in a story without failure protocol.

Function returned value: J.before

Use 'failures' story method to define failure protocol.
    """.strip()

    assert isinstance(J().a.failures, enum.EnumMeta)
    assert set(J().a.failures.__members__.keys()) == {"foo", "bar", "baz"}

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a)()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        r(J().a.run)()
    assert str(exc_info.value) == expected
