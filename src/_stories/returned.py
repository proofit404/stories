# -*- coding: utf-8 -*-


class Result(object):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return "Result(" + repr(self.value) + ")"


class Failure(object):
    def __init__(self, reason=None):
        self.reason = reason

    def __repr__(self):
        reason = repr(self.reason) if self.reason else ""
        return "Failure(" + reason + ")"


class Success(object):
    def __repr__(self):
        return "Success()"


class Skip(object):
    def __repr__(self):
        return "Skip()"
