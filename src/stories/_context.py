from collections import OrderedDict

from ._repr import context_representation, history_representation


class Context(object):
    def __init__(self, ns, history, contract):
        self.__dict__["ns"] = OrderedDict(ns)
        self.__dict__["history"] = history
        self.__dict__["lines"] = ["Story argument"] * len(ns)
        self.__dict__["contract"] = contract

    def assign(self, method, kwargs):
        self.ns.update(kwargs)
        line = "Set by %s.%s" % (method.__self__.__class__.__name__, method.__name__)
        self.lines.extend([line] * len(kwargs))

    def __getattr__(self, name):
        return self.ns[name]

    def __setattr__(self, name, value):
        self.contract.deny_attribute_assign()

    def __delattr__(self, name):
        self.contract.deny_attribute_delete()

    def __eq__(self, other):
        return self.ns == other

    def __iter__(self):
        return iter(self.ns)

    def __repr__(self):
        return (
            history_representation(self.history) + "\n\n" + context_representation(self)
        )

    def __dir__(self):
        spec = type("Context", (object,), {})
        parent = set(dir(spec()))
        current = set(self.__dict__) - {"ns", "history", "lines", "contract"}
        scope = set(self.ns)
        attributes = sorted(parent | current | scope)
        return attributes
