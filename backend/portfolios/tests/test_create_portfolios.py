import json

import pytest
from assets.tests import AssetFactory
from django.urls import reverse
from rest_framework import status
from users.tests import UserFactory

from ..models import Investment, Portfolio
from .factories import InvestmentFactory, PortfolioFactory


@pytest.mark.django_db
class TestCreatePortfolio:
    def test_givenCorrectInformation_whenPostingANewPortfolio_thenANewPortfolioIsCreated(
        self, client, django_assert_num_queries
    ):
        user = UserFactory()
        asset = AssetFactory()
        another_asset = AssetFactory()
        client.force_login(user)

        json_data = {
            "name": "Name of the Portfolio",
            "investments": [
                {
                    "amount": 10,
                    "asset": asset.symbol,
                },
                {
                    "amount": 100,
                    "asset": another_asset.symbol,
                },
            ],
        }

        with django_assert_num_queries(12):
            response = client.post(
                reverse("portfolio-list"),
                json.dumps(json_data),
                content_type="application/json",
            )

        assert response.status_code == status.HTTP_201_CREATED, response.content

        assert Portfolio.objects.count() == 1
        portfolio = Portfolio.objects.first()
        assert portfolio.name == "Name of the Portfolio"

        assert portfolio.investments.count() == 2

        first_investment = portfolio.investments.first()
        last_investment = portfolio.investments.last()

        assert first_investment.amount == 10
        assert first_investment.asset == asset
        assert last_investment.amount == 100
        assert last_investment.asset == another_asset
