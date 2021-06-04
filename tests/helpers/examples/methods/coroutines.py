async def _normal_method(self, state):
    ...


def _append_method(attribute, value):
    async def method(self, state):
        getattr(state, attribute).append(value)

    return method
