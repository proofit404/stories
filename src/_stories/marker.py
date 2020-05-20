# -*- coding: utf-8 -*-


class BeginningOfStory(object):
    def __init__(self, cls_name, name):
        self.cls_name = cls_name
        self.name = name
        self.parent_name = None

    @property
    def story_name(self):
        if self.parent_name is not None:
            return self.parent_name + " (" + self.cls_name + "." + self.name + ")"
        else:
            return self.cls_name + "." + self.name

    def set_parent(self, parent_name):
        self.parent_name = parent_name


class EndOfStory(object):
    pass
