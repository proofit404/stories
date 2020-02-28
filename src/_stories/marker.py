# -*- coding: utf-8 -*-


class BeginningOfStory(object):
    def __init__(self, cls_name, name):
        self.cls_name = cls_name
        self.name = name
        self.parent_name = None
        self.same_object = None

    @property
    def story_name(self):
        if self.parent_name is None:
            return self.cls_name + "." + self.name
        elif self.same_object:
            return self.parent_name
        else:
            return self.parent_name + " (" + self.cls_name + "." + self.name + ")"

    def set_parent(self, parent_name, same_object):
        self.parent_name = parent_name
        self.same_object = same_object


class EndOfStory(object):
    pass
