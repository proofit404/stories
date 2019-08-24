from django.db import models


class Category(models.Model):
    cost = models.IntegerField()


class Profile(models.Model):
    balance = models.IntegerField()


class Subscription(models.Model):
    category = models.ForeignKey(
        Category, related_name="subscriptions", on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile, related_name="subscriptions", on_delete=models.CASCADE
    )
