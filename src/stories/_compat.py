try:
    from enum import Enum, EnumMeta
except ImportError:
    # We are on Python 2.7 and enum34 package is not installed.
    class Enum(object):
        pass

    class EnumMeta(object):
        pass


try:
    from pydantic.main import MetaModel as PydanticSpec
except ImportError:
    # Pydantic package is not installed.
    class PydanticSpec(object):
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
