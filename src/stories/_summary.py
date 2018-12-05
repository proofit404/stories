class FailureSummary(object):
    def __init__(
        self, protocol, story_cls_name, story_method_name, ctx, failed_method, reason
    ):
        self.is_success = False
        self.is_failure = True
        # FIXME: This three attributes assignments are bad.  We expose
        # very internal stuff to the user facing API.  Rewrite before
        # release!
        self.protocol = protocol
        self.story_cls_name = story_cls_name
        self.story_method_name = story_method_name
        self.ctx = ctx
        self.failed_method = failed_method
        self.failure_reason = reason

    def failed_on(self, method_name):
        return method_name == self.failed_method

    def failed_because(self, reason):
        self.protocol.summarize(self.story_cls_name, self.story_method_name, reason)
        return reason == self.failure_reason

    @property
    def value(self):
        raise AssertionError

    def __repr__(self):
        return "Failure()"


class SuccessSummary(object):
    def __init__(self, value):
        self.is_success = True
        self.is_failure = False
        self.value = value

    def failed_on(self, method_name):
        return False

    def failed_because(self, reason):
        return False

    def __repr__(self):
        return "Success()"
