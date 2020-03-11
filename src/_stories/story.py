# -*- coding: utf-8 -*-
from _stories.argument import get_arguments
from _stories.collect import collect_story
from _stories.failures import check_data_type
from _stories.mounted import ClassMountedStory
from _stories.mounted import MountedStory
from _stories.wrap import wrap_story


def story(f):
    name = f.__name__
    arguments = get_arguments(f)
    collected = collect_story(f)
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
        if obj is None:
            return ClassMountedStory(
                cls, name, collected, contract_method, failures_method
            )
        else:
            methods, contract, failures, executor = wrap_story(
                arguments,
                collected,
                cls.__name__,
                name,
                obj,
                this["contract"],
                this["failures"],
            )
            return MountedStory(
                obj,
                cls.__name__,
                name,
                arguments,
                methods,
                contract,
                failures,
                executor,
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
