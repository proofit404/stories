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

    # TODO: Split into Interface and two classes.  Rewrite without
    # self-monkey-patching initializer.

    def __init__(self, failures):
        self.failures = failures
        if isinstance(failures, EnumMeta):
            available = failures.__members__.values()
            check = self.check_enum
            cast = self.cast_enum
        elif failures is not None:
            available = failures
            check = self.check_collection
            cast = self.cast_collection
        else:
            self.cast_reason = self.cast_collection
            return
        self.available = ", ".join(map(repr, available))
        self.check_reason = check
        self.cast_reason = cast

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
        return isinstance(reason, Enum) and reason.name in self.failures.__members__

    def summarize(self, cls_name, method_name, reason):
        # TODO: Deny to use `failed_because(None)`.
        if self.failures and not self.check_reason(reason):
            message = wrong_summary_template.format(
                reason=reason,
                available=self.available,
                cls=cls_name,
                method=method_name,
            )
            raise FailureProtocolError(message)
        if not self.failures:
            message = null_summary_template.format(cls=cls_name, method=method_name)
            raise FailureProtocolError(message)

    def cast_collection(self, reason):
        return reason

    def cast_enum(self, reason):
        return self.failures.__members__[reason.name]


wrong_reason_template = """
Failure({reason!r}) failure reason is not allowed by current protocol.

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


wrong_summary_template = """
'failed_because' method got argument mismatching failure protocol: {reason!r}

Available failures are: {available}

Story returned result: {cls}.{method}
""".strip()


null_summary_template = """
'failed_because' method can not be used to check result of a story defined without failure protocol.

Story returned result: {cls}.{method}

Use StoryFactory to define failure protocol.
""".strip()
