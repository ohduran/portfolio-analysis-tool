from django.db import models


class Asset(models.Model):

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
    symbol = models.CharField(max_length=6)
    name = models.TextField()
    sector = models.CharField(max_length=2, choices=SECTORS_CHOICES)

    def __str__(self):
        return self.symbol


class HistoricValue(models.Model):

    date_time = models.DateTimeField()
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name="historic_values"
    )
    value = models.DecimalField(max_digits=9, decimal_places=2)
    currency = models.CharField(
        max_length=3
    )  # TODO: Forex market is To Be Defined into a new app. Out of scope.
