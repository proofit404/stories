def _normal_method(self, state):
    ...


def _append_method(attribute, value):
    def method(self, state):
        getattr(state, attribute).append(value)

    return method


def _error_method(message):
    def method(self, state):
        raise _StepError(message)

    return method


class _StepError(Exception):
    ...
