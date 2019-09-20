from _stories.mounted import ClassMountedStory


def contract_in(cls, *args):
    def setter(contract):
        for attrname in dir(cls):
            attribute = getattr(cls, attrname)
            if type(attribute) is ClassMountedStory:
                attribute.contract(contract)
        return contract

    if args:
        return setter(*args)
    else:
        return setter


def failures_in(cls, *args):
    def setter(failures):
        for attrname in dir(cls):
            attribute = getattr(cls, attrname)
            if type(attribute) is ClassMountedStory:
                attribute.failures(failures)
        return failures

    if args:
        return setter(*args)
    else:
        return setter
