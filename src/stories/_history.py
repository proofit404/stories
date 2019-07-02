from ._types import AbstractHistory, FailureVariant, ValueVariant


class History(AbstractHistory):
    def __init__(self):
        self.indent = 0
        self.lines = []

    def before_call(self, method_name):
        # type: (str) -> None
        self.lines.append("  " * self.indent + method_name)

    def on_result(self, value):
        # type: (ValueVariant) -> None
        self.lines[-1] += " (returned: " + repr(value) + ")"

    def on_failure(self, reason):
        # type: (FailureVariant) -> None
        if reason:
            self.lines[-1] += " (failed: " + repr(reason) + ")"
        else:
            self.lines[-1] += " (failed)"

    def on_skip(self):
        # type: () -> None
        self.lines[-1] += " (skipped)"
        self.indent -= 1

    def on_error(self, error_name):
        # type: (str) -> None
        self.lines[-1] += " (errored: " + error_name + ")"

    def on_substory_start(self):
        # type: () -> None
        self.indent += 1

    def on_substory_end(self):
        # type: () -> None
        self.lines.pop()
        self.indent -= 1
