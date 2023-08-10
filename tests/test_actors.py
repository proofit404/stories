from types import SimpleNamespace

from stories import I


def test_define_actor(s):
    class User(s.Actor):
        ...

    class A1(s.Story, User):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = s.normal_method
        a1s2 = s.normal_method
        a1s3 = s.normal_method

    class B1(s.Story, User):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.normal_method
        b1s2 = s.normal_method

        def __init__(self):
            self.a1 = A1()

    class C1(s.Story, User):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.normal_method
        c1s2 = s.normal_method

        def __init__(self):
            self.b1 = B1()

    # First level.

    story = A1()
    state = SimpleNamespace()
    s.run(story, state)
    assert isinstance(story, User)

    # Second level.

    story = B1()
    state = SimpleNamespace()
    s.run(story, state)
    assert isinstance(story, User)

    # Third level.

    story = C1()
    state = SimpleNamespace()
    s.run(story, state)
    assert isinstance(story, User)
