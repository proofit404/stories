from ._contract import combine_contract, make_contract, maybe_extend_downstream_argsets
from ._failures import combine_failures, make_exec_protocol, maybe_disable_null_protocol
from ._marker import BeginningOfStory, EndOfStory
from ._mounted import MountedStory


def wrap_story(arguments, collected, cls_name, story_name, obj, spec, failures):

    contract = make_contract(cls_name, story_name, arguments, spec)
    protocol = make_exec_protocol(failures)

    methods = [(BeginningOfStory(cls_name, story_name), contract, protocol)]

    for name in collected:

        attr = getattr(obj, name)

        if type(attr) is not MountedStory:
            methods.append((attr, contract, protocol))
            continue

        combine_contract(contract, attr.methods[0][1])

        failures = combine_failures(
            failures, cls_name, story_name, attr.failures, attr.cls_name, attr.name
        )

        # FIXME: Is there a way to avoid this modification?
        attr.methods[0][0].set_parent(name, attr.obj is obj)

        methods.extend(attr.methods)

    methods.append((EndOfStory(is_empty=not collected), contract, protocol))

    maybe_extend_downstream_argsets(methods, contract)

    methods = maybe_disable_null_protocol(methods, failures)

    return methods, failures
