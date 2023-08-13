"""Service objects designed with OOP in mind."""
from stories.actor import Actor
from stories.initiate import Initiate
from stories.story import Steps
from stories.story import Story


__all__ = ("Story", "I", "initiate", "Actor")


I = Steps()  # noqa: E741
del Steps


initiate = Initiate((Story,))
del Initiate
