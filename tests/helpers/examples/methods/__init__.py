from stories import arguments
from stories import story


# Child base classes.


class Child:
    @story
    def a1(I):
        I.a1s1
        I.a1s2
        I.a1s3


class ParamChild(object):
    @story
    @arguments("a1v1", "a1v2")
    def a1(I):
        I.a1s1
        I.a1s2
        I.a1s3


# Parent base classes.


class Parent:
    @story
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


class ParamParent(object):
    @story
    @arguments("b1v1")
    def b1(I):
        I.b1s1
        I.a1
        I.b1s2


class ExpectedException(Exception):
    pass


# Root base classes.


class Root(object):
    @story
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2


class ParamRoot(object):
    @story
    @arguments("c1v1")
    def c1(I):
        I.c1s1
        I.b1
        I.c1s2
