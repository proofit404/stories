from collections import OrderedDict

from .exceptions import MutationError


def make_context(arguments, kwargs, history):
    ns = OrderedDict((arg, kwargs[arg]) for arg in arguments if arg in kwargs)
    ctx = Context()
    ctx.__dict__["_Context__ns"] = ns
    ctx.__dict__["_Context__history"] = history
    ctx.__dict__["_Context__lines"] = ["Story argument"] * len(kwargs)
    return ctx


class Context(object):
    def __getattr__(self, name):
        return self.__ns[name]

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


def assign_namespace(ctx, method, kwargs):
    ctx._Context__ns.update(kwargs)
    line = "Set by %s.%s" % (method.__self__.__class__.__name__, method.__name__)
    ctx._Context__lines.extend([line] * len(kwargs))


def history_representation(ctx):
    result = "\n".join(ctx._Context__history.lines)
    return result


def context_representation(ctx):
    if not ctx._Context__lines:
        return "Context()"
    items = [
        "%s = %s" % (key, repr(value)) for (key, value) in ctx._Context__ns.items()
    ]
    longest = max(map(len, items))
    lines = [
        "    %s  # %s" % (item.ljust(longest), line)
        for item, line in zip(items, ctx._Context__lines)
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
