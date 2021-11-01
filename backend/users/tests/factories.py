import factory
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(
        lambda _: fake.profile(fields=["username"])["username"]
    )
    email = factory.LazyAttribute(lambda _: fake.email())
