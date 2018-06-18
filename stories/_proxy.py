def make_proxy(obj, ctx):
    class Proxy:
        def __repr__(self):
            return repr(self.ctx.history)

    Proxy.__name__ = obj.__class__.__name__
    proxy = Proxy()
    for name, attr in obj.__dict__.items():
        setattr(proxy, name, attr)
    proxy.ctx = ctx
    return proxy
