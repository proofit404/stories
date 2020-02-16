# -*- coding: utf-8 -*-


try:
    from enum import Enum, EnumMeta
except ImportError:
    # We are on Python 2.7 and enum34 package is not installed.
    class Enum(object):
        pass

    class EnumMeta(object):
        pass


try:
    from pydantic.error_wrappers import ErrorWrapper as PydanticError
    from pydantic.main import ModelMetaclass as PydanticSpec
except ImportError:
    # Pydantic package is not installed.
    class PydanticSpec(object):
        pass

    class PydanticError(object):
        pass


try:
    import marshmallow

    if marshmallow.__version_info__[0] != 3:
        raise ImportError

    from marshmallow.schema import SchemaMeta as Marshmallow3Spec
    from marshmallow.exceptions import ValidationError as Marshmallow3Error
except ImportError:
    # Marshmallow 3 package is not installed.
    class Marshmallow3Spec(object):
        pass

    class Marshmallow3Error(object):
        pass


try:
    import marshmallow

    if marshmallow.__version_info__[0] != 2:
        raise ImportError

    from marshmallow.schema import SchemaMeta as Marshmallow2Spec
except ImportError:
    # Marshmallow 2 package is not installed.
    class Marshmallow2Spec(object):
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
    def indent(text, prefix):
        return "".join(map(lambda l: prefix + l, text.splitlines(True)))


try:
    from prettyprinter import pformat
except ImportError:
    # Prettyprinter package is not installed.
    from pprint import pformat  # noqa: F401


try:
    from asyncio import iscoroutinefunction
except ImportError:
    # We are on Python 2.7
    def iscoroutinefunction(func):
        return False
