from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    """Entity."""

    name: str


@dataclass
class Cost:
    """Entity."""

    at: datetime
    amount: int


@dataclass
class Order:
    """Entity."""

    product: Product
    cost: Cost

    def affordable_for(self, customer):
        """Check if customer could afford an order."""
        return customer.balance > self.cost.amount


@dataclass
class Customer:
    """Entity."""

    balance: int


@dataclass
class Payment:
    """Entity."""

    due_date: datetime

    def was_received(self):
        """Check if payment was received."""
        return False
