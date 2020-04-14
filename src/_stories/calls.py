# -*- coding: utf-8 -*-
class CallMethod(object):
    def __init__(self, name):
        self.name = name
        self.base_class = None

    def bind_to_object(self, obj):
        return getattr(obj, self.name)

    def __repr__(self):
        return "CallMethod({})".format(self.name)


class CallSuperStory(CallMethod):
    def __init__(self, name, base_class):
        super(CallSuperStory, self).__init__(name)
        self.base_class = base_class

    def bind_to_object(self, obj):
        class_mounted_story = getattr(self.base_class, self.name)

        mounted_story = class_mounted_story.to_mounted_story(obj)

        return mounted_story

    def __repr__(self):
        return "CallSuperStory({}.{})".format(self.base_class.__name__, self.name)
