import pytest
from stories import Failure, Result, Success, argument, story


class My:

    @story
    @argument("a")
    @argument("b")
    def x(self):
        self.one()
        self.two()
        self.three()

    def one(self):

        return Success()

    def two(self):

        if self.ctx.a > 1:
            return Failure()

        return Success(c=4)

    def three(self):

        return Result(self.ctx.b - self.ctx.c)


def test_failure():

    result = My().x(2, 2)
    assert isinstance(result, Failure)


def test_success():

    result = My().x(1, 2)
    assert result == -2


def test_success_keywords():

    result = My().x(a=1, b=2)
    assert result == -2


def test_assertion_error():

    with pytest.raises(AssertionError):
        My().x(1)


def test_assertion_error_keywords():

    with pytest.raises(AssertionError):
        My().x(1, b=2)


# TODO: test My().y() without arguments at all.
