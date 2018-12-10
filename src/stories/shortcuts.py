from ._story import Story


def failures_in(cls):
    # FIXME: Test me with Enum decorator and list argument.
    def setter(failures):
        for attrname in dir(cls):
            attribute = getattr(cls, attrname)
            if isinstance(attribute, Story):
                attribute.failures(failures)

    return setter
