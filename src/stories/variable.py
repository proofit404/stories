class Variable:
    """Variable definition in state class."""

    def __init__(self, validate=None):
        self.validate = validate or _default

    def __repr__(self):
        if self.validate is _default:
            return "Variable()"
        else:
            return f"Variable({self.validate!r})"


def _default(value):
    return value
