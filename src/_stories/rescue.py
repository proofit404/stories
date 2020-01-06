def rescue(f, error):
    if not hasattr(f, 'rescues'):
        f.rescues = {}

    def decorator(rescue_f):
        f.rescues[error] = rescue_f
        return rescue_f

    return decorator


def get_rescues(f):
    rescues = {}
    for error, rescue in getattr(f, "rescues", {}).items():
        if callable(error):
            rescues[error()] = rescue
        else:
            rescues[error] = rescue
    
    return rescues
