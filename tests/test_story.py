import pytest

from stories import story
from stories.exceptions import StoryDefinitionError


def test_story_private_fields():
    """Deny access to the private fields of the story class and object."""

    @story
    def do(I):
        I.one

    assert do.__dict__ == {}


def test_deny_empty_stories():
    """We can not define a story which does not have any steps.

    This will make it impossible to determine the right executor in the stories
    composition.

    """

    with pytest.raises(StoryDefinitionError) as exc_info:

        class Action:
            @story
            def do(I):
                pass

    assert str(exc_info.value) == "Story should have at least one step defined"


def test_deny_repeat_steps():
    """We can not define a story which has duplicating steps."""

    with pytest.raises(StoryDefinitionError) as exc_info:

        class Action:
            @story
            def do(I):
                I.foo
                I.bar
                I.foo

    assert str(exc_info.value) == "Story has repeated steps: foo"


def test_deny_recursive_stories():
    """Story can not call itself as step.

    This should prevent recursion error at the wrapping step.

    """
    with pytest.raises(StoryDefinitionError) as exc_info:

        class Action:
            @story
            def do(I):
                I.one
                I.do
                I.two

    assert str(exc_info.value) == "Story should not call itself recursively"


def test_story_representation(x):

    story = repr(x.Simple().x)
    expected = """
Simple.x
  one
  two
  three
""".strip()
    assert story == expected

    story = repr(x.SubstoryDI(x.Simple().x).y)
    expected = """
SubstoryDI.y
  start
  before
  x (Simple.x)
    one
    two
    three
  after
""".strip()
    assert story == expected


def test_story_class_attribute_representation(x):

    story = repr(x.Simple.x)
    expected = """
Simple.x
  one
  two
  three
""".strip()
    assert story == expected

    story = repr(x.SubstoryDI.y)
    expected = """
SubstoryDI.y
  start
  before
  x
  after
""".strip()
    assert story == expected


def test_deny_coroutine_stories(r, x):
    """Story specification can not be a coroutine function."""
    r.skip_if_function()

    expected = "Story should be a regular function"

    with pytest.raises(StoryDefinitionError) as exc_info:
        x.define_coroutine_story()
    assert str(exc_info.value) == expected


def test_deny_mix_coroutine_with_regular_methods(r, x):
    """If all story steps are functions, we can not use coroutine method in it."""
    r.skip_if_function()

    class A(x.Child, x.MixedCoroutineMethod):
        pass

    class B(x.Parent, x.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
Coroutines and functions can not be used together in story definition.

This method should be a function: A.three

Story method: A.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        A().x
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
Coroutines and functions can not be used together in story definition.

This method should be a function: A.three

Story method: A.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        B().a
    assert str(exc_info.value) == expected


def test_deny_mix_function_with_coroutine_methods(r, x):
    """If all story steps are functions, we can not use coroutine method in it."""
    r.skip_if_function()

    class A(x.Child, x.MixedFunctionMethod):
        pass

    class B(x.Parent, x.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # First level.

    expected = """
Coroutines and functions can not be used together in story definition.

This method should be a coroutine: A.three

Story method: A.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        A().x
    assert str(exc_info.value) == expected

    # Second level.

    expected = """
Coroutines and functions can not be used together in story definition.

This method should be a coroutine: A.three

Story method: A.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        B().a
    assert str(exc_info.value) == expected


def test_deny_compose_coroutine_with_function_stories(r, x):
    """If child story steps are coroutines, we can not inject this story in a parent
    which steps are functions."""
    r.skip_if_function()

    class A(x.Child, x.NormalMethod):
        pass

    class B(x.Parent, x.FunctionParentMethod):
        def __init__(self):
            self.x = A().x

    # Second level.

    expected = """
Coroutine and function stories can not be injected into each other.

Story function method: B.a

Substory coroutine method: A.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        B().a
    assert str(exc_info.value) == expected


def test_deny_compose_function_with_coroutine_stories(r, x):
    """If child story steps are functions, we can not inject this story in a parent
    which steps are coroutines."""
    r.skip_if_function()

    class A(x.Child, x.FunctionMethod):
        pass

    class B(x.Parent, x.NormalParentMethod):
        def __init__(self):
            self.x = A().x

    # Second level.

    expected = """
Coroutine and function stories can not be injected into each other.

Story coroutine method: B.a

Substory function method: A.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        B().a
    assert str(exc_info.value) == expected
