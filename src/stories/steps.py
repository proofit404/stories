from __future__ import annotations

from collections.abc import Callable
from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stories import Story


class Steps:
    def __init__(self) -> None:
        self.__steps__ = []

    def __getattr__(self, name: str) -> None:
        self.__steps__.append(name)

    def __call__(self, story: Story) -> Iterable[Callable[[object], None]]:
        for step in self.__steps__:
            yield getattr(story, step)
