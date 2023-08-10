from types import SimpleNamespace

import pytest

from stories import I
from stories.exceptions import StoryError


def test_initiate(s):
    class A1(s.Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = s.append_method("calls", "a1s1")
        a1s2 = s.append_method("calls", "a1s2")
        a1s3 = s.append_method("calls", "a1s3")

    class A2(s.Story):
        I.a2s1
        I.a2s2
        I.a2s3

        a2s1 = s.append_method("calls", "a2s1")
        a2s2 = s.append_method("calls", "a2s2")
        a2s3 = s.append_method("calls", "a2s3")

    class A3(s.Story):
        I.a3s1
        I.a3s2
        I.a3s3

        a3s1 = s.append_method("calls", "a3s1")
        a3s2 = s.append_method("calls", "a3s2")
        a3s3 = s.append_method("calls", "a3s3")

    class A4(s.Story):
        I.a4s1

        a4s1 = s.append_method("calls", "a4s1")

    @s.initiate
    class B1(s.Story):
        I.a1
        I.a2

    @s.initiate
    class B2(s.Story):
        I.a3
        I.a4

    @s.initiate
    class C1(s.Story):
        I.b1
        I.b2

    # First level.

    story = A1()
    state = SimpleNamespace(calls=[])
    s.run(story, state)
    assert state.calls == ["a1s1", "a1s2", "a1s3"]

    # Second level.

    story = B1(a1=A1(), a2=A2())
    state = SimpleNamespace(calls=[])
    s.run(story, state)
    assert state.calls == ["a1s1", "a1s2", "a1s3", "a2s1", "a2s2", "a2s3"]

    # Third level.

    story = C1(b1=B1(a1=A1(), a2=A2()), b2=B2(a3=A3(), a4=A4()))
    state = SimpleNamespace(calls=[])
    s.run(story, state)
    assert state.calls == [
        "a1s1",
        "a1s2",
        "a1s3",
        "a2s1",
        "a2s2",
        "a2s3",
        "a3s1",
        "a3s2",
        "a3s3",
        "a4s1",
    ]


def test_deny_functions(s):
    with pytest.raises(StoryError) as exc_info:

        @s.initiate
        def a1():  # pragma: no branch
            raise RuntimeError

    assert str(exc_info.value) == "@initiate can decorate Story subclasses only"


def test_deny_non_story_classes(s):
    with pytest.raises(StoryError) as exc_info:

        @s.initiate
        class A1:
            pass

    assert str(exc_info.value) == "@initiate can decorate Story subclasses only"


def test_deny_step_definitions(s):
    with pytest.raises(StoryError) as exc_info:

        @s.initiate
        class A1(s.Story):
            I.a1s1
            I.a1s2
            I.a1s3

            a1s1 = s.normal_method

    expected = "Story decorated by @initiate can not have step methods"

    assert str(exc_info.value) == expected


def test_deny_constructor_definition(s):
    with pytest.raises(StoryError) as exc_info:

        @s.initiate
        class A1(s.Story):
            I.a1s1
            I.a1s2
            I.a1s3

            def __init__(self):
                raise RuntimeError

    expected = "Story decorated by @initiate can not have constructor defined"

    assert str(exc_info.value) == expected
