from __future__ import annotations
class Steps:
    def __init__(self) -> None:
        self.__steps__: list[str] = []

    def __getattr__(self, name: str) -> None:
        self.__steps__.append(name)

    def __call__(self, story: Story) -> Iterable[Callable[[State]]]:
        for step in self.__steps__:
            yield getattr(story, step)
