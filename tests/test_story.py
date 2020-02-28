# -*- coding: utf-8 -*-
import pytest

import examples
from stories import story
from stories.exceptions import StoryDefinitionError


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


def test_story_representation():

    story = repr(examples.methods.Simple().x)
    expected = """
Simple.x
  one
  two
  three
""".strip()
    assert story == expected

    story = repr(examples.methods.SimpleSubstory().y)
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

    story = repr(examples.methods.SubstoryDI(examples.methods.Simple().x).y)
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

    story = repr(examples.methods.SubstoryDI(examples.methods.SimpleSubstory().z).y)
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


def test_story_class_attribute_representation():

    story = repr(examples.methods.Simple.x)
    expected = """
Simple.x
  one
  two
  three
""".strip()
    assert story == expected

    story = repr(examples.methods.SimpleSubstory.y)
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

    story = repr(examples.methods.SubstoryDI.y)
    expected = """
SubstoryDI.y
  start
  before
  x ??
  after
""".strip()
    assert story == expected
