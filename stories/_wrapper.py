from ._collect import wrap_story
from ._repr import story_representation
from ._run import run_the_story, tell_the_story


class StoryWrapper(object):
    def __init__(self, cls, obj, name, arguments, collected):
        self.cls = cls
        self.obj = obj
        self.cls_name = cls.__name__
        self.name = name
        self.arguments = arguments
        self.collected = collected
        self.of = of = object()  # FIXME: Remove!
        self.methods = wrap_story(is_story, of, obj, collected)

    def __call__(self, *args, **kwargs):
        return tell_the_story(
            self.cls_name, self.name, self.methods, self.arguments, args, kwargs
        )

    def run(self, *args, **kwargs):
        return run_the_story(
            self.cls_name, self.name, self.methods, self.arguments, args, kwargs
        )

    def __repr__(self):
        return story_representation(
            is_story,
            self.cls_name + "." + self.name,
            self.cls,
            self.obj,
            self.collected,
        )


def is_story(attribute):
    return callable(attribute) and type(attribute) is StoryWrapper
