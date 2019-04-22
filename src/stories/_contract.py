from collections import OrderedDict
from functools import partial

from ._compat import CerberusSpec, MarshmallowSpec, PydanticError, PydanticSpec
from .exceptions import ContextContractError


# FIXME:
#
# [ ] Handle protocol extension.  There should be way to say in the
#     substory contract "this variable should be an integer" and in
#     addition in the story "this integer should be greater then 7".
#     This way we also can require a certain substory to declare
#     context variable for parent story.
#
# [ ] Add fix suggestion to the bottom of the error message.
#
# [ ] Support custom validation of complex relationships.  For
#     example, `@pydantic.validator` of `password2` depends on
#     `password1`.


# Disassemble.


def disassemble_pydantic(spec):
    def validator(f, v):
        return f.validate(v, {}, loc=f.alias, cls=spec)

    result = {}
    for name, field in spec.__fields__.items():
        result[name] = partial(validator, field)
    return result


def disassemble_marshmallow(spec):
    def validator(f, v):
        values, errors = spec().load({f: v})
        return values.get(f), errors.get(f)

    result = {}
    for name in spec._declared_fields:
        result[name] = partial(validator, name)
    return result


def disassemble_cerberus(spec):
    def validator(f, v):
        validated = CerberusSpec()
        validated.validate({f: v}, spec.schema.schema)
        return validated.document.get(f), validated.errors.get(f)

    result = {}
    for name in spec.schema:
        result[name] = partial(validator, name)
    return result


def disassemble_raw(spec):
    return spec.copy()


# Execute.


def make_contract(cls_name, name, arguments, spec):
    if spec is None:
        return NullContract(cls_name, name, arguments)
    elif isinstance(spec, PydanticSpec):
        disassembled = disassemble_pydantic(spec)
    elif isinstance(spec, MarshmallowSpec):
        disassembled = disassemble_marshmallow(spec)
    elif isinstance(spec, CerberusSpec):
        disassembled = disassemble_cerberus(spec)
    elif isinstance(spec, dict):
        disassembled = disassemble_raw(spec)
    check_arguments_definitions(cls_name, name, arguments, disassembled)
    return SpecContract(cls_name, name, arguments, disassembled, spec)


def check_arguments_definitions(cls_name, name, arguments, spec):
    undefined = set(arguments) - set(spec)
    if undefined:
        message = undefined_argument_template.format(
            undefined=", ".join(sorted(undefined)),
            cls=cls_name,
            method=name,
            arguments=", ".join(arguments),
        )
        raise ContextContractError(message)


class NullContract(object):
    def __init__(self, cls_name, name, arguments):
        self.cls_name = cls_name
        self.name = name
        self.arguments = arguments
        self.make_argset()

    def make_argset(self):
        self.argset = OrderedDict((arg, set()) for arg in self.arguments)

    def check_story_call(self, kwargs):
        # FIXME: Check required arguments here.
        unknown_arguments = set(kwargs) - set(self.argset)
        if unknown_arguments:
            if self.arguments:
                # FIXME: What if arguments were defined only in the substory?
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
        return ns


class SpecContract(NullContract):
    # FIXME: Deny empty disassembled spec.  If there is such need, we
    # should replace `NullContract` with empty `SpecContract`
    # ourselves.
    def __init__(self, cls_name, name, arguments, spec, origin):
        self.spec = spec
        self.origin = origin
        super(SpecContract, self).__init__(cls_name, name, arguments)
        self.make_declared()

    def make_argset(self):
        super(SpecContract, self).make_argset()
        for arg in self.arguments:
            self.argset[arg].add((self.spec[arg], self.cls_name, self.name))
            del self.spec[arg]

    def make_declared(self):
        self.declared = OrderedDict(
            (variable, (self.cls_name, self.name)) for variable in self.spec
        )

    def check_story_call(self, kwargs):
        super(SpecContract, self).check_story_call(kwargs)
        kwargs, errors = self.validate(kwargs)
        if errors:
            message = invalid_argument_template.format(
                variables=", ".join(map(repr, sorted(errors))),
                cls=self.cls_name,
                method=self.name,
                violations=format_violations(errors),
            )
            raise ContextContractError(message)
        return kwargs

    def check_success_statement(self, method, ctx, ns):
        super(SpecContract, self).check_success_statement(method, ctx, ns)
        unknown, available = self.identify(ns)
        if unknown:
            message = unknown_variable_template.format(
                unknown=", ".join(map(repr, sorted(unknown))),
                available=", ".join(map(repr, sorted(available))),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
            )
            raise ContextContractError(message)
        kwargs, errors = self.validate(ns)
        if errors:
            message = invalid_variable_template.format(
                variables=", ".join(map(repr, sorted(errors))),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
                violations=format_violations(errors),
            )
            raise ContextContractError(message)
        return kwargs

    def identify(self, ns):
        available = set(self.spec) | set(self.argset)
        unknown = set(ns) - available
        return unknown, available

    def validate(self, ns):
        result, errors, conflict = {}, {}, {}
        for key, value in ns.items():
            if key in self.spec:
                self.validate_spec(result, errors, key, value)
            else:
                self.validate_argset(result, errors, conflict, key, value)
        if conflict:
            message = normalization_conflict_template.format(
                conflict=", ".join(
                    map(repr, sorted(set(j for i in conflict.values() for j in i)))
                ),
                results="\n\n".join(
                    normalization_conflict_result_template.format(
                        cls=cls,
                        method=method,
                        result="\n".join(
                            "  - %s: %r" % (i, result[i]) for i in sorted(result)
                        ),
                    )
                    for (cls, method), result in conflict.items()
                ),
            )
            raise ContextContractError(message)
        return result, errors

    def validate_spec(self, result, errors, key, value):
        new_value, error = self.spec[key](value)
        if error:
            errors[key] = error
        else:
            result[key] = new_value

    def validate_argset(self, result, errors, conflict, key, value):
        new_values, has_error = [], False
        for validator, cls_name, name in self.argset[key]:
            new_value, error = validator(value)
            if error:
                has_error = True
                errors[key] = error
            else:
                new_values.append((new_value, cls_name, name))
        if new_values:
            first, others = new_values[0], new_values[1:]
            for other in others:
                if first[0] != other[0]:
                    conflict.setdefault((first[1], first[2]), {})
                    conflict[(first[1], first[2])][key] = first[0]
                    conflict.setdefault((other[1], other[2]), {})
                    conflict[(other[1], other[2])][key] = other[0]
        if not has_error:
            result[key] = new_value


