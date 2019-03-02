from ._compat import CerberusSpec, MarshmallowSpec, PydanticSpec
from .exceptions import ContextContractError


# Unknown variables.


def unknown_null(spec, kwargs):
    return []


def unknown_pydantic(spec, kwargs):
    return set(kwargs) - set(spec.__fields__)


def unknown_marshmallow(spec, kwargs):
    return set(kwargs) - set(spec._declared_fields)


def unknown_cerberus(spec, kwargs):
    return set(kwargs) - set(spec.schema)


def unknown_raw(spec, kwargs):
    return set(kwargs) - set(spec)


# Validation.


def validate_null(spec, kwargs):
    pass


def validate_pydantic(spec, kwargs):
    spec(**kwargs)


def validate_marshmallow(spec, kwargs):
    spec().load(kwargs)


def validate_cerberus(spec, kwargs):
    assert spec.validate(kwargs)


def validate_raw(spec, kwargs):
    for key, value in kwargs.items():
        if not spec[key](value):
            raise Exception("We are here.")


# Execute.


def make_contract(cls_name, name, arguments, spec):
    if spec is None:
        unknown_func = unknown_null
        validate_func = validate_null
    elif isinstance(spec, PydanticSpec):
        unknown_func = unknown_pydantic
        validate_func = validate_pydantic
    elif isinstance(spec, MarshmallowSpec):
        unknown_func = unknown_marshmallow
        validate_func = validate_marshmallow
    elif isinstance(spec, CerberusSpec):
        unknown_func = unknown_cerberus
        validate_func = validate_cerberus
    elif isinstance(spec, dict):
        unknown_func = unknown_raw
        validate_func = validate_raw
    return Contract(cls_name, name, arguments, spec, unknown_func, validate_func)


def validate_arguments(arguments, args, kwargs):
    # FIXME: Should be a method of the `Contract` class.
    assert not (args and kwargs)

    if args:
        assert len(arguments) == len(args)
        return [(k, v) for k, v in zip(arguments, args)]

    assert set(arguments) == set(kwargs)
    return [(k, kwargs[k]) for k in arguments]


class Contract(object):
    def __init__(self, cls_name, name, arguments, spec, unknown_func, validate_func):
        self.cls_name = cls_name
        self.name = name
        self.arguments = arguments
        self.spec = spec
        self.unknown_func = unknown_func
        self.validate_func = validate_func

    def check_story_arguments(self, ctx):
        missed = set(self.arguments) - set(ctx._Context__ns)
        if missed:
            message = missed_variable_template.format(
                missed=", ".join(sorted(missed)),
                cls=self.cls_name,
                method=self.name,
                arguments=", ".join(self.arguments),
                ctx=ctx,
            )
            raise ContextContractError(message)

    def check_success_statement(self, method, ctx, ns):
        tries_to_override = set(ctx._Context__ns) & set(ns)
        if tries_to_override:
            message = variable_override_template.format(
                variables=", ".join(map(repr, sorted(tries_to_override))),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
            )
            raise ContextContractError(message)
        unknown_variables = self.unknown_func(self.spec, ns)
        if unknown_variables:
            message = ""
            raise ContextContractError(message)
        self.validate_func(self.spec, ns)


def deny_attribute_assign():
    raise ContextContractError(assign_attribute_template)


def deny_attribute_delete():
    raise ContextContractError(delete_attribute_template)


# Messages.


missed_variable_template = """
These variables are missing from the context: {missed}

Story method: {cls}.{method}

Story arguments: {arguments}

{ctx!r}
""".strip()


variable_override_template = """
These variables are already present in the context: {variables}

Function returned value: {cls}.{method}

Use different names for Success() keyword arguments.
""".strip()


assign_attribute_template = """
Context object is immutable.

Use Success() keyword arguments to expand its scope.
""".strip()


delete_attribute_template = """
Context object is immutable.

Variables can not be removed from Context.
""".strip()
