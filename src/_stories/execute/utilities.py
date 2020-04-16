# -*- coding: utf-8 -*-
from _stories.exceptions import StoryDefinitionError
from _stories.returned import Failure
from _stories.returned import Result
from _stories.returned import Skip
from _stories.returned import Success


def validate_result_type(method, result_type, result):
    if hasattr(method, "story_name"):
        method_name = "{}.{}".format(method.story_name, method.__name__)
    else:
        try:
            method_name = method.__qualname__
        except AttributeError:
            # Python 2 fallback
            method_name = "{}.{}".format(
                method.im_self.__class__.__name__, method.__name__
            )
    if result_type not in (Result, Success, Failure, Skip):
        if result is True:
            expected = "`Success()` or `Result(True)`"
            raise StoryDefinitionError(
                ambiguous_result_type_template.format(
                    method=method_name, result=result, expected=expected
                )
            )
        elif result is False:
            expected = "`Failure()` or `Result(False)`"
            raise StoryDefinitionError(
                ambiguous_result_type_template.format(
                    method=method_name, result=result, expected=expected
                )
            )
        elif result is None:
            expected = "`Success()` or `Result()`"
            raise StoryDefinitionError(
                ambiguous_result_type_template.format(
                    method=method_name, result=result, expected=expected
                )
            )
        else:
            expected = "`Result({})`".format(result)
            raise StoryDefinitionError(
                invalid_result_type_template.format(
                    method=method_name, result=result, expected=expected
                )
            )


# Messages

ambiguous_result_type_template = """
Ambiguous result type returned from {method}.

Got `{result}`. Did you mean {expected}?
""".strip()

invalid_result_type_template = """
Invalid result type returned from {method}.

Got `{result}`. Did you mean {expected}?
""".strip()
