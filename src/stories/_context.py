from collections import OrderedDict

from ._marker import undefined
from ._repr import context_representation, history_representation


class Context(object):
    def __init__(self, ns, history):
        self.ns = OrderedDict(ns)
        self.history = history
        self.lines = ["Story argument"] * len(ns)

    def __getattr__(self, name):
        return self.ns[name]

    def __eq__(self, other):
        return self.ns == other

    def __iter__(self):
        return iter(self.ns)

    def __repr__(self):
        return (
            history_representation(self.history) + "\n\n" + context_representation(self)
        )

    def __dir__(self):
        parent = set(dir(undefined))
        current = set(self.__dict__) - {"ns", "history", "lines"}
        scope = set(self.ns)
        attributes = sorted(parent | current | scope)
        return attributes
