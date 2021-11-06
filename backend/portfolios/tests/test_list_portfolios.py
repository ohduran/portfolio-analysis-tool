import pytest
from assets.models import Asset
from assets.tests import AssetFactory, HistoricValueFactory
from django.urls import reverse
from freezegun import freeze_time
from portfolios.models import Portfolio
from rest_framework import status
from users.tests import UserFactory

from .factories import InvestmentFactory, PortfolioFactory


@pytest.mark.django_db
class TestListPortfolios:
    def test_givenSomePortfolios_whenListingAllPortfolios_thenAllPortfoliosAreListed(
        self, client, django_assert_num_queries
    ):
        user = UserFactory()
        another_user = UserFactory()
        client.force_login(user)

        portfolios = PortfolioFactory.create_batch(5, user=user)
        for portfolio in portfolios:
            InvestmentFactory(portfolio=portfolio)

        # Some portfolios that should not appear on the list
        PortfolioFactory.create_batch(2, user=user, status=Portfolio.INACTIVE_STATUS)

        with django_assert_num_queries(6):
            response = client.get(reverse("portfolio-list"))

        assert response.status_code == status.HTTP_200_OK

        assert response.json() == {
            "count": 5,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": portfolio.id,
                    "name": portfolio.name,
                    "investments": [
                        {
                            "id": investment.id,
                            "amount": str(investment.amount),
                            "asset": investment.asset.symbol,
                        }
                        for investment in portfolio.investments.all()
                    ],
                }
                for portfolio in portfolios
            ],
        }


@pytest.mark.django_db
class TestListPortfolios:
    def test_givenAPortfolioWithInvestmentsInSectors_whenCallingSectorsEndpoint_thenItShowsInvestmentsGroupedBySector(
        self, client, django_assert_num_queries
    ):
        user = UserFactory()
        client.force_login(user)

        portfolio = PortfolioFactory(user=user)

        # 4 investments under IT
        IT_asset_1 = AssetFactory(sector=Asset.INFORMATION_TECHNOLOGY)
        with freeze_time("2021-10-03"):
            HistoricValueFactory(asset=IT_asset_1)
        with freeze_time("2021-10-04"):
            HistoricValueFactory(asset=IT_asset_1)
        with freeze_time("2021-10-05"):
            HistoricValueFactory(asset=IT_asset_1)
        with freeze_time("2021-10-06"):
            last_historic_value_IT_asset_1 = HistoricValueFactory(
                asset=IT_asset_1, close=1
            )

        IT_asset_2 = AssetFactory(sector=Asset.INFORMATION_TECHNOLOGY)
        with freeze_time("2021-10-05"):
            HistoricValueFactory(asset=IT_asset_2)
        with freeze_time("2021-10-06"):
            HistoricValueFactory(asset=IT_asset_2)
        with freeze_time("2021-10-07"):
            HistoricValueFactory(asset=IT_asset_2)
        with freeze_time("2021-10-08"):
            last_historic_value_IT_asset_2 = HistoricValueFactory(
                asset=IT_asset_2, close=2
            )

        IT_investment_1 = InvestmentFactory(
            portfolio=portfolio, asset=IT_asset_1, amount=1
        )
        IT_investment_2 = InvestmentFactory(
            portfolio=portfolio, asset=IT_asset_2, amount=2
        )

        # 2 investments under RE
        RE_asset_1 = AssetFactory(sector=Asset.REAL_ESTATE)
        with freeze_time("2021-10-07"):
            HistoricValueFactory(asset=RE_asset_1)
        with freeze_time("2021-10-08"):
            HistoricValueFactory(asset=RE_asset_1)
        with freeze_time("2021-10-09"):
            HistoricValueFactory(asset=RE_asset_1)
        with freeze_time("2021-10-10"):
            last_historic_value_RE_asset_1 = HistoricValueFactory(
                asset=RE_asset_1, close=3
            )

        RE_asset_2 = AssetFactory(sector=Asset.REAL_ESTATE)
        with freeze_time("2021-10-09"):
            HistoricValueFactory(asset=RE_asset_2)
        with freeze_time("2021-10-10"):
            HistoricValueFactory(asset=RE_asset_2)
        with freeze_time("2021-10-11"):
            HistoricValueFactory(asset=RE_asset_2)
        with freeze_time("2021-10-12"):
            last_historic_value_RE_asset_2 = HistoricValueFactory(
                asset=RE_asset_2, close=5
            )

        RE_investment_1 = InvestmentFactory(
            portfolio=portfolio, asset=RE_asset_1, amount=7
        )
        RE_investment_2 = InvestmentFactory(
            portfolio=portfolio, asset=RE_asset_2, amount=11
        )

        # An investment under FI
        FI_asset = AssetFactory(sector=Asset.FINANCIALS)
        with freeze_time("2021-10-11"):
            HistoricValueFactory(asset=FI_asset)
        with freeze_time("2021-10-12"):
            HistoricValueFactory(asset=FI_asset)
        with freeze_time("2021-10-13"):
            HistoricValueFactory(asset=FI_asset)
        with freeze_time("2021-10-14"):
            last_historic_value_FI_asset = HistoricValueFactory(
                asset=FI_asset, close=13
            )

        FI_investment = InvestmentFactory(
            portfolio=portfolio, asset=FI_asset, amount=17
        )

        with django_assert_num_queries(20):
            response = client.get(reverse("portfolio-sectors", args=[portfolio.id]))

        assert response.status_code == status.HTTP_200_OK

        assert response.json() == [
            {
                "sector": "FI",
                "total_invested": float(
                    FI_investment.amount * last_historic_value_FI_asset.close
                ),
            },
            {
                "sector": "IT",
                "total_invested": sum(
                    [
                        IT_investment_1.amount * last_historic_value_IT_asset_1.close,
                        IT_investment_2.amount * last_historic_value_IT_asset_2.close,
                    ]
                ),
            },
            {
                "sector": "RE",
                "total_invested": float(
                    sum(
                        [
                            RE_investment_1.amount
                            * last_historic_value_RE_asset_1.close,
                            RE_investment_2.amount
                            * last_historic_value_RE_asset_2.close,
                        ]
                    )
                ),
            },
        ]
