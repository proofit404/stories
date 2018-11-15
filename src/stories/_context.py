from collections import OrderedDict

from ._marker import undefined
from ._repr import context_representation


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
        return "\n\n".join([repr(self.history), context_representation(self)])

    def __dir__(self):
        parent = set(dir(undefined))
        current = set(self.__dict__) - {"ns", "history", "lines"}
        scope = set(self.ns)
        attributes = sorted(parent | current | scope)
        return attributes


def validate_arguments(arguments, args, kwargs):

    assert not (args and kwargs)

    if args:
        assert len(arguments) == len(args)
        return [(k, v) for k, v in zip(arguments, args)]

    assert set(arguments) == set(kwargs)
    return [(k, kwargs[k]) for k in arguments]
