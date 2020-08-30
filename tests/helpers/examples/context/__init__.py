from stories import arguments
from stories import story


# Base classes.


class Child:
    @story
    def x(I):
        I.one


class ParamChild:
    @story
    @arguments("bar")
    def x(I):
        I.one


class Parent:
    @story
    def a(I):
        I.before
        I.x
        I.after


class ParamParent:
    @story
    @arguments("bar")
    def a(I):
        I.before
        I.x
        I.after
