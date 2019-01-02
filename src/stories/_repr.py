from ._compat import EnumMeta


def history_representation(history):
    result = "\n".join(history.lines)
    return result


def context_representation(ns, lines):

    if not lines:
        return "Context()"
    items = ["%s = %s" % (key, repr(value)) for (key, value) in ns.items()]
    longest = max(map(len, items))
    lines = [
        "    %s  # %s" % (item.ljust(longest), line) for item, line in zip(items, lines)
    ]
    return "\n".join(["Context:"] + lines)


def story_representation(is_story, first_line, cls, obj, collected):

    result = [first_line]
    if collected:
        for name in collected:
            attr = getattr(obj or cls, name, None)
            if is_story(attr):
                if attr.cls is cls:
                    first = name
                else:
                    first = name + " (" + attr.cls_name + "." + attr.name + ")"
                sub_result = story_representation(
                    is_story, first, attr.cls, attr.obj, attr.collected
                )
                result.extend(["  " + line for line in sub_result.split("\n")])
            else:
                suffix = " ??" if attr is None else ""
                result.append("  " + name + suffix)
    else:
        result.append("  <empty>")

    return "\n".join(result)


def failures_representation(failures):

    if isinstance(failures, EnumMeta):
        return ", ".join(map(repr, failures.__members__.values()))
    elif isinstance(failures, (list, tuple, set, frozenset)):
        return ", ".join(map(repr, failures))
    elif failures is None:
        return "None"
