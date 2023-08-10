"""Service objects designed with OOP in mind."""
from stories.actor import Actor
from stories.initiate import initiate
from stories.steps import Steps
from stories.story import Story


__all__ = ("Story", "I", "initiate", "Actor")


I = Steps()  # noqa: E741

del Steps
