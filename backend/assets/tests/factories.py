import random

import factory
from contrib.tests.utilities import random_amount
from faker import Faker

from ..models import Asset, HistoricValue

fake = Faker()


class AssetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Asset

    symbol = factory.LazyAttribute(
        lambda _: fake.random_uppercase_letter() * fake.random_int(min=1, max=6)
    )
    name = factory.LazyAttribute(lambda _: fake.company())
    sector = factory.LazyAttribute(lambda _: random.choice(Asset.SECTORS_CHOICES)[0])


class HistoricValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HistoricValue

    date_time = factory.LazyAttribute(lambda _: fake.date_time())
    asset = factory.SubFactory(AssetFactory)

    value = factory.LazyAttribute(lambda _: random_amount())
    currency = factory.LazyAttribute(lambda _: fake.random_uppercase_letter() * 3)
