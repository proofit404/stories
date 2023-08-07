from _stories.argument import Argument
from _stories.state import State
from _stories.variable import Variable


def Union(*states):
    """Create a union of states.

    State union combine variables and arguments defined in each state.

    Validators for repeated variables and arguments would be combined as well.

    """
    class_name = "Union(" + ", ".join(state.__name__ for state in states) + ")"
    scope = {
        name: lookup[is_argument](_Merge(validators))
        for name, (is_argument, validators) in _compose(states)
    }
    return type(class_name, (State,), scope)


class _Merge:
    def __new__(cls, validators):
        if len(validators) > 1:
            return object.__new__(cls)
        else:
            return validators[0]

    def __init__(self, validators):
        self.validators = validators

    def __call__(self, value):
        for validator in self.validators:
            validated = validator(value)
        return validated


def _compose(states):
    new = {}
    for state in states:
        init = state.__init__
        arguments = init.arguments
        for name, validator in init.validators.items():
            _set(new, name, name in arguments, validator)
    return new.items()


def _set(new, name, is_argument, validator):
    value = new.setdefault(name, [False, []])
    value[0] = value[0] or is_argument
    if isinstance(validator, _Merge):
        value[1].extend(validator.validators)
    else:
        value[1].append(validator)


lookup = {True: Argument, False: Variable}
