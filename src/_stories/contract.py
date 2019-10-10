from inspect import isclass
from operator import itemgetter

from _stories.compat import CerberusSpec
from _stories.compat import MarshmallowSpec
from _stories.compat import pydantic_display
from _stories.compat import PydanticError
from _stories.compat import PydanticShape
from _stories.compat import PydanticSpec
from _stories.exceptions import ContextContractError


# FIXME: Handle protocol extension.  There should be way to say in the
# substory contract "this variable should be an integer" and in
# addition in the story "this integer should be greater then 7".  This
# way we also can require a certain substory to declare context
# variable for parent story.
#
# FIXME: Add fix suggestion to the bottom of the error message.
#
# FIXME: Support custom validation of complex relationships.  For
# example, `@pydantic.validator` of `password2` depends on
# `password1`.
#
# FIXME: Check that contracts collisions are checked in the situation:
#
# story
#   substory
#     substory with variable declaration
#   substory with this variable as an argument
#
# FIXME: Depending of the level of nesting the same substory can
# occurred multiple times at one argument in the contract
# representation.
#
# defaults:
#   typing.Union[typing.Dict[str, str], NoneType]  # Argument of ProcessImages.process
#   typing.Union[typing.Dict[str, str], NoneType]  # Argument of ProcessImages.process
#   typing.Union[typing.Dict[str, str], NoneType]  # Argument of ProcessImages.process
# raw_urls:
#   str  # Argument of FetchURLPreviews.fetch
#   str  # Argument of FetchURLPreviews.fetch
# files:
#   typing.Dict[str, typing.Union[str, int, typing.Any]]  # Argument of ProcessVideos.process  # noqa: E501
#   typing.Dict[str, typing.Union[str, int, typing.Any]]  # Argument of ProcessImages.process  # noqa: E501
#   typing.Dict[str, typing.Union[str, int, typing.Any]]  # Argument of ProcessImages.process  # noqa: E501
#   typing.Dict[str, typing.Union[str, int, typing.Any]]  # Argument of ProcessImages.process  # noqa: E501
#
# FIXME: Fix pydantic error messages.
#
# In [1]: class Context(pydantic.BaseModel):
#    ...:     files: typing.Dict[str, typing.Dict[str, typing.Union[str, int, typing.BinaryIO]]]  # noqa: E501
#    ...:
#
# In [2]: Context(files={"a": {'name': B(name='test'), 'size': 1}})
# ---------------------------------------------------------------------------
# ValidationError: 3 validation errors
# files -> a -> name
#   str type expected (type=type_error.str)
# files -> a -> name
#   value is not a valid integer (type=type_error.integer)
# files -> a -> name
#   instance of BinaryIO expected (type=type_error.arbitrary_type; expected_arbitrary_type=BinaryIO)  # noqa: E501
#
# FIXME: Test all field representation for all supported libraries.
# I.e. Dict, List, Tuple, Integer, String, etc.
#
# FIXME: Alias validation creates new object for each alias.  So they
# became not aliases.
#
# FIXME: Parent story can't define an argument, if child story already
# defined variable with the same name.
#
# FIXME: When Success argument is broken we should show validator of
# what argument of what substory is broken.  Because it's really hard
# to track down it in a deep story composition.
#
# FIXME: Nested collision detector doesn't support identity check for
# neighbor substories.  Only parent-child for now.
#
# class Subs
#   @story
#   def foo(I):
#
#   @story
#   def bar(I):
#
#   @contract_in(Subs)
#   class Context:
#     bar: int
#
# class Parent:
#   @story
#   def quiz(I):
#     I.foo
#     I.bar   <--- `bar` will be treated as repeated variable.
#
# NOTE: `noqa` comments are not part of the program output.


# Validators.


class PydanticValidator(object):
    def __init__(self, spec, field):
        self.spec = spec
        self.field = field

    def __call__(self, value):
        return self.field.validate(value, {}, loc=self.field.alias, cls=self.spec)

    def __repr__(self):
        if self.field.shape is PydanticShape.SINGLETON:
            template = "%s"
        elif self.field.shape is PydanticShape.LIST:
            template = "List[%s]"
        elif self.field.shape is PydanticShape.SET:
            template = "Set[%s]"
        elif self.field.shape is PydanticShape.MAPPING:
            template = "Mapping[%s]"
        elif self.field.shape is PydanticShape.TUPLE:
            template = "Tuple[%s]"
        elif self.field.shape is PydanticShape.TUPLE_ELLIPS:
            template = "Tuple[%s, ...]"
        elif self.field.shape is PydanticShape.SEQUENCE:
            template = "Sequence[%s]"
        return template % (pydantic_display(self.field.type_),)


