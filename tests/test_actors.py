from types import SimpleNamespace

from fixtures import S
from stories import I


def test_define_actor(s: S) -> None:
    class User(s.actor_class):
        ...

    class A1(s.story_class, User):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = s.normal_method
        a1s2 = s.normal_method
        a1s3 = s.normal_method

    class B1(s.story_class, User):
        I.b1s1
        I.a1
        I.b1s2

        b1s1 = s.normal_method
        b1s2 = s.normal_method

        def __init__(self) -> None:
            self.a1 = A1()

    class C1(s.story_class, User):
        I.c1s1
        I.b1
        I.c1s2

        c1s1 = s.normal_method
        c1s2 = s.normal_method

        def __init__(self) -> None:
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
