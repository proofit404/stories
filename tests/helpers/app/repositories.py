from app.entities import Category
from app.entities import Profile
from app.entities import Subscription


log = __builtins__["print"]


def load_category(category_id):
    """Load category from db."""
    names = {1: "Books", 2: "Movies"}
    costs = {1: 7, 2: 17}
    return Category(name=names[category_id], cost=costs[category_id])


def load_profile(profile_id):
    """Load profile from db."""
    balances = {1: 8, 2: 8}
    return Profile(balance=balances[profile_id])


def create_subscription(profile_id, category_id):
    """Save Subscription into db."""
    durations = {(1, 1): "30 days"}
    return Subscription(duration=durations[(profile_id, category_id)])


def lock_item_query():
    log("UPDATE 'items';")


def charge_money_query():
    log("UPDATE 'balance';")
