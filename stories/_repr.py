def namespace_representation(ns):
    return "(" + ", ".join([k + "=" + repr(v) for k, v in ns.items()]) + ")"


def story_representation(is_story, first_line, cls, obj, collected):

    result = [first_line]
    if collected:
        for name in collected:
            attr = getattr(obj, name)
            if is_story(attr):
                if attr.cls is cls:
                    first = name
                else:
                    first = name + " (" + attr.cls_name + "." + attr.name + ")"
                # FIXME: I don't like this recursion.
                sub_result = story_representation(
                    is_story, first, attr.cls, attr.obj, attr.collected
                )
                result.extend(["  " + line for line in sub_result.split("\n")])
            else:
                result.append("  " + name)
    else:
        result.append("  <empty>")

    return "\n".join(result)
