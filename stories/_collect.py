from ._marker import undefined, valid_arguments


def collect_story(f):

    calls = []

    class Collector(object):
        def __getattr__(self, name):
            calls.append(name)
            return lambda: None

    f(Collector())

    return calls


def wrap_story(is_story, of, obj, collected):

    methods = []

    for name in collected:
        attr = getattr(obj, name)
        if is_story(attr):
            if attr.obj is obj:
                method_name = name
            else:
                # FIXME: I don't like this duplication.
                method_name = name + " (" + attr.cls_name + "." + attr.name + ")"
            methods.append(
                (attr.obj, make_validator(method_name, attr.arguments), attr.of)
            )
            methods.extend(attr.methods)
            methods.append((attr.obj, end_of_story, attr.of))
        else:
            methods.append((obj, attr.__func__, of))

    return methods


def make_validator(name, arguments):
    def validate_substory_arguments(self):
        assert set(arguments) <= set(self.ctx)
        return valid_arguments

    validate_substory_arguments.method_name = name

    return validate_substory_arguments


def end_of_story(self):
    return undefined
