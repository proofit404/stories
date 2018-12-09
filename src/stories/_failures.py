try:
    from enum import Enum, EnumMeta
except ImportError:
    # We are on Python 2.7 and enum34 package is not installed.
    class Enum(object):
        pass

    class EnumMeta(object):
        pass


from .exceptions import FailureProtocolError


def make_protocol(failures):
    if isinstance(failures, EnumMeta):
        protocol_class = EnumProtocol
    elif failures is not None:
        protocol_class = CollectionProtocol
    else:
        protocol_class = NullProtocol
    return protocol_class(failures)


class Protocol(object):
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

    def compare(self, story, cls_name, method_name):
        if not self.compare_other(story.protocol):
            message = mismatch_template.format(
                cls=cls_name,
                method=method_name,
                available=self.available,
                other_cls=story.cls_name,
                other_method=story.name,
                other_available=story.protocol.available,
            )
            raise FailureProtocolError(message)

    def check_reason(self, reason):

        raise NotImplementedError

    def cast_reason(self, reason):

        raise NotImplementedError

    def compare_other(self, other):

        raise NotImplementedError


class NullProtocol(Protocol):
    def __init__(self, failures):
        self.failures = None
        self.available = "None"

    def cast_reason(self, reason):
        return reason

    def compare_other(self, other):
        return other.failures is None


class CollectionProtocol(Protocol):
    def __init__(self, failures):
        self.failures = failures
        self.available = ", ".join(map(repr, failures))

    def check_reason(self, reason):
        return reason in self.failures

    def cast_reason(self, reason):
        return reason

    def compare_other(self, other):
        return other.failures is not None and set(self.failures) >= set(other.failures)


class EnumProtocol(Protocol):
    def __init__(self, failures):
        self.failures = failures
        self.available = ", ".join(map(repr, failures.__members__.values()))

    def check_reason(self, reason):
        return isinstance(reason, Enum) and reason.name in self.failures.__members__

    def cast_reason(self, reason):
        return self.failures.__members__[reason.name]

    def compare_other(self, other):
        return isinstance(other.failures, EnumMeta) and set(
            self.failures.__members__
        ) >= set(other.failures.__members__)


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


mismatch_template = """
Story and substory failure protocol mismatch.

Story: {cls}.{method}

Available failures are: {available}

Substory: {other_cls}.{other_method}

Available failures are: {other_available}
""".strip()
