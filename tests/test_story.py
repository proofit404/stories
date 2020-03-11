# -*- coding: utf-8 -*-
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

    This will make it impossible to determine the right executor in the
    stories composition.
    """

    with pytest.raises(StoryDefinitionError) as exc_info:

        class Action(object):
            @story
            def do(I):
                pass

    assert str(exc_info.value) == "Story should have at least one step defined"


def test_story_representation(x):

    story = repr(x.Simple().x)
    expected = """
Simple.x
  one
  two
  three
""".strip()
    assert story == expected

    story = repr(x.SimpleSubstory().y)
    expected = """
SimpleSubstory.y
  start
  before
  x
    one
    two
    three
  after
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

    story = repr(x.SubstoryDI(x.SimpleSubstory().z).y)
    expected = """
SubstoryDI.y
  start
  before
  x (SimpleSubstory.z)
    first
    x
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

    story = repr(x.SimpleSubstory.y)
    expected = """
SimpleSubstory.y
  start
  before
  x
    one
    two
    three
  after
""".strip()
    assert story == expected

    story = repr(x.SubstoryDI.y)
    expected = """
SubstoryDI.y
  start
  before
  x ??
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
    """If all story steps are functions, we can not use coroutine method in
    it."""
    r.skip_if_function()

    class T(x.Child, x.MixedCoroutineMethod):
        pass

    class Q(x.Parent, x.NormalParentMethod, T):
        pass

    class J(x.Parent, x.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
Coroutines and functions can not be used together in story definition.

This method should be a function: T.three

Story method: T.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        T().x
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Coroutines and functions can not be used together in story definition.

This method should be a function: Q.three

Story method: Q.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        Q().a
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Coroutines and functions can not be used together in story definition.

This method should be a function: T.three

Story method: T.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        J().a
    assert str(exc_info.value) == expected


def test_deny_mix_function_with_coroutine_methods(r, x):
    """If all story steps are functions, we can not use coroutine method in
    it."""
    r.skip_if_function()

    class T(x.Child, x.MixedFunctionMethod):
        pass

    class Q(x.Parent, x.NormalParentMethod, T):
        pass

    class J(x.Parent, x.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Simple.

    expected = """
Coroutines and functions can not be used together in story definition.

This method should be a coroutine: T.three

Story method: T.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        T().x
    assert str(exc_info.value) == expected

    # Substory inheritance.

    expected = """
Coroutines and functions can not be used together in story definition.

This method should be a coroutine: Q.three

Story method: Q.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        Q().a
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Coroutines and functions can not be used together in story definition.

This method should be a coroutine: T.three

Story method: T.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        J().a
    assert str(exc_info.value) == expected


def test_deny_compose_coroutine_with_function_stories(r, x):
    """If child story steps are coroutines, we can not inject this story in a
    parent which steps are functions."""
    r.skip_if_function()

    class T(x.Child, x.NormalMethod):
        pass

    class Q(x.Parent, x.FunctionParentMethod, T):
        pass

    class J(x.Parent, x.FunctionParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Coroutine and function stories can not be injected into each other.

Story function method: Q.a

Substory coroutine method: Q.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        Q().a
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Coroutine and function stories can not be injected into each other.

Story function method: J.a

Substory coroutine method: T.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        J().a
    assert str(exc_info.value) == expected


def test_deny_compose_function_with_coroutine_stories(r, x):
    """If child story steps are functions, we can not inject this story in a
    parent which steps are coroutines."""
    r.skip_if_function()

    class T(x.Child, x.FunctionMethod):
        pass

    class Q(x.Parent, x.NormalParentMethod, T):
        pass

    class J(x.Parent, x.NormalParentMethod):
        def __init__(self):
            self.x = T().x

    # Substory inheritance.

    expected = """
Coroutine and function stories can not be injected into each other.

Story coroutine method: Q.a

Substory function method: Q.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        Q().a
    assert str(exc_info.value) == expected

    # Substory DI.

    expected = """
Coroutine and function stories can not be injected into each other.

Story coroutine method: J.a

Substory function method: T.x
    """.strip()

    with pytest.raises(StoryDefinitionError) as exc_info:
        J().a
    assert str(exc_info.value) == expected
