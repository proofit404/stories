from dataclasses import dataclass


@dataclass
class Category:
    """Category entity."""

    name: str
    cost: int

    def affordable_for(self, profile):
        """Check if profile could afford a category."""
        return profile.balance > self.cost


@dataclass
class Profile:
    """Profile entity."""

    balance: int


@dataclass
class Subscription:
    """Subscription entity."""

    duration: str

    def is_expired(self):
        """Check subscription expiraton."""
        return False
