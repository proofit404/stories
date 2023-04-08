from dataclasses import dataclass
from dataclasses import field

from stories import story


def test_execute_steps() -> None:
    @dataclass
    class State:
        calls: list[str] = field(default_factory=list)

    class A1:
        @story
        def it(self, state: State) -> None:
            self.a1s1(state)
            self.a1s2(state)
            self.a1s3(state)

        def a1s1(self, state: State) -> None:
            state.calls.append("a1s1")

        def a1s2(self, state: State) -> None:
            state.calls.append("a1s2")

        def a1s3(self, state: State) -> None:
            state.calls.append("a1s3")

    class B1:
        @story
        def it(self, state: State) -> None:
            self.b1s1(state)
            self.a1(state)
            self.b1s2(state)

        def b1s1(self, state: State) -> None:
            state.calls.append("b1s1")

        def b1s2(self, state: State) -> None:
            state.calls.append("b1s2")

        def __init__(self) -> None:
            self.a1 = A1().it

    class C1:
        @story
        def it(self, state: State) -> None:
            self.c1s1(state)
            self.b1(state)
            self.c1s2(state)

        def c1s1(self, state: State) -> None:
            state.calls.append("c1s1")

        def c1s2(self, state: State) -> None:
            state.calls.append("c1s2")

        def __init__(self) -> None:
            self.b1 = B1().it

    # First level.

    state = State()
    A1().it(state)
    assert state.calls == ["a1s1", "a1s2", "a1s3"]

    # Second level.

    state = State()
    B1().it(state)
    assert state.calls == ["b1s1", "a1s1", "a1s2", "a1s3", "b1s2"]

    # Third level.

    state = State()
    C1().it(state)
    assert state.calls == ["c1s1", "b1s1", "a1s1", "a1s2", "a1s3", "b1s2", "c1s2"]
