from ._failures import combine_failures, maybe_disable_null_protocol
from ._marker import BeginningOfStory, EndOfStory


def wrap_story(is_story, collected, cls_name, story_name, obj, protocol):

    methods = []
    failures = protocol.failures

    for name in collected:

        attr = getattr(obj, name)
        if not is_story(attr):
            methods.append((attr, protocol))
            continue

        failures = combine_failures(
            failures, cls_name, story_name, attr.failures, attr.cls_name, attr.name
        )
        if not attr.methods:
            continue

        if attr.obj is obj:
            method_name = name
        else:
            method_name = name + " (" + attr.cls_name + "." + attr.name + ")"

        methods.append((BeginningOfStory(method_name, attr.arguments), protocol))
        methods.extend(attr.methods)
        methods.append((EndOfStory(), protocol))

    methods = maybe_disable_null_protocol(methods, failures)

    return methods, failures
