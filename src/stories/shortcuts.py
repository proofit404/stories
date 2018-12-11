from ._mounted import is_story


def failures_in(cls):
    def setter(failures):
        for attrname in dir(cls):
            attribute = getattr(cls, attrname)
            if is_story(attribute):
                attribute.failures(failures)
        return failures

    return setter
