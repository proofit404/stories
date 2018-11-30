from enum import Enum, unique


errors = ["foo", "bar", "baz"]


@unique
class Errors(Enum):
    foo = 1
    bar = 2
    baz = 3
