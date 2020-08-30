try:
    from pydantic.error_wrappers import ErrorWrapper as PydanticError
    from pydantic.main import ModelMetaclass as PydanticSpec
except ImportError:
    # Pydantic package is not installed.
    class PydanticSpec:
        pass

    class PydanticError:
        pass


try:
    from marshmallow.schema import SchemaMeta as MarshmallowSpec
    from marshmallow.exceptions import ValidationError as MarshmallowError
except ImportError:
    # Marshmallow package is not installed.
    class MarshmallowSpec:
        pass

    class MarshmallowError:
        pass


try:
    from cerberus import Validator as CerberusSpec
except ImportError:
    # Cerberus package is not installed.
    class CerberusSpec:
        pass


try:
    from prettyprinter import pformat
except ImportError:
    # Prettyprinter package is not installed.
    from pprint import pformat  # noqa: F401
