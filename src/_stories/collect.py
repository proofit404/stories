# -*- coding: utf-8 -*-
from inspect import getsourcelines

from _stories.calls import CallMethod
from _stories.compat import iscoroutinefunction
from _stories.exceptions import StoryDefinitionError


def create_class_story_example(f):
    try:
        lines, _ = getsourcelines(f.__func__)
        i = 0
        for c in lines[0]:
            if not c.isspace():
                break
            i += 1
        indentation = " " * i
        new_lines = []
        for line in lines:
            if "@story" in line:
                line = line.replace("@story", "@class_story")
            if "(I):" in line:
                line = line.replace("(I):", "(cls, I):")
            if "@classmethod" not in line:
                line = line.replace(indentation, "").rstrip()
                new_lines.append(line)
    except OSError:
        new_lines = ["Source code unavailable."]

    return new_lines


def collect_story(f):
    if isinstance(f, classmethod):
        new_lines = create_class_story_example(f)
        raise StoryDefinitionError(
            use_class_story_template.format(source="\n".join(new_lines))
        )

    if iscoroutinefunction(f):
        raise StoryDefinitionError("Story should be a regular function")

    calls = []

    class Collector(object):
        def __getattr__(self, name):
            self.__append_to_calls__(CallMethod(name))

        def __append_to_calls__(self, call):
            calls.append(call)

    f(Collector())

    if not calls:
        raise StoryDefinitionError("Story should have at least one step defined")

    return calls


use_class_story_template = """
Story cannot be a class method.

Use @class_story instead:
{source}
""".strip()
