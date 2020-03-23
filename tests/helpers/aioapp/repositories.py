# -*- coding: utf-8 -*-
from app.entities import Category
from app.entities import Profile
from app.entities import Subscription


async def load_category(primary_key):
    return Category(primary_key=primary_key)


async def load_profile(primary_key):
    return Profile()


async def create_subscription(profile, category):
    return Subscription()
