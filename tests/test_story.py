from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from stories import story
from stories.typing import Persona


def test_execute_steps() -> None:
    @story
    def a1(it: Persona, state: State) -> None:
        it.a1s1(state)
        it.a1s2(state)
        it.a1s3(state)

    @story
    def b1(it: Persona, state: State) -> None:
        it.b1s1(state)
        it.a1(state)
        it.b1s2(state)

    @story
    def c1(it: Persona, state: State) -> None:
        it.c1s1(state)
        it.b1(state)
        it.c1s2(state)

    # First level.

    state = State()
    a1(A1Steps(), state)
    assert state.calls == ["a1s1", "a1s2", "a1s3"]

    # Second level.

    state = State()
    b1(B1Steps(), state)
    assert state.calls == ["b1s1", "a1s1", "a1s2", "a1s3", "b1s2"]

    # Third level.

    state = State()
    c1(C1Steps(), state)
    assert state.calls == ["c1s1", "b1s1", "a1s1", "a1s2", "a1s3", "b1s2", "c1s2"]


class A1Steps:
    def a1s1(self, state: State) -> None:
        state.calls.append("a1s1")

    def a1s2(self, state: State) -> None:
        state.calls.append("a1s2")

    def a1s3(self, state: State) -> None:
        state.calls.append("a1s3")


class B1Steps:
    def b1s1(self, state: State) -> None:
        state.calls.append("b1s1")

    def b1s2(self, state: State) -> None:
        state.calls.append("b1s2")


class C1Steps:
    def c1s1(self, state: State) -> None:
        state.calls.append("c1s1")

    def c1s2(self, state: State) -> None:
        state.calls.append("c1s2")


@dataclass
class State:
    calls: list[str] = field(default_factory=list)
