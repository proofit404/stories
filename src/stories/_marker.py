from ._return import Success


class BeginningOfStory(object):

    __name__ = "validate_substory_arguments"

    def __init__(self, cls_name, name, arguments):
        self.cls_name = cls_name
        self.name = name
        self.parent_name = None
        self.same_object = None
        self.arguments = arguments

    def __call__(self, ctx):
        assert set(self.arguments) <= set(ctx)
        return Success()

    @property
    def method_name(self):
        if self.parent_name is None:
            return self.cls_name + "." + self.name
        elif self.same_object:
            return self.parent_name
        else:
            return self.parent_name + " (" + self.cls_name + "." + self.name + ")"

    def set_parent(self, parent_name, same_object):
        self.parent_name = parent_name
        self.same_object = same_object


class EndOfStory(object):

    __name__ = "end_of_story"

    def __call__(self, ctx):
        return Success()
