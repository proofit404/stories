from inspect import getfullargspec

from stories import Success


class MethodDefinitionsType(type):
    def __getattr__(cls, attrname):
        if attrname in getfullargspec(cls.__init__).args:
            raise AttributeError
        else:
            return lambda self, ctx: Success()


class MethodDefinitions(metaclass=MethodDefinitionsType):
    pass
