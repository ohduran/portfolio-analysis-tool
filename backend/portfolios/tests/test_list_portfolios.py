import pytest
from django.urls import reverse
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
