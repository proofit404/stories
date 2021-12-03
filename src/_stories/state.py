from _stories.argument import Argument
from _stories.exceptions import StateError
from _stories.variable import Variable


def _setter(state, name, value):
    object.__setattr__(state, name, value)


def _initiator(state, **arguments):
    for argument, value in arguments.items():
        _setter(state, argument, value)


class _ValidateSetter:
    def __init__(self, validators):
        self.validators = validators

    def __get__(self, state, state_class):
        return _BoundValidateSetter(self.validators, state)


class _ValidateInitiator:
    def __init__(self, validators, arguments):
        self.validators = validators
        self.arguments = arguments

    def __get__(self, state, state_class):
        return _BoundValidateInitiator(self.validators, self.arguments, state)


class _BoundValidateSetter:
    def __init__(self, validators, state):
        self.validators = validators
        self.state = state

    def __call__(self, name, value):
        if name not in self.validators:
            message = unknown_variable_template.format(variable=name, state=self.state)
            raise StateError(message)
        validator = self.validators[name]
        validated = validator(value)
        _setter(self.state, name, validated)


class _BoundValidateInitiator:
    def __init__(self, validators, arguments, state):
        self.validators = validators
        self.arguments = arguments
        self.state = state

    def __call__(self, **arguments):
        template = unknown_argument_template
        for argument, value in arguments.items():
            if argument not in self.arguments:
                message = template.format(argument=argument, state=self.state)
                raise StateError(message)
            validator = self.validators[argument]
            validated = validator(value)
            _setter(self.state, argument, validated)


def _representation(state):
    return state.__class__.__name__


def _class_representation(state_class):
    validators = state_class.__init__.validators
    variables = "\n".join(
        f"    {name} = Variable({validators[name]!r})" for name in sorted(validators)
    )
    return f"{state_class.__name__}:\n{variables}"


def _new_validate_state(namespace):
    validators = {
        k: v.validate
        for k, v in namespace.items()
        if isinstance(v, (Variable, Argument))
    }
    arguments = {k for k, v in namespace.items() if isinstance(v, Argument)}
    scope = {
        "__setattr__": _ValidateSetter(validators),
        "__init__": _ValidateInitiator(validators, arguments),
        "__repr__": _representation,
    }
    return scope


class _StateType(type):
    def __new__(cls, class_name, bases, namespace):
        if bases:
            scope = _new_validate_state(namespace)
        else:
            scope = {"__init__": _initiator}
        return type.__new__(cls, class_name, bases, scope)

    def __repr__(cls):
        return _class_representation(cls)


class State(metaclass=_StateType):
    """Business process state."""


unknown_variable_template = """
Unknown variable assignment: {variable}

{state!r}
""".strip()


unknown_argument_template = """
Unknown argument passed: {argument}

{state!r}
""".strip()
