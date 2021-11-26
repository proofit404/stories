class Variable:
    """Variable definition in state class."""

    def __init__(self, validate=None):
        self.validate = validate or (lambda value: value)
