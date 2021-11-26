async def _normal_method(self, state):
    ...


def _assign_method(attribute, value):
    async def method(self, state):
        setattr(state, attribute, value)

    return method


def _append_method(attribute, value):
    async def method(self, state):
        getattr(state, attribute).append(value)

    return method


def _error_method(message):
    async def method(self, state):
        raise _StepError(message)

    return method


class _StepError(Exception):
    ...
