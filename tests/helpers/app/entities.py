from dataclasses import dataclass
from dataclasses import field
from datetime import date
from typing import NewType


CategoryId = NewType("CategoryId", int)


@dataclass
class Category:
    primary_key: CategoryId
    name: str
    cost: int


class Token:
    def is_expired(self):
        return True


PriceId = NewType("PriceId", int)


@dataclass
class Price:
    primary_key: PriceId
    cost: int
    period: int


ProfileId = NewType("ProfileId", int)


@dataclass
class Profile:
    primary_key: ProfileId
    balance: int

    def has_enough_balance(self, price):
        return self.balance >= price.cost


SubscriptionId = NewType("SubscriptionId", int)


@dataclass
class Subscription:
    primary_key: SubscriptionId
    created: date = field(default=date(2019, 1, 1), repr=False)

    def is_expired(self):
        expiration = {1: False, 7: True}
        return expiration[self.primary_key]
