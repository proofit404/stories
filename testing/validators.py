from operator import eq
from operator import gt
from operator import lt


def _is_integer(value):
    if isinstance(value, int):
        return value
    elif isinstance(value, str) and value.isdigit():
        return int(value)
    else:
        raise _ValidationError(value)


class _Operator:
    def __init__(self, constant):
        self.constant = constant

    def __call__(self, value):
        if self.compare(value, self.constant):
            return value
        else:
            raise _ValidationError(value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.constant})"


class _equal_to(_Operator):
    compare = eq


class _greater_than(_Operator):
    compare = gt


class _less_than(_Operator):
    compare = lt


class _ValidationError(Exception):
    ...
