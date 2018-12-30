from .exceptions import ContextContractError


def make_contract():
    return Contract()


def validate_arguments(arguments, args, kwargs):
    # FIXME: Should be a method of the `Contract` class.
    assert not (args and kwargs)

    if args:
        assert len(arguments) == len(args)
        return [(k, v) for k, v in zip(arguments, args)]

    assert set(arguments) == set(kwargs)
    return [(k, kwargs[k]) for k in arguments]


class Contract(object):
    def check_success_statement(self, method, ctx, ns):
        tries_to_override = set(ctx._Context__ns) & set(ns)
        if tries_to_override:
            message = variable_override_template.format(
                variables=", ".join(map(repr, sorted(tries_to_override))),
                cls=method.__self__.__class__.__name__,
                method=method.__name__,
            )
            raise ContextContractError(message)

    def deny_attribute_assign(self):
        raise ContextContractError(assign_attribute_template)

    def deny_attribute_delete(self):
        raise ContextContractError(delete_attribute_template)


variable_override_template = """
This variables already present in the context: {variables}

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
