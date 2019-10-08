import pytest

from stories import arguments
from stories import story
from stories.exceptions import StoryDefinitionError


def test_deny_empty_arguments():
    """
    We can not used @arguments decorator without the actual arguments
    passed in.
    """

    with pytest.raises(StoryDefinitionError) as exc_info:

        class Action(object):
            @story
            @arguments()
            def do(I):
                pass

    assert str(exc_info.value) == "Story arguments can not be an empty list"


def test_deny_non_string_arguments():
    """
    We can not pass anything except string to the story @arguments
    decorator.
    """

    with pytest.raises(StoryDefinitionError) as exc_info:

        class Action(object):
            @story
            @arguments
            def do(I):
                pass

    assert str(exc_info.value) == "Story arguments can only be defined with string type"
