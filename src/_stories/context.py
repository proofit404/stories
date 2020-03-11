# -*- coding: utf-8 -*-
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
    lines = ["Story argument"] * len(ns)

    def getattr_method(self, name):
        try:
            return ns[name]
        except KeyError:
            raise AttributeError(
                ATTRIBUTE_ERROR_MSG.format(obj="Context", attr=name, ctx=self)
            )

    def repr_method(self):
        return (
            history_representation(history) + "\n\n" + context_representation(ns, lines)
        )

    def dir_method(self):
        spec = type("Context", (object,), {})
        parent = set(dir(spec()))
        scope = set(ns)
        attributes = sorted(parent | scope)
        return attributes

    def bool_method(self):
        # FIXME: It isn't a mutation error.
        #
        # FIXME: Support custom report function.
        message = comparison_template.format(available=", ".join(map(repr, ns)))
        raise MutationError(message)

    return (
        type(
            "Context",
            (object,),
            {
                "__getattr__": getattr_method,
                "__setattr__": setattr_method,
                "__delattr__": delattr_method,
                "__repr__": repr_method,
                "__dir__": dir_method,
                "__bool__": bool_method,
                "__nonzero__": bool_method,  # Python 2.
            },
        )(),
        ns,
        lines,
    )


def setattr_method(self, name, value):
    raise MutationError(assign_attribute_message)


def delattr_method(self, name):
    raise MutationError(delete_attribute_message)


def assign_namespace(ns, lines, method, kwargs):
    ns.update((arg, kwargs[arg]) for arg in sorted(kwargs))
    line = "Set by {}.{}".format(method.__self__.__class__.__name__, method.__name__)
    lines.extend([line] * len(kwargs))


def history_representation(history):
    return "\n".join(history.lines)


def context_representation(ns, lines, repr_func=repr):
    if not lines:
        return "Context()"
    seen = []
    items = []
    longest = 0
    for key, value in ns.items():
        for seen_key, seen_value in seen:
            if value is seen_value:
                item = "`{}` alias".format(seen_key)
                break
        else:
            item = repr_func(value)
        too_long = len(key) + len(item) + 4 > 88
        has_new_lines = "\n" in item
        if too_long or has_new_lines:
            head = key + ":"
            tail = "\n" + indent(item, "    ")
        else:
            head = "{}: {}".format(key, item)
            tail = ""
        if type(value) not in [type(None), bool, int, float, Decimal]:
            seen.append((key, value))
        items.append((head, tail))
        head_length = len(head)
        if head_length > longest:
            longest = head_length
    lines = [
        "  {}  # {}{}".format(head.ljust(longest), line, tail)
        for (head, tail), line in zip(items, lines)
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
