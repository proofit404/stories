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


class My6:

    @story
    def x(self):
        self.one()

    @story
    @argument("a")
    def y(self):
        pass

    def one(self):
        return self.y()


class My7:

    @story
    @argument("a")
    def x(self):
        self.one()
        self.three()

    @story
    def y(self):
        self.two()

    def one(self):
        return self.y()

    def two(self):
        if self.ctx.a > 1:
            return Result(True)

        return Failure()

    def three(self):
        raise Exception


class My8:

    def __init__(self, f):
        self.f = f

    @story
    @argument("a")
    def x(self):
        self.one()

    @story
    def y(self):
        self.two()

    def one(self):
        return self.y()

    def two(self):
        if self.f(self.ctx.a):
            return Result(2)

        return Failure()


class My9:
    clsattr = 1

    @story
    def x(self):
        self.one()

    @story
    def y(self):
        self.two()

    def one(self):
        return self.y()

    def two(self):
        if self.clsattr == 1:
            return Result(True)

        return Failure()


class My10:

    @story
    def x(self):
        self.one()
        self.five()

    @story
    def y(self):
        self.two()
        self.four()

    @story
    def z(self):
        self.three()

    def one(self):
        return self.y()

    def two(self):
        return self.z()

    def three(self):
        return Success(a=1)

    def four(self):
        return Success(b=self.ctx.a + 1)

    def five(self):
        return Result(self.ctx.b == 2)


class My11:

    @story
    def x(self):
        self.y()

    @story
    def y(self):
        self.one()
        self.two()

    def one(self):
        return Success(a=True)

    def two(self):
        return Result(self.ctx.a)


class My12:

    def __init__(self, y):
        self.y = y

    @story
    def x(self):
        self.y()
        self.three()

    def three(self):
        return Result(self.ctx.b + 1)


class My13:

    def __init__(self, z):

        self.z = z

    @story
    def y(self):
        self.z()
        self.two()

    def two(self):
        return Success(b=self.ctx.a + 1)


class My14:

    @story
    def z(self):
        self.one()

    def one(self):
        return Success(a=1)


class My15:

    def __init__(self, y):
        self.y = y

    @story
    def x(self):
        self.y()
        self.three()

    def three(self):
        raise Exception


class My16:

    def __init__(self, z):
        self.z = z

    @story
    def y(self):
        self.z()
        self.two()

    def two(self):
        raise Exception


class My17:

    @story
    def z(self):
        self.one()

    def one(self):
        return Result(3)


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


def test_assertion_substory_context():

    with pytest.raises(AssertionError):
        My6().x()


def test_failure_substory():

    result = My7().x(1)
    assert isinstance(result, Failure)


def test_result_substory():

    result = My7().x(2)
    assert result is True


def test_injectable_substory():

    def foo(arg):
        assert arg == 1
        return True

    result = My8(f=foo).x(a=1)
    assert result == 2


def test_class_attribute_access_substory():

    result = My9().x()
    assert result is True


def test_substory_for_substory():

    result = My10().x()
    assert result is True


def test_direct_substory():

    result = My11().x()
    assert result is True


def test_injectable_substory_to_story():

    z = My14().z
    y = My13(z).y
    result = My12(y).x()
    assert result == 3


def test_injectable_substory_to_story_result():

    z = My17().z
    y = My16(z).y
    result = My15(y).x()
    assert result == 3
