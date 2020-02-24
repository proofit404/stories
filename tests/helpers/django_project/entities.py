# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import NewType


CategoryId = NewType("CategoryId", int)


@dataclass
class Category:
    primary_key: CategoryId


class Token:
    def is_expired(self):
        return True
