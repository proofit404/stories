class Result:
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        value = repr(self.value) if self.value is not None else ''
        return "Result(" + value + ")"


class Failure:
    def __init__(self, reason=None):
        self.reason = reason

    def __repr__(self):
        reason = repr(self.reason) if self.reason else ""
        return "Failure(" + reason + ")"


class Success:
    def __repr__(self):
        return "Success()"


class Next:
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        value = repr(self.value) if self.value is not None else ''
        return "Next(" + value + ")"
