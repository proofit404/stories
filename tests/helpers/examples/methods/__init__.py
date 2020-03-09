# -*- coding: utf-8 -*-
from stories import story


# Child base classes.


class Child(object):
    @story
    def x(I):
        I.one
        I.two
        I.three


# Parent base classes.


class Parent(object):
    @story
    def a(I):
        I.before
        I.x
        I.after


class ExpectedException(Exception):
    pass
