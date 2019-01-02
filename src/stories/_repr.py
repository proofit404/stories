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
