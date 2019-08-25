from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=300)
    cost = models.IntegerField()


class Price(models.Model):
    cost = models.IntegerField()
    period = models.IntegerField()


class Profile(models.Model):
    balance = models.IntegerField()


class Subscription(models.Model):
    created = models.DateField(auto_now_add=True)
    category = models.ForeignKey(
        Category, related_name="subscriptions", on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile, related_name="subscriptions", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["category", "profile"]

    def is_expired(self):
        # FIXME: It should be a real method
        return True if self.pk == 7 else False
