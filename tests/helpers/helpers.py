def make_collector(cls, methodname):

    storage = []
    method = getattr(cls, methodname)
    method = getattr(method, "__func__", method)

    def collect(self, ctx):
        storage.append(self)
        return method(self, ctx)

    class Collector(cls):
        pass

    collect.__name__ = methodname
    Collector.__name__ = cls.__name__
    setattr(Collector, methodname, collect)

    def getter():
        length = len(storage)
        assert length == 1, " ".join(
            ["Method", "'" + methodname + "'", "was", "called", str(length), "times"]
        )
        return storage[0]

    return Collector, getter
