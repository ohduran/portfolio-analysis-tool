import os
from datetime import datetime

from assets.models import Asset, HistoricValue
from polygon import RESTClient


def get_stocks_equities_daily_open_close(asset: Asset, date_time: datetime) -> None:
    key: str = os.environ["POLYGON_API_KEY"]
    date: str = date_time.strftime("%Y-%m-%d")  # YYYY-MM-DD

    # https://requests.readthedocs.io/en/master/user/advanced/#session-objects
    with RESTClient(key) as client:
        response = client.stocks_equities_daily_open_close(asset.symbol, date)
        print(
            f"On: {response.from_} {response.symbol} opened at {response.open} and closed at {response.close}"
        )

    if response.status == "OK":
        HistoricValue.objects.get_or_create(
            asset=asset,
            date_time=date_time.replace(hour=0, minute=0, second=0, microsecond=0),
            defaults={
                "currency": "USD",
                "after_hours": response.after_hours,
                "close": response.close,
                "high": response.high,
                "low": response.low,
                "_open": response.open,
                "pre_market": response.pre_market,
                "volume": response.volume,
            },
        )
