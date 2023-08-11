from dataclasses import dataclass
from datetime import datetime
from typing import NewType


@dataclass
class Product:
    name: str


@dataclass
class Cost:
    at: datetime
    amount: int


CustomerId = NewType("CustomerId", int)


@dataclass
class Customer:
    balance: int


OrderId = NewType("OrderId", int)


@dataclass
class Order:
    product: Product
    cost: Cost

    def affordable_for(self, customer: Customer) -> bool:
        return customer.balance > self.cost.amount


@dataclass
class Payment:
    due_date: datetime

    def was_received(self) -> bool:
        return False
