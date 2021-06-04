"""Tests related to @initiate decorator."""
from stories.exceptions import StoryError


def test_initiate():
    """Dumb test for coverage."""
    assert issubclass(StoryError, Exception)
