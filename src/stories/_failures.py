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
    def __init__(self, cls, failures):
        # FIXME: Support inheritance substory and substory DI types.
        self.cls = cls
        self.failures = failures
        if isinstance(failures, EnumMeta):
            available = failures.__members__.values()
        elif failures is not None:
            available = failures
        else:
            return
        self.available = ", ".join(map(repr, available))

    def check(self, method, reason):
        if reason and self.failures:
            if isinstance(self.failures, EnumMeta) and not isinstance(reason, Enum):
                # TODO: This comparison should happens only if users
                # define their stories with Enum and StoryFactory.
                # This decision should be made in the StoryFactory
                # itself and then propagated to the executor.  Also
                # this is sequestial duplication is bad.
                message = wrong_reason_template.format(
                    reason=reason,
                    available=self.available,
                    cls=self.cls.__name__,
                    method=method.__name__,
                )
                raise FailureProtocolError(message)
            if reason not in self.failures:
                message = wrong_reason_template.format(
                    reason=reason,
                    available=self.available,
                    cls=self.cls.__name__,
                    method=method.__name__,
                )
                raise FailureProtocolError(message)
        if not reason and self.failures:
            message = null_reason_template.format(
                available=self.available, cls=self.cls.__name__, method=method.__name__
            )
            raise FailureProtocolError(message)


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
