from django_project.entities import Token
from django_project.models import Category
from django_project.models import Price
from django_project.models import Profile
from django_project.models import Subscription


def load_promo_code(category):
    pass


def load_token():
    return Token()


def load_category(primary_key):
    return Category.objects.get(pk=primary_key)


def load_price(primary_key):
    return Price.objects.get(pk=primary_key)


def load_profile(primary_key):
    return Profile.objects.get(pk=primary_key)


def decrease_balance(profile, cost):
    pass


def save_profile(profile):
    pass


def calculate_period(period):
    pass


def create_subscription(profile, category, expires):
    pass


def load_subscription(category_id, profile_id):
    return Subscription.objects.filter(
        category_id=category_id, profile_id=profile_id
    ).first()


def send_notification(kind, profile, category_name):
    pass
