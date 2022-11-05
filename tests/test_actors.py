"""Tests related to actors module."""
from types import SimpleNamespace

from stories import Actor
from stories import I
from stories import Story


def test_define_actor(r, m):
    """Story could be written for certain actor."""

    class User(Actor):
        ...

    class A1(Story, User):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._normal_method
        a1s2 = m._normal_method
        a1s3 = m._normal_method

    class B1(Story, User):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = m._normal_method
        b1s2 = m._normal_method

        def __init__(self):
            self.a1 = A1()

    class C1(Story, User):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = m._normal_method
        c1s2 = m._normal_method

        def __init__(self):
            self.b1 = B1()

    # First level.

    story = A1()
    state = SimpleNamespace()
    r.run(story, state)
    assert isinstance(story, User)

    # Second level.

    story = B1()
    state = SimpleNamespace()
    r.run(story, state)
    assert isinstance(story, User)

    # Third level.

    story = C1()
    state = SimpleNamespace()
    r.run(story, state)
    assert isinstance(story, User)
