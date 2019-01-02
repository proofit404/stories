from ._mounted import ClassMountedStory


def failures_in(cls):
    def setter(failures):
        for attrname in dir(cls):
            attribute = getattr(cls, attrname)
            if type(attribute) is ClassMountedStory:
                attribute.failures(failures)
        return failures

    return setter
