import textwrap
from collections import OrderedDict
from decimal import Decimal

from _stories.compat import indent
from _stories.exceptions import MutationError


ATTRIBUTE_ERROR_MSG = textwrap.dedent(
    """
    '{obj}' object has no attribute {attr}

    {ctx!r}
    """
).strip()


def make_context(contract, kwargs, history):
    kwargs = contract.check_story_call(kwargs)
    ns = OrderedDict(
        # FIXME: We should be able to remove `if` statement here.
        (arg, kwargs[arg])
        for arg in sorted(contract.argset)
        if arg in kwargs
    )
    ctx = Context()
    ctx.__dict__["_Context__ns"] = ns
    ctx.__dict__["_Context__history"] = history
    ctx.__dict__["_Context__lines"] = ["Story argument"] * len(ns)
    return ctx


class Context(object):
    def __getattr__(self, name):
        try:
            return self.__ns[name]
        except KeyError:
            raise AttributeError(
                ATTRIBUTE_ERROR_MSG.format(obj="Context", attr=name, ctx=self)
            )

    def __setattr__(self, name, value):
        raise MutationError(assign_attribute_message)

    def __delattr__(self, name):
        raise MutationError(delete_attribute_message)

    def __repr__(self):
        return history_representation(self) + "\n\n" + context_representation(self)

    def __dir__(self):
        spec = type("Context", (object,), {})
        parent = set(dir(spec()))
        current = set(self.__dict__) - {
            "_Context__ns",
            "_Context__history",
            "_Context__lines",
        }
        scope = set(self.__ns)
        attributes = sorted(parent | current | scope)
        return attributes

    def __bool__(self):
        message = comparison_template.format(available=", ".join(map(repr, self.__ns)))
        raise MutationError(message)

    __nonzero__ = __bool__


def assign_namespace(ctx, method, kwargs):
    ctx._Context__ns.update((arg, kwargs[arg]) for arg in sorted(kwargs))
    line = "Set by %s.%s" % (method.__self__.__class__.__name__, method.__name__)
    ctx._Context__lines.extend([line] * len(kwargs))


def history_representation(ctx):
    result = "\n".join(ctx._Context__history.lines)
    return result


def context_representation(ctx, repr_func=repr):
    if not ctx._Context__lines:
        return "Context()"
    seen = []
    items = []
    longest = 0
    for key, value in ctx._Context__ns.items():
        for seen_key, seen_value in seen:
            if value is seen_value:
                item = "`%s` alias" % (seen_key,)
                break
        else:
            item = repr_func(value)
        too_long = len(key) + len(item) + 4 > 88
        has_new_lines = "\n" in item
        if too_long or has_new_lines:
            head = key + ":"
            tail = "\n" + indent(item, "    ")
        else:
            head = "%s: %s" % (key, item)
            tail = ""
        if type(value) not in [type(None), bool, int, float, Decimal]:
            seen.append((key, value))
        items.append((head, tail))
        head_length = len(head)
        if head_length > longest:
            longest = head_length
    lines = [
        "  %s  # %s%s" % (head.ljust(longest), line, tail)
        for (head, tail), line in zip(items, ctx._Context__lines)
    ]
    return "\n".join(["Context:"] + lines)


# Messages.


assign_attribute_message = """
Context object is immutable.

Use Success() keyword arguments to expand its scope.
""".strip()


delete_attribute_message = """
Context object is immutable.

Variables can not be removed from Context.
""".strip()


comparison_template = """
Context object can not be used in boolean comparison.

Available variables: {available}
""".strip()
