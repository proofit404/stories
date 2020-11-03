from stories import Failure
from stories import Next
from stories import Result
from stories import Success


def test_result_representation():

    marker = Result()
    assert repr(marker) == "Result()"

    marker = Result(1)
    assert repr(marker) == "Result(1)"


def test_failure_representation():

    marker = Failure()
    assert repr(marker) == "Failure()"

    marker = Failure("test")
    assert repr(marker) == "Failure('test')"


def test_success_representation():

    success = Success()
    assert repr(success) == "Success()"


def test_next_representation():

    marker = Next()
    assert repr(marker) == "Next()"

    marker = Next(1)
    assert repr(marker) == "Next(1)"


def test_failure_summary_representation(r, x):

    marker = r(x.Simple().x.run)(foo=2, bar=2)
    assert repr(marker) == "Failure()"


def test_success_summary_representation(r, x):

    marker = r(x.Simple().x.run)(foo=1, bar=3)
    assert repr(marker) == "Success()"
