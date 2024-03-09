from __future__ import annotations

from datetime import date

from pydantic.dataclasses import dataclass


@dataclass
class Product:
    name: str


@dataclass
class Cost:
    at: date
    amount: int


@dataclass
class Customer:
    balance: int


@dataclass
class Order:
    product: Product
    cost: Cost

    def affordable_for(self, customer: Customer) -> bool:
        return customer.balance > self.cost.amount


@dataclass
class Payment:
    due_date: date

    def was_received(self) -> bool:
        return False
