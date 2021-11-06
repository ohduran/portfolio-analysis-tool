import time
from datetime import datetime, timedelta, timezone

from assets.models import Asset
from assets.poly import (
    get_stocks_equities_daily_open_close as poly_get_stocks_equities_daily_open_close,
)
from celery import shared_task


@shared_task
def debug():
    print("This task works!!")
    pass  # do some long running task


@shared_task
def get_yesterday_stocks_equities_daily_open_close():
    API_CALLS_PER_MINUTE = 5
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    for asset in Asset.objects.all():
        poly_get_stocks_equities_daily_open_close(asset=asset, date_time=yesterday)
        time.sleep(60 / API_CALLS_PER_MINUTE)
