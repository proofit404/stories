def _is_integer(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, str) and value.isdigit():
        return int(value)
    else:
        raise _ValidationError(value)


class _ValidationError(Exception):
    ...
