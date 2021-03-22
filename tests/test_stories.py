"""Tests related to stories module."""
from stories import I
from stories import State
from stories import Story


def test_return_value(r, m):
    """Story should not return any value."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m.normal_method
        a1s2 = m.normal_method
        a1s3 = m.normal_method

    class B1(Story):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m.normal_method
        b1s2 = m.normal_method

        def __init__(self):
            self.a1 = A1()

    class C1(Story):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m.normal_method
        c1s2 = m.normal_method

        def __init__(self):
            self.b1 = B1()

    # First level.

    story = A1()
    state = State()
    assert r.run(story, state) is None

    # Second level.

    story = B1()
    state = State()
    assert r.run(story, state) is None

    # Third level.

    story = C1()
    state = State()
    assert r.run(story, state) is None
