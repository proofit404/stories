class Category:
    cost = 7

    def __init__(self, id):
        self.id = id


class Profile:
    balance = 8

    def __init__(self, user_id):
        self.user_id = user_id


class Subscription:
    def __init__(self, category, profile):
        self.category = category
        self.profile = profile

    def __repr__(self):
        return "<Subscription object (1)>"

    def save(self):
        pass


class Objects:
    def __init__(self, cls):
        self.cls = cls

    def get(self, **kwargs):
        return self.cls(**kwargs)

    def all(self):
        pass


Category.objects = Objects(Category)
Profile.objects = Objects(Profile)
Subscription.objects = Objects(Subscription)
