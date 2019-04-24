# TOOD: check import in Python 2
import inspect
from ._contract import combine_contract, make_contract
from ._failures import combine_failures, make_exec_protocol, maybe_disable_null_protocol
from ._marker import BeginningOfStory, EndOfStory
from ._mounted import MountedStory


def clean_method_type(method, reference_value):
    is_async = inspect.iscoroutinefunction(method)
    # If markers flag was set before and was changed so async and sync methods are mixed
    if (reference_value is not None) and (not reference_value == is_async):
        raise TypeError('Sync and async methods should not be mixed.')
    return is_async


def wrap_story(arguments, collected, cls_name, story_name, obj, spec, failures):

    contract = make_contract(cls_name, story_name, arguments, spec)
    protocol = make_exec_protocol(failures)

    specs = [(spec, cls_name, story_name)]
    methods = []

    # Flag is undefined before any method processed
    use_async_markers = None

    for name in collected:

        attr = getattr(obj, name)

        if type(attr) is not MountedStory:
            use_async_markers = clean_method_type(attr, use_async_markers)
            methods.append((attr, contract, protocol))
            continue

        for method in attr.methods:
            use_async_markers = clean_method_type(method[0], use_async_markers)

        contract.add_substory_contract(attr.methods[0][1])

        specs = combine_contract(specs, attr.specs)

        failures = combine_failures(
            failures, cls_name, story_name, attr.failures, attr.cls_name, attr.name
        )

        # FIXME: Is there a way to avoid this modification?
        attr.methods[0][0].set_parent(name, attr.obj is obj)

        methods.extend(attr.methods)

    # Use sync markers if flag is undefined or false
    if not use_async_markers:
        beginning_marker = BeginningOfStory
        end_marker = EndOfStory
    else:
        from ._marker import AsyncBeginningOfStory, AsyncEndOfStory
        beginning_marker = AsyncBeginningOfStory
        end_marker = AsyncEndOfStory

    methods.insert(0, (beginning_marker(cls_name, story_name), contract, protocol))
    methods.append((end_marker(is_empty=not collected), contract, protocol))

    methods = maybe_disable_null_protocol(methods, failures)

    return methods, specs, failures
