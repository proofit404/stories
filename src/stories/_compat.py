# NOTE: Every type ignore in this module is necessary due to
# false-positive bugs in mypy.  Feel free to remove them as they'll be
# fixed.  See GitHub issues for more info:
# `https://github.com/python/mypy/issues/1105`,
# `https://github.com/python/mypy/issues/1106`,
# `https://github.com/python/mypy/issues/1107`.


try:
    from enum import Enum, EnumMeta
except ImportError:
    # We are on Python 2.7 and enum34 package is not installed.
    class Enum(object):  # type: ignore
        pass

    class EnumMeta(object):  # type: ignore
        pass


try:
    from pydantic.error_wrappers import ErrorWrapper as PydanticError
    from pydantic.fields import Shape as PydanticShape
    from pydantic.main import MetaModel as PydanticSpec
    from pydantic.utils import display_as_type as pydantic_display
except ImportError:
    # Pydantic package is not installed.
    class PydanticSpec(object):  # type: ignore
        pass

    class PydanticError(object):  # type: ignore
        pass

    class PydanticShape(object):  # type: ignore
        pass

    def pydantic_display(v):  # type: ignore
        pass


try:
    from marshmallow.schema import SchemaMeta as MarshmallowSpec
except ImportError:
    # Marshmallow package is not installed.
    class MarshmallowSpec(object):  # type: ignore
        pass


try:
    from cerberus import Validator as CerberusSpec
except ImportError:
    # Cerberus package is not installed.
    class CerberusSpec(object):  # type: ignore
        pass


try:
    from textwrap import indent
except ImportError:
    # We are on Python 2.7
    def indent(text, prefix):  # type: ignore
        return "".join(map(lambda l: prefix + l, text.splitlines(True)))


try:
    from prettyprinter import pformat
except ImportError:
    # Prettyprinter package is not installed.
    from pprint import pformat  # noqa
