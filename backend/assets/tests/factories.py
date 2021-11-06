import random

import factory
from contrib.tests.utilities import random_positive_amount
from django.utils import timezone
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

    date_time = factory.LazyAttribute(lambda _: timezone.now())
    asset = factory.SubFactory(AssetFactory)

    currency = "EUR"

    after_hours = factory.LazyAttribute(lambda _: random_positive_amount())
    pre_market = factory.LazyAttribute(lambda _: random_positive_amount())
    close = factory.LazyAttribute(lambda _: random_positive_amount())
    high = factory.LazyAttribute(lambda _: random_positive_amount())
    low = factory.LazyAttribute(lambda _: random_positive_amount())
    _open = factory.LazyAttribute(lambda _: random_positive_amount())
    volume = factory.LazyAttribute(lambda _: random_positive_amount())
