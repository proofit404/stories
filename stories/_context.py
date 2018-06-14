from ._marker import undefined


class Context(object):
    def __init__(self, ns):
        self.ns = ns
        self.lines = [(key, "Story argument") for key in ns]

    def __getattr__(self, name):
        return self.ns[name]

    def __eq__(self, other):
        return self.ns == other

    def __repr__(self):
        if not self.lines:
            return self.__class__.__name__ + "()"
        assignments = [
            ("%s = %s" % (key, repr(self.ns[key])), line) for key, line in self.lines
        ]
        longest = max(map(lambda x: len(x[0]), assignments))
        return "\n".join(
            [self.__class__.__name__ + ":"]
            + [
                "    %s  # %s" % (assignment.ljust(longest), line)
                for assignment, line in assignments
            ]
        )

    def __dir__(self):
        parent = set(dir(undefined))
        current = set(self.__dict__) - {"ns", "lines", "__position__"}
        scope = set(self.ns)
        attributes = sorted(parent | current | scope)
        return attributes
