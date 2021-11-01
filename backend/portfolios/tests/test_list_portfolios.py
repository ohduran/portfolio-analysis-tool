import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.tests import UserFactory

from .factories import InvestmentFactory, PortfolioFactory


@pytest.mark.django_db
class TestListPortfolios:
    def test_example(self, client, django_user_model, django_assert_num_queries):
        user = UserFactory()
        client.force_login(user)

        portfolios = PortfolioFactory.create_batch(5, user=user)
        for portfolio in portfolios:
            InvestmentFactory(portfolio=portfolio)

        with django_assert_num_queries(4):
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
                    "user": user.id,
                }
                for portfolio in portfolios
            ],
        }
