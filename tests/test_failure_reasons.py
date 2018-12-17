import enum

import pytest

import examples.failure_reasons as f
from stories.exceptions import FailureError, FailureProtocolError


# Arguments of the Failure class.


def test_reasons_defined_with_list():
    """We can use list of strings to define story failure protocol."""

    # Simple.

    class T(f.ChildWithList, f.StringMethod):
        pass

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

    class Q(f.ParentWithList, f.ParentMethod, T):
        pass

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

    class J(f.ParentWithList, f.ParentMethod):
        def __init__(self):
            self.x = T().x

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

    # Simple.

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

    with pytest.raises(FailureError) as exc_info:
        T().x()
    assert exc_info.value.reason is T().x.failures.foo
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = T().x.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason is T().x.failures.foo
    assert result.failed_because(T().x.failures.foo)

    # Substory inheritance.

    class Q(f.ParentWithEnum, f.ParentMethod, T):
        pass

    with pytest.raises(FailureError) as exc_info:
        Q().a()
    assert exc_info.value.reason is Q().a.failures.foo
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = Q().a.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason is Q().a.failures.foo
    assert result.failed_because(Q().a.failures.foo)

    # Substory DI.

    class J(f.ParentWithEnum, f.ParentMethod):
        def __init__(self):
            self.x = T().x

    with pytest.raises(FailureError) as exc_info:
        J().a()
    assert exc_info.value.reason is J().a.failures.foo
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = J().a.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason is J().a.failures.foo
    assert result.failed_because(J().a.failures.foo)


def test_wrong_reason_with_list():
    """
    We deny to use wrong reason in stories defined with list of
    strings as its failure protocol.
    """

    # Simple.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: T.one
    """.strip()

    class T(f.ChildWithList, f.WrongMethod):
        pass

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

    class Q(f.ParentWithList, f.ParentMethod, T):
        pass

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

    class J(f.ParentWithList, f.ParentMethod):
        def __init__(self):
            self.x = T().x

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

    # Simple.

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: T.one
    """.strip()

    class T(f.ChildWithEnum, f.WrongMethod):
        pass

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

    class Q(f.ParentWithEnum, f.ParentMethod, T):
        pass

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

    class J(f.ParentWithEnum, f.ParentMethod):
        def __init__(self):
            self.x = T().x

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

    # Simple.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: T.one

Use one of them as Failure() argument.
    """.strip()

    class T(f.ChildWithList, f.NullMethod):
        pass

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

    class Q(f.ParentWithList, f.ParentMethod, T):
        pass

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

    class J(f.ParentWithList, f.ParentMethod):
        def __init__(self):
            self.x = T().x

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

    # Simple.

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: T.one

Use one of them as Failure() argument.
    """.strip()

    class T(f.ChildWithEnum, f.NullMethod):
        pass

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

    class Q(f.ParentWithEnum, f.ParentMethod, T):
        pass

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

    class J(f.ParentWithEnum, f.ParentMethod):
        def __init__(self):
            self.x = T().x

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

    # Simple.

    expected = """
Failure("'foo' is too big") can not be used in a story without failure protocol.

Function returned value: T.one

Use 'failures' story method to define failure protocol.
""".strip()

    class T(f.ChildWithNull, f.WrongMethod):
        pass

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

    class Q(f.ParentWithNull, f.ParentMethod, T):
        pass

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

    class J(f.ParentWithNull, f.ParentMethod):
        def __init__(self):
            self.x = T().x

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        J().a.run()
    assert str(exc_info.value) == expected


# Arguments of the result class methods.


def test_summary_wrong_reason_with_list():
    """
    Summary classes should verify failure reason passed to the
    `failed_because` method.
    """

    # TODO: Check success summary the same way.

    # Simple.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: 'foo', 'bar', 'baz'

Story returned result: T.x
""".strip()

    class T(f.ChildWithList, f.StringMethod):
        pass

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

    class Q(f.ParentWithList, f.ParentMethod, T):
        pass

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

    class J(f.ParentWithList, f.ParentMethod):
        def __init__(self):
            self.x = T().x

    result = J().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


def test_summary_wrong_reason_with_enum():
    """
    Summary classes should verify failure reason passed to the
    `failed_because` method.
    """

    # TODO: Check success summary the same way.

    # Simple.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Story returned result: T.x
""".strip()

    class T(f.ChildWithEnum, f.EnumMethod):
        pass

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

    class Q(f.ParentWithEnum, f.ParentMethod, T):
        pass

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

    class J(f.ParentWithEnum, f.ParentMethod):
        def __init__(self):
            self.x = T().x

    result = J().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


def test_summary_reason_without_protocol():
    """
    Summary classes should deny to use `failed_because` method on
    stories defined without failure protocol.
    """

    # TODO: Check success summary the same way.

    # Simple.

    expected = """
'failed_because' method can not be used with story defined without failure protocol.

Story returned result: T.x

Use 'failures' story method to define failure protocol.
""".strip()

    class T(f.ChildWithNull, f.NullMethod):
        pass

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

    class Q(f.ParentWithNull, f.ParentMethod, T):
        pass

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

    class J(f.ParentWithNull, f.ParentMethod):
        def __init__(self):
            self.x = T().x

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

    class Q(f.ParentWithNull, f.ParentMethod, T):
        pass

    class J(f.ParentWithNull, f.ParentMethod):
        def __init__(self):
            self.x = T().x

    with pytest.raises(FailureError) as exc_info:
        Q().a()
    assert exc_info.value.reason is None

    result = Q().a.run()
    assert result.failure_reason is None

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

    class Q(f.WideParentWithList, f.ParentMethod, T):
        pass

    class J(f.WideParentWithList, f.ParentMethod):
        def __init__(self):
            self.x = T().x

    with pytest.raises(FailureError) as exc_info:
        Q().a()
    assert exc_info.value.reason == "foo"

    result = Q().a.run()
    assert result.failed_because("foo")

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

    class Q(f.WideParentWithEnum, f.ParentMethod, T):
        pass

    class J(f.WideParentWithEnum, f.ParentMethod):
        def __init__(self):
            self.x = T().x

    with pytest.raises(FailureError) as exc_info:
        Q().a()
    assert exc_info.value.reason is Q().a.failures.foo

    result = Q().a.run()
    assert result.failed_because(Q().a.failures.foo)

    with pytest.raises(FailureError) as exc_info:
        J().a()
    assert exc_info.value.reason is J().a.failures.foo

    result = J().a.run()
    assert result.failed_because(J().a.failures.foo)


def test_expand_substory_protocol_empty():
    """
    We expand protocol of composed story if substory does not define
    any protocol.
    """


def test_expand_substory_protocol_list():
    """
    We expand protocol of composed story if substory define protocol
    with list of strings.
    """

    class T(f.ChildWithNull, f.NormalMethod):
        pass

    class Q(f.ParentWithList, f.ParentMethod, T):
        pass

    class J(f.ParentWithList, f.ParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    Q().a.failures == ["foo", "bar", "baz"]

    result = Q().a()
    assert result is None

    result = Q().a.run()
    assert result.is_success
    assert result.value is None

    # Substory DI.

    J().a.failures == ["foo", "bar", "baz"]

    result = J().a()
    assert result is None

    result = J().a.run()
    assert result.is_success
    assert result.value is None


def test_expand_substory_protocol_enum():
    """
    We expand protocol of composed story if substory define protocol
    with enum class.
    """

    class T(f.ChildWithNull, f.NormalMethod):
        pass

    class Q(f.ParentWithEnum, f.ParentMethod, T):
        pass

    class J(f.ParentWithEnum, f.ParentMethod):
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
