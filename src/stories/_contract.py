from ._compat import CerberusSpec, MarshmallowSpec, PydanticSpec
from .exceptions import ContextContractError


# FIXME:
#
# [ ] Handle protocol extension.  There should be way to say in the
#     substory contract "this variable should be an integer" and in
#     addition in the story "this integer should be greater then 7".
#     This way we also can require a certain substory to declare
#     context variable for parent story.


# Unknown variables.


def unknown_null(spec, kwargs):
    return [], None


def unknown_pydantic(spec, kwargs):
    available = set(spec.__fields__)
    return set(kwargs) - available, available


def unknown_marshmallow(spec, kwargs):
    available = set(spec._declared_fields)
    return set(kwargs) - available, available


def unknown_cerberus(spec, kwargs):
    available = set(spec.schema)
    return set(kwargs) - available, available


def unknown_raw(spec, kwargs):
    available = set(spec)
    return set(kwargs) - available, available


# Validation.


def validate_null(spec, ns, keys):
    return ns, None


def validate_pydantic(spec, ns, keys):
    result, errors = {}, {}
    for key in keys:
        field = spec.__fields__[key]
        new_value, error = field.validate(ns[key], {}, loc=field.alias, cls=spec)
        if error:
            # FIXME: Errors can be a list.
            errors[key] = [error.msg]
        else:
            result[key] = new_value
    return result, errors


def validate_marshmallow(spec, ns, keys):
    result, errors = spec().load(ns)
    return result, errors


def validate_cerberus(spec, ns, keys):
    validator = CerberusSpec()
    validator.validate(ns, spec.schema.schema)
    return validator.document, validator.errors


def validate_raw(spec, ns, keys):
    result, errors = {}, {}
    for key in keys:
        new_value, error = spec[key](ns[key])
        if error:
            errors[key] = [error]
        else:
            result[key] = new_value
    return result, errors


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
        kwargs, errors = self.validate_func(self.spec, ctx._Context__ns, self.arguments)
        if errors:
            message = invalid_argument_template.format(
                variables=", ".join(map(repr, sorted(errors))),
                cls=self.cls_name,
                method=self.name,
                violations="\n\n".join(
                    [key + ":\n  " + "\n  ".join(errors[key]) for key in sorted(errors)]
                ),
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
        unknown_variables, available = self.unknown_func(self.spec, ns)
        if unknown_variables:
            message = unknown_variable_template.format(
                unknown=", ".join(map(repr, sorted(unknown_variables))),
                available=", ".join(map(repr, sorted(available))),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
            )
            raise ContextContractError(message)
        kwargs, errors = self.validate_func(self.spec, ns, ns)
        if errors:
            message = invalid_variable_template.format(
                variables=", ".join(map(repr, sorted(errors))),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
                violations="\n\n".join(
                    [key + ":\n  " + "\n  ".join(errors[key]) for key in sorted(errors)]
                ),
            )
            raise ContextContractError(message)
        return kwargs


# Wrap.


def combine_contract(specs, tail):
    for first_spec, first_cls_name, first_method_name in specs:
        for second_spec, second_cls_name, second_method_name in tail:
            if first_spec is None and second_spec is None:
                repeated = set()
            elif isinstance(first_spec, PydanticSpec) and isinstance(
                second_spec, PydanticSpec
            ):
                repeated = set(first_spec.__fields__) & set(second_spec.__fields__)
            elif isinstance(first_spec, MarshmallowSpec) and isinstance(
                second_spec, MarshmallowSpec
            ):
                repeated = set(first_spec._declared_fields) & set(
                    second_spec._declared_fields
                )
            elif isinstance(first_spec, CerberusSpec) and isinstance(
                second_spec, CerberusSpec
            ):
                repeated = set(first_spec.schema) & set(second_spec.schema)
            elif isinstance(first_spec, dict) and isinstance(second_spec, dict):
                repeated = set(first_spec) & set(second_spec)
            else:
                message = type_error_template.format(
                    cls=first_cls_name,
                    method=first_method_name,
                    contract=first_spec,
                    other_cls=second_cls_name,
                    other_method=second_method_name,
                    other_contract=second_spec,
                )
                raise ContextContractError(message)
            if repeated:
                message = incompatible_contracts_template.format(
                    repeated=", ".join(map(repr, sorted(repeated))),
                    cls=first_cls_name,
                    method=first_method_name,
                    other_cls=second_cls_name,
                    other_method=second_method_name,
                )
                raise ContextContractError(message)
    contracts = []
    contracts.extend(specs)
    contracts.extend(tail)
    return contracts


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


unknown_variable_template = """
These variables were not defined in the context contract: {unknown}

Available variables are: {available}

Function returned value: {cls}.{method}

Use different names for Success() keyword arguments or add these names to the contract.
""".strip()


invalid_variable_template = """
These variables violates context contract: {variables}

Function returned value: {cls}.{method}

Violations:

{violations}
""".strip()


invalid_argument_template = """
These arguments violates context contract: {variables}

Story method: {cls}.{method}

Violations:

{violations}
""".strip()


incompatible_contracts_template = """
Repeated variables can not be used in a story composition.

Variables repeated in both context contracts: {repeated}

Story method: {cls}.{method}

Substory method: {other_cls}.{other_method}

Use variables with different names.
""".strip()


type_error_template = """
Story and substory context contracts has incompatible types:

Story method: {cls}.{method}

Story context contract: {contract}

Substory method: {other_cls}.{other_method}

Substory context contract: {other_contract}
""".strip()
