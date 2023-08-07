class StoryError(Exception):
    """Base error of all stories errors."""

    pass


class StateError(StoryError):
    """Incorrect state usage."""

    pass
