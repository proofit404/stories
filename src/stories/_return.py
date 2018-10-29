from ._repr import namespace_representation


class Result(object):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.value) + ")"


class Success(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __repr__(self):
        return self.__class__.__name__ + namespace_representation(self.kwargs)


class Failure(object):
    def __init__(self, reason=None):
        self.reason = reason

    def __repr__(self):
        reason = repr(self.reason) if self.reason else ""
        return self.__class__.__name__ + "(" + reason + ")"


class Skip(object):
    def __repr__(self):
        return self.__class__.__name__ + "()"
