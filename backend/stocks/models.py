from django.db import models


class Stock(models.Model):

    # Stocks listed on the New York Stock Exchange (NYSE) can have four or fewer letters.
    # Nasdaq-listed securities can have up to five characters.
    symbol = models.CharField(max_length=6)
    name = models.TextField()


class HistoricValue(models.Model):

    date_time = models.DateTimeField()
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="historic_values"
    )
    value = models.DecimalField(max_digits=9, decimal_places=2)
    currency = models.CharField(max_length=3, default="BTC")
