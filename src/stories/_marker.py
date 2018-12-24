from ._return import Success


class BeginningOfStory(object):

    __name__ = "validate_substory_arguments"

    def __init__(self, name, arguments):
        self.method_name = name
        self.arguments = arguments

    def __call__(self, ctx):
        assert set(self.arguments) <= set(ctx)
        return Success()


class EndOfStory(object):

    __name__ = "end_of_story"

    def __call__(self, ctx):
        return Success()
