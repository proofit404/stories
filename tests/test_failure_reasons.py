import pytest

import examples
from stories.exceptions import FailureError, FailureProtocolError


def test_reasons_defined_with_list():
    """We can use list of strings to define story failure protocol."""

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleWithList().x()
    assert exc_info.value.reason == "foo"
    assert repr(exc_info.value) == "FailureError('foo')"

    result = examples.failure_reasons.SimpleWithList().x.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason == "foo"
    assert result.failed_because("foo")

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithList().a()
    assert exc_info.value.reason == "foo"
    assert repr(exc_info.value) == "FailureError('foo')"

    result = examples.failure_reasons.SimpleSubstoryWithList().a.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason == "foo"
    assert result.failed_because("foo")

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SubstoryDIWithList().a()
    assert exc_info.value.reason == "foo"
    assert repr(exc_info.value) == "FailureError('foo')"

    result = examples.failure_reasons.SubstoryDIWithList().a.run()
    assert not result.is_success
    assert result.is_failure
    assert result.failure_reason == "foo"
    assert result.failed_because("foo")


def test_reasons_defined_with_enum():
    """We can use enum class to define story failure protocol."""

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().x()
    assert (
        exc_info.value.reason is examples.failure_reasons.SimpleWithEnum.x.failures.foo
    )
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = examples.failure_reasons.SimpleWithEnum().x.run()
    assert not result.is_success
    assert result.is_failure
    assert (
        result.failure_reason is examples.failure_reasons.SimpleWithEnum.x.failures.foo
    )
    assert result.failed_because(examples.failure_reasons.SimpleWithEnum.x.failures.foo)

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithEnum().a()
    assert (
        exc_info.value.reason
        is examples.failure_reasons.SimpleSubstoryWithEnum.a.failures.foo
    )
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = examples.failure_reasons.SimpleSubstoryWithEnum().a.run()
    assert not result.is_success
    assert result.is_failure
    assert (
        result.failure_reason
        is examples.failure_reasons.SimpleSubstoryWithEnum.a.failures.foo
    )
    assert result.failed_because(
        examples.failure_reasons.SimpleSubstoryWithEnum.a.failures.foo
    )

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SubstoryDIWithEnum().a()
    assert (
        exc_info.value.reason
        is examples.failure_reasons.SubstoryDIWithEnum.a.failures.foo
    )
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = examples.failure_reasons.SubstoryDIWithEnum().a.run()
    assert not result.is_success
    assert result.is_failure
    assert (
        result.failure_reason
        is examples.failure_reasons.SubstoryDIWithEnum.a.failures.foo
    )
    assert result.failed_because(
        examples.failure_reasons.SubstoryDIWithEnum.a.failures.foo
    )


def test_wrong_reason_with_list():
    """
    We deny to use wrong reason in stories defined with list of
    strings as its failure protocol.
    """

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleWithList.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().y()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().y.run()
    assert str(exc_info.value) == expected

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleSubstoryWithList.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithList().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithList().b.run()
    assert str(exc_info.value) == expected

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleWithList.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithList().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithList().b.run()
    assert str(exc_info.value) == expected


def test_wrong_reason_with_enum():
    """
    We deny to use wrong reason in stories defined with enum class as
    its failure protocol.
    """

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleWithEnum.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().y()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().y.run()
    assert str(exc_info.value) == expected

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleSubstoryWithEnum.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithEnum().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithEnum().b.run()
    assert str(exc_info.value) == expected

    expected = """
Failure("'foo' is too big") failure reason is not allowed by current protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleWithEnum.two
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithEnum().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithEnum().b.run()
    assert str(exc_info.value) == expected


def test_null_reason_with_list():
    """
    We deny to use Failure() in stories defined with list of strings
    as its failure protocol.
    """

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleWithList.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().z()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithList().z.run()
    assert str(exc_info.value) == expected

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleSubstoryWithList.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithList().c()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithList().c.run()
    assert str(exc_info.value) == expected

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: 'foo', 'bar', 'baz'

Function returned value: SimpleWithList.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithList().c()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithList().c.run()
    assert str(exc_info.value) == expected


def test_null_reason_with_enum():
    """
    We deny to use Failure() in stories defined with enum class as its
    failure protocol.
    """

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleWithEnum.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().z()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleWithEnum().z.run()
    assert str(exc_info.value) == expected

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleSubstoryWithEnum.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithEnum().c()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithEnum().c.run()
    assert str(exc_info.value) == expected

    expected = """
Failure() can not be used in a story with failure protocol.

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Function returned value: SimpleWithEnum.three

Use one of them as Failure() argument.
    """.strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithEnum().c()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIWithEnum().c.run()
    assert str(exc_info.value) == expected


def test_reason_without_protocol():
    """
    We deny to use Failure('reason') in stories defined without
    failure protocol.
    """

    expected = """
Failure("'foo' is too big") can not be used in a story without failure protocol.

Function returned value: ReasonWithSimple.two

Use StoryFactory to define failure protocol.
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSimple().y()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSimple().y.run()
    assert str(exc_info.value) == expected

    expected = """
Failure("'foo' is too big") can not be used in a story without failure protocol.

Function returned value: ReasonWithSimpleSubstory.two

Use StoryFactory to define failure protocol.
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSimpleSubstory().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSimpleSubstory().b.run()
    assert str(exc_info.value) == expected

    expected = """
Failure("'foo' is too big") can not be used in a story without failure protocol.

Function returned value: ReasonWithSimple.two

Use StoryFactory to define failure protocol.
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSubstoryDI().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSubstoryDI().b.run()
    assert str(exc_info.value) == expected