def format_violations(errors):
    result = []

    def normalize(value, indent, dict_value=False):
        if isinstance(value, dict):
            normalize_dict(value, indent + 2)
        elif isinstance(value, list):
            normalize_list(value, indent + 2)
        elif isinstance(value, PydanticError):
            indent = indent + 2 if dict_value else indent
            normalize_pydantic(value, indent)
        else:
            indent = indent + 2 if dict_value else indent
            normalize_str(value, indent)

    def normalize_dict(value, indent, sep=None):
        for key in sorted(value):
            normalize(str(key) + ":", indent)
            normalize(value[key], indent, dict_value=True)
            if sep is not None:
                normalize_str(sep, 0)

    def normalize_list(value, indent):
        for elem in value:
            normalize(elem, indent)

    def normalize_pydantic(value, indent):
        normalize_str(value.msg, indent)

    def normalize_str(value, indent):
        result.append(" " * indent + value)

    normalize_dict(errors, 0, "")

    return "\n".join(result)


# Wrap.


def combine_contract(parent, child):
    if type(parent) is NullContract and type(child) is NullContract:
        combine_argsets(parent, child)
        return
    elif (
        type(parent) is SpecContract
        and type(child) is SpecContract
        and parent.origin is child.origin
    ):
        combine_argsets(parent, child)
        return
    elif (
        type(parent) is SpecContract
        and type(child) is SpecContract
        and any(
            isinstance(parent.origin, spec_type) and isinstance(child.origin, spec_type)
            for spec_type in [PydanticSpec, MarshmallowSpec, CerberusSpec, dict]
        )
    ):
        repeated = set(parent.declared) & set(child.declared)
        if repeated:
            # FIXME: Repeated variables can occur in three different
            # classes.
            key = next(iter(repeated))
            message = incompatible_contracts_template.format(
                repeated=", ".join(map(repr, sorted(repeated))),
                cls=parent.declared[key][0],
                method=parent.declared[key][1],
                other_cls=child.declared[key][0],
                other_method=child.declared[key][1],
            )
            raise ContextContractError(message)
        combine_argsets(parent, child)
        combine_declared(parent, child)
    else:
        message = type_error_template.format(
            cls=parent.cls_name,
            method=parent.name,
            contract=parent.spec if type(parent) is SpecContract else None,
            other_cls=child.cls_name,
            other_method=child.name,
            other_contract=child.spec if type(child) is SpecContract else None,
        )
        raise ContextContractError(message)


def combine_argsets(parent, child):
    for key in set(parent.argset) & set(child.argset):
        parent.argset[key].update(child.argset[key])
        child.argset[key].update(parent.argset[key])
    for key in set(parent.argset) - set(child.argset):
        child.argset[key] = parent.argset[key]
    for key in set(child.argset) - set(parent.argset):
        parent.argset[key] = child.argset[key]


def combine_declared(parent, child):
    parent.declared.update(child.declared)


def maybe_extend_downstream_argsets(methods, root):
    if type(root) is NullContract:
        return
    for method, contract, protocol in methods:
        combine_argsets(root, contract)


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


normalization_conflict_template = """
These arguments have normalization conflict: {conflict}

{results}
""".strip()


normalization_conflict_result_template = """
Story method: {cls}.{method}

Story normalization result:
{result}
""".strip()
