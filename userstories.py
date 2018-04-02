def story(f):

    def wrapper(self, *args):
        arguments = getattr(f, "arguments", [])
        assert len(arguments) == len(args)
        kwargs = {k: v for k, v in zip(arguments, args)}
        inp = Input(kwargs)
        proxy = Proxy(self, inp)
        f(proxy)
        return proxy.value

    return wrapper


def argument(name):

    def decorator(f):
        if not hasattr(f, "arguments"):
            f.arguments = []
        f.arguments.insert(0, name)
        return f

    return decorator


class Result:

    def __init__(self, value=None):
        self.value = value


class Success:

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class Failure:

    def __repr__(self):
        return self.__class__.__name__


class Input:

    def __init__(self, ns):
        self.ns = ns

    def __getattr__(self, name):
        return self.ns[name]


class Proxy:

    def __init__(self, other, inp):
        self.other = other
        self.input = inp

    def __getattr__(self, name):
        attr = getattr(self.other.__class__, name)
        # TODO: Check if this is a method.
        return MethodWrapper(self, attr)


class MethodWrapper:

    def __init__(self, proxy, method):
        self.proxy = proxy
        self.method = method

    def __call__(self):
        if hasattr(self.proxy, "done"):
            return self.proxy.value

        result = self.method(self.proxy)
        if isinstance(result, Failure):
            value = self.proxy.value = result
            self.proxy.done = True
        elif isinstance(result, Result):
            value = self.proxy.value = result.value
            self.proxy.done = True
        else:
            self.proxy.input.ns.update(result.kwargs)
            value = self.proxy.value = None
        return value
