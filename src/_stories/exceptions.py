class StoryError(Exception):
    pass


class StoryDefinitionError(StoryError):
    pass


class FailureError(StoryError):
    def __init__(self, reason):
        self.__reason = reason
        super(FailureError, self).__init__()

    def __repr__(self):
        reason = repr(self.__reason) if self.__reason else ""
        return "FailureError(" + reason + ")"


class FailureProtocolError(StoryError):
    pass


class ContextContractError(StoryError):
    pass


class MutationError(StoryError):
    pass
