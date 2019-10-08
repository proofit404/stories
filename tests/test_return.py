import examples
from stories import Failure
from stories import Result
from stories import Skip
from stories import Success


def test_result_representation():

    result = Result(1)
    assert repr(result) == "Result(1)"


def test_success_representation():

    success = Success(foo="bar", baz=2)
    assert repr(success) in {"Success(foo='bar', baz=2)", "Success(baz=2, foo='bar')"}


def test_failure_representation():

    failure = Failure()
    assert repr(failure) == "Failure()"

    failure = Failure("test")
    assert repr(failure) == "Failure('test')"


def test_skip_representation():

    skip = Skip()
    assert repr(skip) == "Skip()"


def test_failure_summary_representation():

    expected = "Failure()"
    result = examples.methods.Simple().x.run(foo=2, bar=2)
    assert repr(result) == expected


def test_success_summary_representation():

    expected = "Success()"
    result = examples.methods.Simple().x.run(foo=1, bar=3)
    assert repr(result) == expected
