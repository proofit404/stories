try:
    from enum import Enum, EnumMeta
except ImportError:
    # We are on Python 2.7 and enum34 package is not installed.
    class Enum(object):
        pass

    class EnumMeta(object):
        pass


from .exceptions import FailureProtocolError


class Protocol(object):
    def __init__(self, failures):
        self.failures = failures
        if isinstance(failures, EnumMeta):
            available = failures.__members__.values()
            check = self.check_enum
        elif failures is not None:
            available = failures
            check = self.check_collection
        else:
            return
        self.available = ", ".join(map(repr, available))
        self.check_reason = check

    def check(self, obj, method, reason):
        if reason and self.failures and not self.check_reason(reason):
            message = wrong_reason_template.format(
                reason=reason,
                available=self.available,
                cls=obj.__class__.__name__,
                method=method.__name__,
            )
            raise FailureProtocolError(message)
        if not reason and self.failures:
            message = null_reason_template.format(
                available=self.available,
                cls=obj.__class__.__name__,
                method=method.__name__,
            )
            raise FailureProtocolError(message)
        if reason and not self.failures:
            message = null_protocol_template.format(
                reason=reason, cls=obj.__class__.__name__, method=method.__name__
            )
            raise FailureProtocolError(message)

    def check_collection(self, reason):
        return reason in self.failures

    def check_enum(self, reason):
        return isinstance(reason, Enum) and reason in self.failures


wrong_reason_template = """
{reason!r} failure reason is not allowed by current protocol

Available failures are: {available}

Function returned value: {cls}.{method}
""".strip()


null_reason_template = """
Failure() can not be used in a story with failure protocol.

Available failures are: {available}

Function returned value: {cls}.{method}

Use one of them as Failure() argument.
""".strip()


null_protocol_template = """
Failure({reason!r}) can not be used in a story without failure protocol.

Function returned value: {cls}.{method}

Use StoryFactory to define failure protocol.
""".strip()
