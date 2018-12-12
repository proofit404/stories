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
        exc_info.value.reason
        is examples.failure_reasons.SimpleWithEnum().x.failures.foo
    )
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = examples.failure_reasons.SimpleWithEnum().x.run()
    assert not result.is_success
    assert result.is_failure
    assert (
        result.failure_reason
        is examples.failure_reasons.SimpleWithEnum().x.failures.foo
    )
    assert result.failed_because(
        examples.failure_reasons.SimpleWithEnum().x.failures.foo
    )

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleSubstoryWithEnum().a()
    assert (
        exc_info.value.reason
        is examples.failure_reasons.SimpleSubstoryWithEnum().a.failures.foo
    )
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = examples.failure_reasons.SimpleSubstoryWithEnum().a.run()
    assert not result.is_success
    assert result.is_failure
    assert (
        result.failure_reason
        is examples.failure_reasons.SimpleSubstoryWithEnum().a.failures.foo
    )
    assert result.failed_because(
        examples.failure_reasons.SimpleSubstoryWithEnum().a.failures.foo
    )

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SubstoryDIWithEnum().a()
    assert (
        exc_info.value.reason
        is examples.failure_reasons.SubstoryDIWithEnum().a.failures.foo
    )
    assert repr(exc_info.value) == "FailureError(<Errors.foo: 1>)"

    result = examples.failure_reasons.SubstoryDIWithEnum().a.run()
    assert not result.is_success
    assert result.is_failure
    assert (
        result.failure_reason
        is examples.failure_reasons.SubstoryDIWithEnum().a.failures.foo
    )
    assert result.failed_because(
        examples.failure_reasons.SubstoryDIWithEnum().a.failures.foo
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

Use 'failures' story method to define failure protocol.
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

Use 'failures' story method to define failure protocol.
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

Use 'failures' story method to define failure protocol.
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSubstoryDI().b()
    assert str(exc_info.value) == expected

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ReasonWithSubstoryDI().b.run()
    assert str(exc_info.value) == expected


def test_summary_wrong_reason_with_list():
    """
    Summary classes should verify failure reason passed to the
    `failed_because` method.
    """

    # TODO: Check success summary the same way.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: 'foo', 'bar', 'baz'

Story returned result: SimpleWithList.x
""".strip()

    result = examples.failure_reasons.SimpleWithList().x.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: 'foo', 'bar', 'baz'

Story returned result: SimpleSubstoryWithList.a
""".strip()

    result = examples.failure_reasons.SimpleSubstoryWithList().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: 'foo', 'bar', 'baz'

Story returned result: SubstoryDIWithList.a
""".strip()

    result = examples.failure_reasons.SubstoryDIWithList().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


def test_summary_wrong_reason_with_enum():
    """
    Summary classes should verify failure reason passed to the
    `failed_because` method.
    """

    # TODO: Check success summary the same way.

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Story returned result: SimpleWithEnum.x
""".strip()

    result = examples.failure_reasons.SimpleWithEnum().x.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Story returned result: SimpleSubstoryWithEnum.a
""".strip()

    result = examples.failure_reasons.SimpleSubstoryWithEnum().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    expected = """
'failed_because' method got argument mismatching failure protocol: "'foo' is too big"

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>

Story returned result: SubstoryDIWithEnum.a
""".strip()

    result = examples.failure_reasons.SubstoryDIWithEnum().a.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


def test_summary_reason_without_protocol():
    """
    Summary classes should deny to use `failed_because` method on
    stories defined without failure protocol.
    """

    # TODO: Check success summary the same way.

    expected = """
'failed_because' method can not be used with story defined without failure protocol.

Story returned result: SummaryWithSimple.z

Use 'failures' story method to define failure protocol.
""".strip()

    result = examples.failure_reasons.SummaryWithSimple().z.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    expected = """
'failed_because' method can not be used with story defined without failure protocol.

Story returned result: SummaryWithSimpleSubstory.c

Use 'failures' story method to define failure protocol.
""".strip()

    result = examples.failure_reasons.SummaryWithSimpleSubstory().c.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected

    expected = """
'failed_because' method can not be used with story defined without failure protocol.

Story returned result: SummaryWithSubstoryDI.c

Use 'failures' story method to define failure protocol.
""".strip()

    result = examples.failure_reasons.SummaryWithSubstoryDI().c.run()

    with pytest.raises(FailureProtocolError) as exc_info:
        result.failed_because("'foo' is too big")
    assert str(exc_info.value) == expected


def test_substory_protocol_match_with_empty():
    """
    We should allow to use stories composition, if parent story and
    substory does not define failure protocols.
    """

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.EmptySubstoryMatch().a()
    assert exc_info.value.reason is None

    result = examples.failure_reasons.EmptySubstoryMatch().a.run()
    assert result.failure_reason is None

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.EmptyDIMatch().a()
    assert exc_info.value.reason is None

    result = examples.failure_reasons.EmptyDIMatch().a.run()
    assert result.failure_reason is None


def test_substory_protocol_match_with_list():
    """
    We should allow to use stories composition, if parent story
    protocol is a superset of the substory protocol.
    """

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleSubstoryMatchWithList().a()
    assert exc_info.value.reason == "foo"

    result = examples.failure_reasons.SimpleSubstoryMatchWithList().a.run()
    assert result.failed_because("foo")

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SubstoryDIMatchWithList().a()
    assert exc_info.value.reason == "foo"

    result = examples.failure_reasons.SubstoryDIMatchWithList().a.run()
    assert result.failed_because("foo")


def test_substory_protocol_match_with_enum():
    """
    We should allow to use stories composition, if parent story
    protocol is a superset of the substory protocol.
    """

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SimpleSubstoryMatchWithEnum().a()
    assert (
        exc_info.value.reason
        is examples.failure_reasons.SimpleSubstoryMatchWithEnum().a.failures.foo
    )

    result = examples.failure_reasons.SimpleSubstoryMatchWithEnum().a.run()
    assert result.failed_because(
        examples.failure_reasons.SimpleSubstoryMatchWithEnum().a.failures.foo
    )

    with pytest.raises(FailureError) as exc_info:
        examples.failure_reasons.SubstoryDIMatchWithEnum().a()
    assert (
        exc_info.value.reason
        is examples.failure_reasons.SubstoryDIMatchWithEnum().a.failures.foo
    )

    result = examples.failure_reasons.SubstoryDIMatchWithEnum().a.run()
    assert result.failed_because(
        examples.failure_reasons.SubstoryDIMatchWithEnum().a.failures.foo
    )


def test_substory_protocol_mismatch_with_empty():
    """
    We should deny to use stories composition, if parent story define failure
    protocol and substory doesn't.
    """

    expected = """
Story and substory failure protocol mismatch.

Story: EmptySubstoryMismatch.a

Available failures are: 'foo', 'quiz'

Substory: EmptySubstoryMismatch.x

Available failures are: None
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.EmptySubstoryMismatch().a()
    assert str(exc_info.value) == expected

    expected = """
Story and substory failure protocol mismatch.

Story: EmptyParentMismatch.a

Available failures are: None

Substory: EmptyParentMismatch.x

Available failures are: 'foo', 'quiz'
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.EmptyParentMismatch().a()
    assert str(exc_info.value) == expected

    expected = """
Story and substory failure protocol mismatch.

Story: EmptyDIMismatch.a

Available failures are: 'foo', 'quiz'

Substory: EmptyMismatch.x

Available failures are: None
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.EmptyDIMismatch().a()
    assert str(exc_info.value) == expected

    expected = """
Story and substory failure protocol mismatch.

Story: ParentDIMismatch.a

Available failures are: None

Substory: ParentMismatch.x

Available failures are: 'foo', 'quiz'
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.ParentDIMismatch().a()
    assert str(exc_info.value) == expected


def test_substory_protocol_mismatch_with_list():
    """
    We should deny to use stories composition, if parent story
    protocol isn't a superset of the substory protocol.
    """

    expected = """
Story and substory failure protocol mismatch.

Story: SimpleSubstoryMismatchWithList.a

Available failures are: 'foo', 'quiz'

Substory: SimpleSubstoryMismatchWithList.x

Available failures are: 'foo', 'bar', 'baz'
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryMismatchWithList().a()
    assert str(exc_info.value) == expected

    expected = """
Story and substory failure protocol mismatch.

Story: SubstoryDIMismatchWithList.a

Available failures are: 'foo', 'quiz'

Substory: SimpleMismatchWithList.x

Available failures are: 'foo', 'bar', 'baz'
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIMismatchWithList().a()
    assert str(exc_info.value) == expected


def test_substory_protocol_mismatch_with_enum():
    """
    We should deny to use stories composition, if parent story
    protocol isn't a superset of the substory protocol.
    """

    expected = """
Story and substory failure protocol mismatch.

Story: SimpleSubstoryMismatchWithEnum.a

Available failures are: <Errors.foo: 1>, <Errors.quiz: 2>

Substory: SimpleSubstoryMismatchWithEnum.x

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SimpleSubstoryMismatchWithEnum().a()
    assert str(exc_info.value) == expected

    expected = """
Story and substory failure protocol mismatch.

Story: SubstoryDIMismatchWithEnum.a

Available failures are: <Errors.foo: 1>, <Errors.quiz: 2>

Substory: SimpleMismatchWithEnum.x

Available failures are: <Errors.foo: 1>, <Errors.bar: 2>, <Errors.baz: 3>
""".strip()

    with pytest.raises(FailureProtocolError) as exc_info:
        examples.failure_reasons.SubstoryDIMismatchWithEnum().a()
    assert str(exc_info.value) == expected
