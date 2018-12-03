import pytest

import examples
from stories.exceptions import FailureError


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
