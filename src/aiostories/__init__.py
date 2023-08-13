"""Service objects designed with OOP in mind."""
from aiostories.story import Story
from stories import Actor
from stories import I
from stories.initiate import Initiate


__all__ = ("Story", "I", "initiate", "Actor")


initiate = Initiate((Story,))
del Initiate
