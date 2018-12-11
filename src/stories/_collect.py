from ._marker import substory_end, substory_start


def collect_story(f):

    calls = []

    class Collector(object):
        def __getattr__(self, name):
            calls.append(name)

    f(Collector())

    return calls


def wrap_story(is_story, collected, obj, protocol, cls_name, method_name):

    # FIXME: `cls_name` and `name` should be encapsulated somewhere.
    # This arguments list is insane.
    methods = []

    for name in collected:
        attr = getattr(obj, name)
        if not is_story(attr):
            methods.append((obj, attr.__func__))
            continue

        protocol.compare(attr, cls_name, method_name)
        # TODO: Test deeper composition.  Protocol mismatch in:
        #
        # story -> normal substory -> mismatched substory
        sub_methods = wrap_story(
            is_story, attr.collected, attr.obj, protocol, cls_name, method_name
        )
        if not sub_methods:
            continue

        if attr.obj is obj:
            method_name = name
        else:
            method_name = name + " (" + attr.cls_name + "." + attr.name + ")"

        sub_obj = sub_methods[0][0]
        methods.append((sub_obj, make_validator(method_name, attr.arguments)))
        methods.extend(sub_methods)
        methods.append((sub_obj, end_of_story))

    return methods


def make_validator(name, arguments):
    def validate_substory_arguments(self, ctx):
        assert set(arguments) <= set(ctx)
        return substory_start

    validate_substory_arguments.method_name = name

    return validate_substory_arguments


def end_of_story(self, ctx):
    return substory_end
