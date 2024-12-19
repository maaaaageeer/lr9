from django.db import models
from django.contrib.auth.models import User


class BonusLevel(models.Model):
    level_name = models.CharField(max_length=20, unique=True)
    spending_threshold = models.DecimalField(max_digits=10, decimal_places=2)
    cashback_percentage = models.IntegerField()

    def __str__(self):
        return self.level_name


class UserBonuses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bonuses")
    current_spending = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    level = models.ForeignKey(BonusLevel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Бонусы пользователя {self.user.username}"
