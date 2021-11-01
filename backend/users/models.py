from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import ActivatorModel, TimeStampedModel


# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class CustomUser(ActivatorModel, TimeStampedModel, AbstractUser):
    pass
