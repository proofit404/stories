class StoryError(Exception):
    pass


class FailureError(StoryError):
    def __init__(self, reason):
        self.reason = reason
        super(FailureError, self).__init__()
