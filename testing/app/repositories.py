from datetime import datetime

from app.entities import Cost
from app.entities import Customer
from app.entities import Order
from app.entities import Payment
from app.entities import Product
from app.tools import log


def load_order(order_id):
    """Perform database query."""
    names = {1: "Books", 2: "Movies"}
    dates = {1: datetime(1999, 12, 31), 2: datetime(2000, 1, 1)}
    costs = {1: 7, 2: 17}
    return Order(
        product=Product(name=names[order_id]),
        cost=Cost(at=dates[order_id], amount=costs[order_id]),
    )


def load_customer(customer_id):
    """Perform database query."""
    balances = {1: 8, 2: 8}
    return Customer(balance=balances[customer_id])


def create_payment(customer_id, order_id):
    """Perform database query."""
    dates = {(1, 1): datetime(1999, 12, 31)}
    return Payment(due_date=dates[(customer_id, order_id)])


def lock_item_query():
    """Perform database query."""
    log("UPDATE 'items';")


def charge_money_query():
    """Perform database query."""
    log("UPDATE 'balance';")
