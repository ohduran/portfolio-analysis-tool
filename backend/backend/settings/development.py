import os

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "cx8&=ho5h7_(0i_g&(j%@^0)3)(*lw7xq^2a2&v=4sder2gwaj"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["django", "0.0.0.0"]

INSTALLED_APPS += [
    "django_extensions",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432,
    }
}


if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }

CELERY_BROKER = os.environ.get("CELERY_BROKER", "redis://127.0.0.1:6379/0")
CELERY_BACKEND = os.environ.get("CELERY_BACKEND", "redis://127.0.0.1:6379/0")
