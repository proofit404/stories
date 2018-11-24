import examples


def test_story_representation():

    story = repr(examples.Empty().x)
    expected = """
Empty.x
  <empty>
""".strip()
    assert story == expected

    story = repr(examples.EmptySubstory().y)
    expected = """
EmptySubstory.y
  x
    <empty>
""".strip()
    assert story == expected

    story = repr(examples.SubstoryDI(examples.Empty().x).y)
    expected = """
SubstoryDI.y
  start
  before
  x (Empty.x)
    <empty>
  after
""".strip()
    assert story == expected

    story = repr(examples.Simple().x)
    expected = """
Simple.x
  one
  two
  three
""".strip()
    assert story == expected

    story = repr(examples.SimpleSubstory().y)
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

    story = repr(examples.SubstoryDI(examples.Simple().x).y)
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

    story = repr(examples.SubstoryDI(examples.SimpleSubstory().z).y)
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

    story = repr(examples.Empty.x)
    expected = """
Empty.x
  <empty>
""".strip()
    assert story == expected

    story = repr(examples.EmptySubstory.y)
    expected = """
EmptySubstory.y
  x
    <empty>
""".strip()
    assert story == expected

    story = repr(examples.Simple.x)
    expected = """
Simple.x
  one
  two
  three
""".strip()
    assert story == expected

    story = repr(examples.SimpleSubstory.y)
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

    story = repr(examples.SubstoryDI.y)
    expected = """
SubstoryDI.y
  start
  before
  x ??
  after
""".strip()
    assert story == expected
