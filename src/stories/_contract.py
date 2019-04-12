from ._compat import CerberusSpec, MarshmallowSpec, PydanticSpec
from .exceptions import ContextContractError


# FIXME:
#
# [ ] Handle protocol extension.  There should be way to say in the
#     substory contract "this variable should be an integer" and in
#     addition in the story "this integer should be greater then 7".
#     This way we also can require a certain substory to declare
#     context variable for parent story.
#
# [ ] Split `Contract` class into `NullContract` and `SpecContract`
#     classes.  Checking `self.spec is None` at the beginning of
#     methods is ugly.  Drop `available_null` and `validate_null`
#     functions.


# Declared validators.


def available_null(spec):
    raise Exception


def available_pydantic(spec):
    return set(spec.__fields__)


def available_marshmallow(spec):
    return set(spec._declared_fields)


def available_cerberus(spec):
    return set(spec.schema)


def available_raw(spec):
    return set(spec)


# Validation.


def validate_null(spec, ns, keys):
    raise Exception


def validate_pydantic(spec, ns, keys):
    result, errors = {}, {}
    for key in keys:
        field = spec.__fields__[key]
        new_value, error = field.validate(ns[key], {}, loc=field.alias, cls=spec)
        if error:
            if isinstance(error, list):
                errors[key] = [e.msg for e in error]
            else:
                errors[key] = [error.msg]
        else:
            result[key] = new_value
    return result, errors


def validate_marshmallow(spec, ns, keys):
    result, errors = spec().load(ns)
    return result, errors


def validate_cerberus(spec, ns, keys):
    validator = CerberusSpec(allow_unknown=True)
    validator.validate(ns, spec.schema.schema)
    return dict((key, validator.document[key]) for key in keys), validator.errors


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
        available_func = available_null
        validate_func = validate_null
    elif isinstance(spec, PydanticSpec):
        available_func = available_pydantic
        validate_func = validate_pydantic
    elif isinstance(spec, MarshmallowSpec):
        available_func = available_marshmallow
        validate_func = validate_marshmallow
    elif isinstance(spec, CerberusSpec):
        available_func = available_cerberus
        validate_func = validate_cerberus
    elif isinstance(spec, dict):
        available_func = available_raw
        validate_func = validate_raw
    return Contract(cls_name, name, arguments, spec, available_func, validate_func)


class Contract(object):
    def __init__(self, cls_name, name, arguments, spec, available_func, validate_func):
        self.cls_name = cls_name
        self.name = name
        self.arguments = arguments
        self.spec = spec
        self.available_func = available_func
        self.validate_func = validate_func
        self.subcontracts = []
        self.check_arguments_definitions()

    def add_substory_contract(self, contract):
        self.subcontracts.append(contract)

    def check_arguments_definitions(self):
        # vvv
        if self.spec is None:
            return
        # ^^^
        undefined = set(self.arguments) - self.available_func(self.spec)
        if undefined:
            message = undefined_argument_template.format(
                undefined=", ".join(sorted(undefined)),
                cls=self.cls_name,
                method=self.name,
                arguments=", ".join(self.arguments),
            )
            raise ContextContractError(message)

    def check_story_call(self, kwargs):
        unknown_arguments = self.get_unknown_arguments(kwargs)
        if unknown_arguments:
            if self.arguments:
                template = unknown_argument_template
            else:
                template = unknown_argument_null_template
            message = template.format(
                unknown=", ".join(sorted(unknown_arguments)),
                cls=self.cls_name,
                method=self.name,
                arguments=", ".join(self.arguments),
            )
            raise ContextContractError(message)
        # vvv
        if self.spec is None:
            return kwargs
        # ^^^
        kwargs, errors = self.get_invalid_variables(kwargs)
        if errors:
            message = invalid_argument_template.format(
                variables=", ".join(map(repr, sorted(errors))),
                cls=self.cls_name,
                method=self.name,
                violations="\n\n".join(
                    [
                        key + ":\n  " + "\n  ".join(str(errors[key]))
                        for key in sorted(errors)
                    ]
                ),
            )
            raise ContextContractError(message)
        return kwargs

    def check_substory_call(self, ctx):
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
        # vvv
        if self.spec is None:
            return ns
        # ^^^
        unknown_variables, available = self.get_unknown_variables(ns)
        if unknown_variables:
            message = unknown_variable_template.format(
                unknown=", ".join(map(repr, sorted(unknown_variables))),
                available=", ".join(map(repr, sorted(available))),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
            )
            raise ContextContractError(message)
        kwargs, errors = self.get_invalid_variables(ns)
        if errors:
            message = invalid_variable_template.format(
                variables=", ".join(map(repr, sorted(errors))),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
                violations="\n\n".join(
                    [
                        key + ":\n  " + "\n  ".join(str(errors[key]))
                        for key in sorted(errors)
                    ]
                ),
            )
            raise ContextContractError(message)
        return kwargs

    def get_arguments(self):
        # FIXME: Remove repeated arguments.
        arguments = []
        arguments.extend(self.arguments)
        for contract in self.subcontracts:
            arguments.extend(contract.get_arguments())
        return arguments

    def get_unknown_arguments(self, kwargs):
        available = set(self.arguments)
        unknown_arguments = set(kwargs) - available
        for contract in self.subcontracts:
            unknown_arguments = contract.get_unknown_arguments(unknown_arguments)
        return unknown_arguments

    def get_unknown_variables(self, ns):
        available = self.available_func(self.spec)
        unknown_variables = set(ns) - available
        for contract in self.subcontracts:
            unknown_variables, _ = contract.get_unknown_variables(unknown_variables)
        return unknown_variables, available

    def get_invalid_variables(self, ns):
        available = self.available_func(self.spec)
        kwargs, errors = self.validate_func(self.spec, ns, set(ns) & available)
        for contract in self.subcontracts:
            sub_kwargs, sub_errors = contract.get_invalid_variables(ns)
            kwargs.update(sub_kwargs)
            errors.update(sub_errors)
        return kwargs, errors


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


undefined_argument_template = """
These arguments should be declared in the context contract: {undefined}

Story method: {cls}.{method}

Story arguments: {arguments}
""".strip()


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


unknown_argument_template = """
These arguments are unknown: {unknown}

Story method: {cls}.{method}

Story composition arguments: {arguments}
""".strip()


unknown_argument_null_template = """
These arguments are unknown: {unknown}

Story method: {cls}.{method}

Story composition has no arguments.
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
