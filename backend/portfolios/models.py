from assets.models import Asset
from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import ActivatorModel, TimeStampedModel


class Portfolio(ActivatorModel, TimeStampedModel, models.Model):
    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user", "name"), name="unique_user_name_portfolio"
            ),
        )

    user = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="portfolios"
    )
    name = models.CharField(max_length=100)
    currency = models.CharField(
        max_length=3
    )  # TODO: Forex market is To Be Defined into a new app. Out of scope.


class Investment(models.Model):
    """
    The currency of each investment is assumed to be the portfolio's.
    """

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("portfolio", "asset"), name="unique_portfolio_asset_investment"
            ),
        )

    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.PROTECT, related_name="investments"
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.PROTECT, related_name="investments"
    )
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        help_text="The number of shares, the amount of commodity bought, etc.",
    )
