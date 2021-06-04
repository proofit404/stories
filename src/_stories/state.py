class State:
    """Business process state."""

    def __init__(self, **arguments):
        for argument, value in arguments.items():
            object.__setattr__(self, argument, value)
