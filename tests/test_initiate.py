"""Tests related to @initiate decorator."""
from stories import I
from stories import initiate
from stories import State
from stories import Story


def test_initiate(r, m):
    """All story steps could be nested stories."""

    class A1(Story):
        I.a1s1
        I.a1s2
        I.a1s3

        a1s1 = m._append_method("calls", "a1s1")
        a1s2 = m._append_method("calls", "a1s2")
        a1s3 = m._append_method("calls", "a1s3")

    class A2(Story):
        I.a2s1
        I.a2s2
        I.a2s3

        a2s1 = m._append_method("calls", "a2s1")
        a2s2 = m._append_method("calls", "a2s2")
        a2s3 = m._append_method("calls", "a2s3")

    class A3(Story):
        I.a3s1
        I.a3s2
        I.a3s3

        a3s1 = m._append_method("calls", "a3s1")
        a3s2 = m._append_method("calls", "a3s2")
        a3s3 = m._append_method("calls", "a3s3")

    class A4(Story):
        I.a4s1

        a4s1 = m._append_method("calls", "a4s1")

    @initiate
    class B1(Story):
        I.a1
        I.a2

    @initiate
    class B2(Story):
        I.a3
        I.a4

    @initiate
    class C1(Story):
        I.b1
        I.b2

    # First level.

    story = A1()
    state = State(calls=[])
    r.run(story, state)
    assert state.calls == ["a1s1", "a1s2", "a1s3"]

    # Second level.

    story = B1(a1=A1(), a2=A2())
    state = State(calls=[])
    r.run(story, state)
    assert state.calls == ["a1s1", "a1s2", "a1s3", "a2s1", "a2s2", "a2s3"]

    # Third level.

    story = C1(b1=B1(a1=A1(), a2=A2()), b2=B2(a3=A3(), a4=A4()))
    state = State(calls=[])
    r.run(story, state)
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
