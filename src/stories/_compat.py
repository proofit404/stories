# NOTE: Every type ignore in this module is necessary due to
# false-positive bugs in mypy.  Feel free to remove them as they'll be
# fixed.  See GitHub issues for more info:
# `https://github.com/python/mypy/issues/1105`,
# `https://github.com/python/mypy/issues/1106`,
# `https://github.com/python/mypy/issues/1107`.

from typing import Callable, Type


try:
    from enum import Enum, EnumMeta  # type: ignore
except ImportError:
    # We are on Python 2.7 and enum34 package is not installed.
    class Enum(object):
        pass

    class EnumMeta(object):
        pass


try:
    from pydantic.error_wrappers import ErrorWrapper as PydanticError  # type: ignore
    from pydantic.fields import Shape as PydanticShape  # type: ignore
    from pydantic.main import MetaModel as PydanticSpec
    from pydantic.utils import display_as_type as pydantic_display
except ImportError:
    # Pydantic package is not installed.
    class PydanticSpec(object):
        pass

    class PydanticError(object):
        pass

    class PydanticShape(object):
        pass

    def pydantic_display(v):
        # type: (Type) -> str
        pass


try:
    from marshmallow.schema import SchemaMeta as MarshmallowSpec
except ImportError:
    # Marshmallow package is not installed.
    class MarshmallowSpec(object):
        pass


try:
    from cerberus import Validator as CerberusSpec
except ImportError:
    # Cerberus package is not installed.
    class CerberusSpec(object):
        pass


try:
    from textwrap import indent
except ImportError:
    # We are on Python 2.7
    def indent(text, prefix, predicate=lambda x: True):
        # type: (str, str, Callable[[str], bool]) -> str
        return "".join(map(lambda l: prefix + l, text.splitlines(True)))


try:
    from prettyprinter import pformat
except ImportError:
    # Prettyprinter package is not installed.
    from pprint import pformat  # noqa
