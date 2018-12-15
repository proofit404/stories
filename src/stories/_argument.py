def argument(*name):
    def decorator(f):
        if not hasattr(f, "arguments"):
            f.arguments = []
        f.arguments = list(reversed(name)) + f.arguments
        return f

    return decorator
