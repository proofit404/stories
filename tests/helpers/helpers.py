def make_collector(cls, methodname):

    storage = []
    method = getattr(cls, methodname)

    def collect(self):
        storage.append(self)
        return method(self)

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
