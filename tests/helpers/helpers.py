def make_collector(cls, methodname):

    storage = []
    method = getattr(cls, methodname)
    method = getattr(method, "__func__", method)

    def collect(self, ctx):
        storage.append(ctx)
        return method(self, ctx)

    class Collector(cls):
        pass

    collect.__name__ = methodname
    Collector.__name__ = cls.__name__
    setattr(Collector, methodname, collect)

    def getter():
        length = len(storage)
        error_template = "Method {methodname!r} was called {length} times"
        error_message = error_template.format(methodname=methodname, length=length)
        assert length == 1, error_message
        return storage[0]

    return Collector, getter
