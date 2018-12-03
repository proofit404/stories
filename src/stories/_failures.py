try:
    from enum import Enum, EnumMeta
except ImportError:
    # We are on Python 2.7 and enum34 package is not installed.
    class Enum(object):
        pass

    class EnumMeta(object):
        pass


from .exceptions import FailureProtocolError


def check_protocol(reason, protocol):

    if reason and protocol:
        if isinstance(protocol, EnumMeta) and not isinstance(reason, Enum):
            # TODO: This comparison should happens only if users
            # define their stories with Enum and StoryFactory.  This
            # decision should be made in the StoryFactory itself and
            # then propagated to the executor.
            raise FailureProtocolError()
        if reason not in protocol:
            raise FailureProtocolError()
    if not reason and protocol:
        raise FailureProtocolError()
