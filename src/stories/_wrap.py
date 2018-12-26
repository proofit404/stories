from ._failures import combine_failures, maybe_disable_null_protocol
from ._marker import BeginningOfStory, EndOfStory


def wrap_story(
    is_story, arguments, collected, cls_name, story_name, obj, contract, protocol
):

    failures = protocol.failures

    methods = [(BeginningOfStory(cls_name, story_name, arguments), contract, protocol)]

    for name in collected:

        attr = getattr(obj, name)

        if not is_story(attr):
            methods.append((attr, contract, protocol))
            continue

        if len(attr.methods) == 2:
            continue

        failures = combine_failures(
            failures, cls_name, story_name, attr.failures, attr.cls_name, attr.name
        )

        # TODO: Is there a way to avoid this modification?
        attr.methods[0][0].set_parent(name, attr.obj is obj)

        methods.extend(attr.methods)

    methods.append((EndOfStory(), contract, protocol))

    methods = maybe_disable_null_protocol(methods, failures)

    return methods, failures
