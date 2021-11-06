from django.db import models


class Asset(models.Model):
    class Meta:
        constraints = (models.UniqueConstraint("symbol", name="unique_symbol_asset"),)

    # GICS Market Sectors
    ENERGY = "EN"
    MATERIALS = "MA"
    INDUSTRIALS = "IN"
    UTILITIES = "UT"
    HEALTHCARE = "HE"
    FINANCIALS = "FI"
    CONSUMER_DISCRETIONARY = "CD"
    CONSUMER_STAPLES = "CS"
    INFORMATION_TECHNOLOGY = "IT"
    COMMUNICATION_SERVICES = "CS"
    REAL_ESTATE = "RE"

    SECTORS_CHOICES = (
        (ENERGY, "energy"),
        (MATERIALS, "materials"),
        (INDUSTRIALS, "industrials"),
        (UTILITIES, "utilities"),
        (HEALTHCARE, "healthcare"),
        (FINANCIALS, "financials"),
        (CONSUMER_DISCRETIONARY, "consumer_discretionary"),
        (CONSUMER_STAPLES, "consumer_staples"),
        (INFORMATION_TECHNOLOGY, "information_technology"),
        (COMMUNICATION_SERVICES, "communication_services"),
        (REAL_ESTATE, "real_estate"),
    )

    # Assets listed on the New York Asset Exchange (NYSE) can have four or fewer letters.
    # Nasdaq-listed securities can have up to five characters.
    symbol = models.CharField(
        max_length=6, help_text="The exchange symbol that this item is traded under."
    )
    name = models.TextField()
    sector = models.CharField(max_length=2, choices=SECTORS_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class HistoricValue(models.Model):
    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("asset", "date_time"),
                name="unique_asset_date_time_historic_value",
            ),
        )

    date_time = models.DateTimeField()
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="historic_values"
    )
    currency = models.CharField(
        max_length=3
    )  # TODO: Forex market is To Be Defined into a new app. Out of scope.

    after_hours = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        help_text="The close price of the ticker symbol in after hours trading.",
    )
    close = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        help_text="The close price for the symbol in the given time period.",
    )
    high = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        help_text="The highest price for the symbol in the given time period.",
    )
    low = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        help_text="The lowest price for the symbol in the given time period.",
    )
    _open = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        help_text="The open price for the symbol in the given time period.",
    )
    pre_market = models.DecimalField(
        max_digits=9,
        decimal_places=3,
        help_text="The open price of the ticker symbol in pre-market trading.",
    )
    volume = models.DecimalField(
        max_digits=19,
        decimal_places=3,
        help_text="The trading volume of the symbol in the given time period.",
    )

    def __str__(self):
        return f"{self.asset.symbol} ({self.date_time}): {self.currency}{self.close}"
