from types import SimpleNamespace

from stories import I


def test_define_actor(s) -> None:
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

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.Story, User):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.normal_method
        c1s2 = s.normal_method

        def __init__(self) -> None:
            self.b1 = B1()

    # First level.

    story_a = A1()
    state_a = SimpleNamespace()
    s.run(story_a, state_a)
    assert isinstance(story_a, User)

    # Second level.

    story_b = B1()
    state_b = SimpleNamespace()
    s.run(story_b, state_b)
    assert isinstance(story_b, User)

    # Third level.

    story_c = C1()
    state_c = SimpleNamespace()
    s.run(story_c, state_c)
    assert isinstance(story_c, User)
