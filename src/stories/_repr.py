def namespace_representation(ns):
    return "(" + ", ".join([k + "=" + repr(v) for k, v in ns.items()]) + ")"


def context_representation(ctx):

    name = ctx.__class__.__name__
    if not ctx.lines:
        return name + "()"
    items = ["%s = %s" % (key, repr(value)) for (key, value) in ctx.ns.items()]
    longest = max(map(len, items))
    lines = [
        "    %s  # %s" % (item.ljust(longest), line)
        for item, line in zip(items, ctx.lines)
    ]
    return "\n".join([name + ":"] + lines)


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
