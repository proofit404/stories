# -*- coding: utf-8 -*-
from _stories.collect import collect_story
from _stories.failures import check_data_type
from _stories.mounted import ClassMountedStory


def story(f):
    collected = collect_story(f)
    name = f.__name__
    # Can't use non local keyword because of Python 2.
    this = {"contract": None, "failures": None}

    def contract_method(contract):
        # FIXME: Raise error on unsupported types.
        this["contract"] = contract
        return contract

    def failures_method(failures):
        check_data_type(failures)
        this["failures"] = failures
        return failures

    def get_method(self, obj, cls):
        __tracebackhide__ = True
        class_mounted_story = ClassMountedStory(
            cls, f, name, collected, contract_method, failures_method
        )
        if obj is None:
            return class_mounted_story
        else:
            return class_mounted_story.to_mounted_story(
                obj, this["contract"], this["failures"]
            )

    return type(
        "Story",
        (object,),
        {
            "__get__": get_method,
            "contract": staticmethod(contract_method),
            "failures": staticmethod(failures_method),
        },
    )()


class class_story(classmethod):
    def __get__(self, instance, owner):
        method = super(class_story, self).__get__(instance, owner)
        return story(method).__get__(instance, owner)
