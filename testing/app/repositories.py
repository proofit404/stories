from __future__ import annotations

from app.usecases import CustomerId
from app.usecases import OrderId


def load_order(order_id: OrderId):
    return {"product": {"name": "Books"}, "cost": {"at": "1999-12-31", "amount": 7}}


def load_customer(customer_id: CustomerId):
    return {"balance": 8}


def create_payment(customer_id: CustomerId, order_id: OrderId):
    return {"due_date": "1999-12-31"}