class MarshmallowValidator(object):
    def __init__(self, spec, field):
        self.spec = spec
        self.field = field

    def __call__(self, value):
        values, errors = self.spec().load({self.field: value})
        return values.get(self.field), errors.get(self.field)

    def __repr__(self):
        field = self.spec._declared_fields[self.field]
        return field.__class__.__name__


class CerberusValidator(object):
    def __init__(self, spec, field):
        self.spec = spec
        self.field = field

    def __call__(self, value):
        validated = CerberusSpec()
        validated.validate({self.field: value}, self.spec.schema.schema)
        return validated.document.get(self.field), validated.errors.get(self.field)

    def __repr__(self):
        schema = self.spec.schema.schema[self.field]
        field_type = schema["type"]
        if "schema" in schema and "type" in schema["schema"]:
            field_type += "[" + schema["schema"]["type"] + "]"
        return field_type


class RawValidator(object):
    def __init__(self, validator):
        self.validator = validator

    def __call__(self, value):
        return self.validator(value)

    def __repr__(self):
        return self.validator.__name__


# Disassemble.


def disassemble_pydantic(spec):
    result = {}
    for name, field in spec.__fields__.items():
        result[name] = PydanticValidator(spec, field)
    return result


def disassemble_marshmallow(spec):
    result = {}
    for name in spec._declared_fields:
        result[name] = MarshmallowValidator(spec, name)
    return result


def disassemble_cerberus(spec):
    result = {}
    for name in spec.schema:
        result[name] = CerberusValidator(spec, name)
    return result


def disassemble_raw(spec):
    result = {}
    for name, validator in spec.items():
        result[name] = RawValidator(validator)
    return result


# Execute.


def make_contract(cls_name, name, arguments, spec):
    __tracebackhide__ = True
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
    __tracebackhide__ = True
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
        self.argset = {
            arg: {(None, self.cls_name, self.name)} for arg in self.arguments
        }

    def check_story_call(self, kwargs):
        __tracebackhide__ = True
        # FIXME: Check required arguments here.
        unknown_arguments = set(kwargs) - set(self.argset)
        if unknown_arguments:
            message = unknown_argument_template.format(
                unknown=", ".join(sorted(unknown_arguments)),
                cls=self.cls_name,
                method=self.name,
                contract=self,
            )
            raise ContextContractError(message)
        return kwargs

    def check_substory_call(self, ctx):
        __tracebackhide__ = True
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
        __tracebackhide__ = True
        tries_to_override = set(ctx._Context__ns) & set(ns)
        if tries_to_override:
            message = variable_override_template.format(
                variables=", ".join(map(repr, sorted(tries_to_override))),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
                ctx=ctx,
            )
            raise ContextContractError(message)
        return ns

    def __repr__(self):
        return self.format_contract_fields(self.argset)

    def format_contract_fields(self, *fieldset):
        if not self.argset:
            return "Contract()"
        lines = ["Contract:"]
        arguments = sorted(
            [field for fields in fieldset for field in fields if field in self.argset]
        )
        for argument in arguments:
            # FIXME: This does not work for story composition when
            # many stories has the same argument.
            ((validator, cls_name, name),) = self.argset[argument]
            lines.append("  %s  # Argument of %s.%s" % (argument, cls_name, name))
        return "\n".join(lines)


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
        self.argset = {}
        for arg in self.arguments:
            self.argset[arg] = {(self.spec[arg], self.cls_name, self.name)}
            del self.spec[arg]

    def make_declared(self):
        self.declared = {
            variable: (self.cls_name, self.name, repr(validator))
            for variable, validator in self.spec.items()
        }

    def check_story_call(self, kwargs):
        __tracebackhide__ = True
        super(SpecContract, self).check_story_call(kwargs)
        result, errors = self.validate(kwargs)
        if errors:
            message = invalid_argument_template.format(
                variables=", ".join(map(repr, sorted(errors))),
                cls=self.cls_name,
                method=self.name,
                violations=format_violations(kwargs, errors),
                contract=self.format_contract_fields(errors),
            )
            raise ContextContractError(message)
        return result

    def check_success_statement(self, method, ctx, ns):
        __tracebackhide__ = True
        super(SpecContract, self).check_success_statement(method, ctx, ns)
        unknown = self.identify(ns)
        if unknown:
            message = unknown_variable_template.format(
                unknown=", ".join(map(repr, sorted(unknown))),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
                contract=self,
            )
            raise ContextContractError(message)
        kwargs, errors = self.validate(ns)
        if errors:
            message = invalid_variable_template.format(
                variables=", ".join(map(repr, sorted(errors))),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
                violations=format_violations(ns, errors),
                contract=self.format_contract_fields(errors),
            )
            raise ContextContractError(message)
        return kwargs

    def identify(self, ns):
        available = set(self.spec) | set(self.argset)
        unknown = set(ns) - available
        return unknown

    def validate(self, ns):
        __tracebackhide__ = True
        result, errors, seen, conflict = {}, {}, [], {}
        for key, value in ns.items():
            if key in self.spec:
                self.validate_spec(result, errors, seen, key, value)
            else:
                self.validate_argset(result, errors, seen, conflict, key, value)
        if conflict:
            conflict_vars = sorted({j for i in conflict.values() for j in i})
            message = normalization_conflict_template.format(
                conflict=", ".join(map(repr, conflict_vars)),
                results="\n\n".join(
                    "%s.%s:\n%s"
                    % (
                        cls,
                        method,
                        "\n".join(" - %s: %r" % (i, result[i]) for i in sorted(result)),
                    )
                    for (cls, method), result in (
                        (i, conflict[i]) for i in sorted(conflict)
                    )
                ),
                contract=self.format_contract_fields(conflict_vars),
            )
            raise ContextContractError(message)
        return result, errors

    def validate_spec(self, result, errors, seen, key, value):
        new_value, error = self.spec[key](value)
        if error:
            errors[key] = error
        else:
            self.assign_result(result, seen, key, value, new_value)

    def validate_argset(self, result, errors, seen, conflict, key, value):
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
            self.assign_result(result, seen, key, value, new_value)

    def assign_result(self, result, seen, key, value, new_value):
        for seen_key, seen_value in seen:
            if value is seen_value:
                seen_new_value = result[seen_key]
                if (
                    type(new_value) is type(seen_new_value)
                    and new_value == seen_new_value
                ):
                    result[key] = seen_new_value
                    return
        result[key] = new_value
        seen.append((key, value))

    def __repr__(self):
        return self.format_contract_fields(self.argset, self.declared)

    def format_contract_fields(self, *fieldset):
        lines = ["Contract:"]
        arguments = sorted(
            [field for fields in fieldset for field in fields if field in self.argset]
        )
        for argument in arguments:
            validators = self.argset[argument]
            if len(validators) == 1:
                ((validator, cls_name, name),) = validators
                lines.append(
                    "  %s: %r  # Argument of %s.%s"
                    % (argument, validator, cls_name, name)
                )
            else:
                lines.append("  %s:" % (argument,))
                for validator in sorted(validators, key=itemgetter(1, 2)):
                    lines.append("    %r  # Argument of %s.%s" % validator)
        variables = sorted(
            [field for fields in fieldset for field in fields if field in self.declared]
        )
        for variable in variables:
            cls_name, name, field_name = self.declared[variable]
            lines.append(
                "  %s: %s  # Variable in %s.%s" % (variable, field_name, cls_name, name)
            )
        return "\n".join(lines)


