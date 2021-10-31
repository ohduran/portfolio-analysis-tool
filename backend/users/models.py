from django.contrib.auth.models import AbstractUser
from django.db import models


# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class CustomUser(AbstractUser):
    pass
