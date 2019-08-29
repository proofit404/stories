class History(object):
    def __init__(self):
        self.indent = 0
        self.lines = []

    def before_call(self, method_name):
        self.lines.append("  " * self.indent + method_name)

    def on_result(self, value):
        self.lines[-1] += " (returned: " + repr(value) + ")"

    def on_failure(self, reason):
        if reason:
            self.lines[-1] += " (failed: " + repr(reason) + ")"
        else:
            self.lines[-1] += " (failed)"

    def on_skip(self):
        self.lines[-1] += " (skipped)"
        self.indent -= 1

    def on_error(self, error_name):
        self.lines[-1] += " (errored: " + error_name + ")"

    def on_substory_start(self):
        self.indent += 1

    def on_substory_end(self):
        self.lines.pop()
        self.indent -= 1
