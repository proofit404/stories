"""Service objects designed with OOP in mind."""
from aiostories.story import Story as Story
from stories import Actor as Actor
from stories import I as I
from stories.initiate import Initiate


__all__ = ("Story", "I", "initiate", "Actor")


initiate = Initiate((Story,))
del Initiate
