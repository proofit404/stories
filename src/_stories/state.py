from _stories.variable import Variable


def _setter(state, name, value):
    object.__setattr__(state, name, value)


def _initiator(state, **arguments):
    for argument, value in arguments.items():
        _setter(state, argument, value)


class _ValidateSetter:
    def __init__(self, variables):
        self.variables = variables

    def __get__(self, state, state_class):
        return _BoundValidateSetter(self.variables, state)


class _BoundValidateSetter:
    def __init__(self, variables, state):
        self.variables = variables
        self.state = state

    def __call__(self, name, value):
        validator = self.variables[name]
        validated = validator(value)
        _setter(self.state, name, validated)


class _StateType(type):
    def __new__(cls, class_name, bases, namespace):
        if bases:
            variables = {
                k: v.validate for k, v in namespace.items() if isinstance(v, Variable)
            }
            scope = {
                "__setattr__": _ValidateSetter(variables),
                "__init__": _initiator,  # pragma: no mutate
            }
        else:
            scope = {
                "__setattr__": _setter,  # pragma: no mutate
                "__init__": _initiator,
            }
        return type.__new__(cls, class_name, bases, scope)

    def __and__(cls, other):
        union = {
            k: Variable(v)
            for state_class in [cls, other]
            for k, v in state_class.__setattr__.variables.items()
        }
        return type(cls.__name__, (State,), union)


class State(metaclass=_StateType):
    """Business process state."""
