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
            "Success("
            + ", ".join([k + "=" + repr(v) for k, v in self.kwargs.items()])
            + ")"
        )


class Failure(object):
    def __init__(self, reason=None):
        self.reason = reason

    def __repr__(self):
        reason = repr(self.reason) if self.reason else ""
        return "Failure(" + reason + ")"


class Skip(object):
    def __repr__(self):
        return "Skip()"