def format_violations(ns, errors):
    result = []

    def normalize(value, indent, list_item=False, dict_value=False):
        if isinstance(value, dict):
            normalize_dict(value, indent + 2)
        elif isinstance(value, list):
            normalize_list(value, indent if list_item else indent + 2)
        elif isinstance(value, PydanticError):
            indent = indent + 2 if dict_value else indent
            normalize_pydantic(value, indent)
        else:
            indent = indent + 2 if dict_value else indent
            normalize_str(value, indent)

    def normalize_dict(value, indent, sep=None):
        for key in sorted(value):
            normalize(str(key) + ":", indent)
            if sep is not None:
                normalize(repr(ns[key]), indent, dict_value=True)
            normalize(value[key], indent, dict_value=True)
            if sep is not None:
                normalize_str(sep, 0)

    def normalize_list(value, indent):
        for elem in value:
            normalize(elem, indent, list_item=True)

    def normalize_pydantic(value, indent):
        normalize_str(value.msg, indent)

    def normalize_str(value, indent):
        result.append(" " * indent + value)

    normalize_dict(errors, 0, "")

    return "\n".join(result).strip()


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
            contract=format_contract(parent),
            other_cls=child.cls_name,
            other_method=child.name,
            other_contract=format_contract(child),
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


def format_contract(contract):
    if type(contract) is SpecContract:
        if isclass(contract.origin):
            return contract.origin.__bases__[0]
        else:
            return type(contract.origin)
    else:
        return None


def maybe_extend_downstream_argsets(methods, root):
    if type(root) is NullContract:
        return
    for _method, contract, _protocol in methods:
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

{ctx!r}
""".strip()


unknown_variable_template = """
These variables were not defined in the context contract: {unknown}

Function returned value: {cls}.{method}

Use different names for Success() keyword arguments or add these names to the contract.

{contract!r}
""".strip()


unknown_argument_template = """
These arguments are unknown: {unknown}

Story method: {cls}.{method}

{contract!r}
""".strip()


invalid_variable_template = """
These variables violates context contract: {variables}

Function returned value: {cls}.{method}

Violations:

{violations}

{contract}
""".strip()


invalid_argument_template = """
These arguments violates context contract: {variables}

Story method: {cls}.{method}

Violations:

{violations}

{contract}
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

{contract}
""".strip()
