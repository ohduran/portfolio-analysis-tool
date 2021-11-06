import os
from datetime import datetime, timezone
from unittest import mock

import pytest
import responses
from freezegun import freeze_time
from users.tests import UserFactory

from ..poly import get_stocks_equities_daily_open_close
from .factories import AssetFactory


@pytest.mark.django_db
class TestPolygon:
    @responses.activate
    @freeze_time("2021-10-05 12:00:13")
    @mock.patch.dict(os.environ, {"POLYGON_API_KEY": "secret-polygon-api-key"})
    def test_givenASymbolAndADate_whenCallingThePolygonAPI_thenACorrectHistoricValueIsCreated(
        self, client, django_assert_num_queries
    ):

        asset = AssetFactory()

        # https://polygon.io/docs/get_v1_open-close__stocksTicker___date__anchor
        responses.add(
            responses.GET,
            f"https://api.polygon.io/v1/open-close/{asset.symbol}/2021-10-05?apiKey=secret-polygon-api-key",
            json={
                "afterHours": 322.1,
                "close": 325.12,
                "from": "2021-10-05T00:00:00.000Z",
                "high": 326.2,
                "low": 322.3,
                "open": 324.66,
                "preMarket": 324.5,
                "status": "OK",
                "symbol": asset.symbol,
                "volume": 26122646,
            },
        )

        user = UserFactory()
        client.force_login(user)

        with django_assert_num_queries(1):
            get_stocks_equities_daily_open_close(asset, datetime.now(timezone.utc))

        asset.refresh_from_db()

        assert asset.historic_values.count() == 1

        historic_value = asset.historic_values.first()

        assert float(historic_value.after_hours) == 322.1
        assert float(historic_value.close) == 325.12
        assert float(historic_value.high) == 326.2
        assert float(historic_value.low) == 322.3
        assert float(historic_value._open) == 324.66
        assert float(historic_value.pre_market) == 324.5
        assert float(historic_value.volume) == 26122646
        assert historic_value.date_time == datetime(
            2021, 10, 5, 0, 0, tzinfo=timezone.utc
        )
