class StoryError(Exception):
    pass


class FailureError(StoryError):
    def __init__(self, reason):
        self.reason = reason
        super(FailureError, self).__init__()

    def __repr__(self):
        reason = repr(self.reason) if self.reason else ""  # FIXME: Test me!
        return self.__class__.__name__ + "(" + reason + ")"


class FailureProtocolError(StoryError):
    pass
