import pytest
from stories import Failure, Result, Success, argument, story


class Empty:

    @story
    def x(self):
        pass


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


class My1:

    def __init__(self, f):

        self.f = f

    @story
    @argument("a")
    def x(self):
        self.one()

    def one(self):

        if self.f(self.ctx.a):
            return Result(2)

        return Failure()


class My2:

    @story
    @argument("a")
    def x(self):
        self.one()

    def one(self):

        return Success(a=2)


class My3:

    @story
    def x(self):
        self.one()

    def one(self):
        return 1


class My4:
    clsattr = 1

    @story
    def x(self):
        self.one()

    def one(self):
        if self.clsattr == 1:
            return Result(True)

        return Failure()


# Substories.
#
# TODO: Test substory attribute access.
#
# TODO: Test substory attribute wrapping.
#
# TODO: Test all subproxy asserts.
#
# TODO: Test subsubstories.


class My5:

    @story
    def x(self):
        self.one()
        self.two()
        self.four()

    @story
    @argument("a")
    def y(self):
        self.three()

    def one(self):
        return Success(a=1)

    def two(self):
        return self.y()

    def three(self):
        if self.ctx.a != 1:
            return Failure()

        return Success(b=2)

    def four(self):
        if self.ctx.b != 2:
            return Failure()

        return Result(True)


# Tests.


def test_empty():

    result = Empty().x()
    assert result is None


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


def test_injectable():

    def foo(arg):
        assert arg == 1
        return True

    result = My1(f=foo).x(a=1)
    assert result == 2


def test_immutable_context():

    with pytest.raises(AssertionError):
        My2().x(a=1)


def test_assertion_result():

    with pytest.raises(AssertionError):
        My3().x()


def test_class_attribute_access():

    result = My4().x()
    assert result is True


def test_substory():

    result = My5().x()
    assert result is True
