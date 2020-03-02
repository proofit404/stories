# -*- coding: utf-8 -*-


class StoryError(Exception):
    pass


class StoryDefinitionError(StoryError):
    pass


class FailureError(StoryError):
    pass


def make_failure_error(reason):
    reason_representation = repr(reason) if reason else ""

    def repr_method(self):
        return "FailureError(" + reason_representation + ")"

    return type("FailureError", (FailureError,), {"__repr__": repr_method})()


class FailureProtocolError(StoryError):
    pass


class ContextContractError(StoryError):
    pass


class MutationError(StoryError):
    pass
