class Result(object):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return "Result(" + repr(self.value) + ")"


class Success(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __repr__(self):
        return (
            self.__class__.__name__
            + "("
            + ", ".join([k + "=" + repr(v) for k, v in self.kwargs.items()])
            + ")"
        )


class Skip(Success):
    pass


class Failure(object):
    def __init__(self, reason=None):
        self.reason = reason

    def __repr__(self):
        reason = repr(self.reason) if self.reason else ""
        return "Failure(" + reason + ")"
