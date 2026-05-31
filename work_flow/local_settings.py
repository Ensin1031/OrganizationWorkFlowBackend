import os

from .settings import *
from django.views.decorators.cache import never_cache


ALLOWED_HOSTS = ["*", ]

os.environ.setdefault('SECRET_KEY', 'django-insecure-ys_q1u2ba1#@gro@q5n!v!&2e=#wa_ad51codr*-38dd3kl9u*')
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True
HOST_URL = os.environ.get("HOST_URL", "http://localhost:8000")

os.environ.setdefault('E_FLOWER_HOST', '127.0.0.1')
os.environ.setdefault('E_FLOWER_PORT', '5555')
os.environ.setdefault("E_DB_DATABASE", 'work_flow')
os.environ.setdefault("E_DB_DATABASE_TEST", 'work_flow_test')
os.environ.setdefault("E_DB_USER", 'work_flow')
os.environ.setdefault("E_DB_PASSWORD", 'work_flow')
os.environ.setdefault("E_DB_ADDRESS", 'localhost')
os.environ.setdefault("E_DB_PORT", '15432')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("E_DB_DATABASE"),
        'USER': os.environ.get("E_DB_USER"),
        'PASSWORD': os.environ.get("E_DB_PASSWORD"),
        'HOST': os.environ.get("E_DB_ADDRESS"),
        'PORT': os.environ.get("E_DB_PORT"),
        'TEST': {
            'NAME': os.environ.get("E_DB_DATABASE_TEST"),
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    },
    'viewset': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'settings': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'method_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'lock_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'licences_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

CACHE_FUNC = lambda seconds, cache: never_cache  # noqa

# во время разработки - отправляем письма в консоль
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SIGNING_ENABLED = True

# Если True — клиент будет доверять сертификату сервера (игнорирует ошибки SSL).
DATABASE_TRUST_SERVER_CERTIFICATE = True


# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('localhost', 6379)],
#         },
#     },
# }


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
