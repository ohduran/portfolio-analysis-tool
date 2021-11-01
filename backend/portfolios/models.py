from assets.models import Asset
from django.contrib.auth import get_user_model
from django.db import models


class Portfolio(models.Model):

    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="portfolios"
    )
    name = models.CharField(max_length=100)


class Investment(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.PROTECT, related_name="investments"
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.PROTECT, related_name="investments"
    )
    amount = models.DecimalField(max_digits=9, decimal_places=2)
