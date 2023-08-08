class Steps:
    def __init__(self) -> None:
        self.__steps__: list[str] = []

    def __getattr__(self, name: str) -> None:
        self.__steps__.append(name)
