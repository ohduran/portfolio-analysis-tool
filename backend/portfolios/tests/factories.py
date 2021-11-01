import factory
from assets.tests import AssetFactory
from contrib.tests import random_amount
from faker import Faker
from users.tests import UserFactory

from ..models import Investment, Portfolio

fake = Faker()


class PortfolioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Portfolio

    user = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda _: fake.company())


class InvestmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Investment

    portfolio = factory.SubFactory(PortfolioFactory)
    asset = factory.SubFactory(AssetFactory)
    amount = factory.LazyAttribute(lambda _: random_amount())
