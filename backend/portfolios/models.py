from django.contrib.auth import get_user_model
from django.db import models
from stocks.models import Stock


class Portfolio(models.Model):

    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="portfolios"
    )


class Investment(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.PROTECT, related_name="investments"
    )
    stock = models.ForeignKey(
        Stock, on_delete=models.PROTECT, related_name="investments"
    )
