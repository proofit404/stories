from collections import OrderedDict

from ._contract import deny_attribute_assign, deny_attribute_delete
from ._repr import context_representation, history_representation


def assign_namespace(ctx, method, kwargs):
    ctx._Context__ns.update(kwargs)
    line = "Set by %s.%s" % (method.__self__.__class__.__name__, method.__name__)
    ctx._Context__lines.extend([line] * len(kwargs))


class Context(object):
    def __init__(self, ns, history):
        self.__dict__["_Context__ns"] = OrderedDict(ns)
        self.__dict__["_Context__history"] = history
        self.__dict__["_Context__lines"] = ["Story argument"] * len(ns)

    def __getattr__(self, name):
        return self.__ns[name]

    def __setattr__(self, name, value):
        deny_attribute_assign()

    def __delattr__(self, name):
        deny_attribute_delete()

    def __repr__(self):
        return (
            history_representation(self.__history)
            + "\n\n"
            + context_representation(self.__ns, self.__lines)
        )

    def __dir__(self):
        spec = type("Context", (object,), {})
        parent = set(dir(spec()))
        current = set(self.__dict__) - {
            "_Context__ns",
            "_Context__history",
            "_Context__lines",
            "_Context__contract",
        }
        scope = set(self.__ns)
        attributes = sorted(parent | current | scope)
        return attributes
