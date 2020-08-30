from stories import story


# Child base classes.


class Child:
    @story
    def x(I):
        I.one
        I.two
        I.three


# Parent base classes.


class Parent:
    @story
    def a(I):
        I.before
        I.x
        I.after


class ExpectedException(Exception):
    pass
