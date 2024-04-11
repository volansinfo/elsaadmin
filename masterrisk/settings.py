"""
Django settings for masterrisk project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import raven as raven

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "i6ova@vbbe4a529#7r5@@qr!!&r%*qdj$u1+nr+_u%h!mp-dc+"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "yes") == "yes"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "proxy",
    "http://localhost:4200"
    "django",
    "printserver",
    "riskcloud.codepartner.cloud",
    "masterrisktool.com",
    'masterrisktool.com',
    "apiewn.unilink360.com",
    "apiewn.unilink360.com",
]

HOSTNAME = os.getenv("HOSTNAME", "localhost")
PROTOCOL = os.getenv("PROTOCOL", "http")

# Application definition


INSTALLED_APPS = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "djrichtextfield",
    "rest_framework",
    "django_rest_passwordreset",
    "corsheaders",
    "colorfield",
    "rangefilter",
    "drf_spectacular",
    "masterdata",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]


CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = "masterrisk.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "masterrisk.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# use_postgres = os.getenv("POSTGRES", "0")
# DATABASES = {}
# if use_postgres == "1":
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql_psycopg2",
#             "NAME": os.getenv("POSTGRES_DB", "postgres"),
#             "USER": os.getenv("POSTGRES_USER", "postgres"),
#             "PASSWORD": os.getenv("POSTGRES_PASSWORD", "456"),
#             "HOST": os.getenv("POSTGRES_HOST", "localhost"),
#             "PORT": os.getenv("POSTGRES_PORT", 5432),
#         }
#     }
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql_psycopg2",
#             "NAME": os.getenv("POSTGRES_DB", "postgres"),
#             "USER": os.getenv("POSTGRES_USER", "postgres"),
#             "PASSWORD": os.getenv("POSTGRES_PASSWORD", "456"),
#             "HOST": os.getenv("POSTGRES_HOST", "localhost"),
#             "PORT": os.getenv("POSTGRES_PORT", 5432),
#         }
#     }
use_postgres = os.getenv("POSTGRES", "0")
DATABASES = {}
if use_postgres == "1":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("POSTGRES_DB", "elsaAdmin"),
            "USER": os.getenv("POSTGRES_USER", "nLF5Bj8ARYqj9rZc"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "wD4:zL3&zK3&jD7$"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", 31522),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("POSTGRES_DB", "elsaAdmin"),
            "USER": os.getenv("POSTGRES_USER", "nLF5Bj8ARYqj9rZc"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "wD4:zL3&zK3&jD7$"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", 31522),
        }
    }

if os.getenv("POSTGRES_SSLMODE", "no") == "no":
    DATABASES["default"]["OPTIONS"] = {}
else:
    DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "masterdata.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda s: s
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
LANGUAGES = (
    ("en", gettext("English")),
    ("de", gettext("German")),
    ("es", gettext("Spanish")),
    ("fr", gettext("French")),
    ("pt", gettext("Portuguese")),
    ("ru", gettext("Russian")),
    ("zh-tw", "简体中文"),
)

DJRICHTEXTFIELD_CONFIG = {
    "js": ["//cdn.ckeditor.com/4.14.0/standard/ckeditor.js"],
    "init_template": "djrichtextfield/init/ckeditor.js",
    "settings": {  # CKEditor
        "toolbar": [
            {"items": ["Format", "-", "Bold", "Italic", "-", "RemoveFormat"]},
            {"items": ["Link", "Unlink", "Image", "Table"]},
            {"items": ["Source"]},
        ],
        "format_tags": "p;h1;h2;h3",
        "width": 700,
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(DATA_DIR, "media")
STATIC_ROOT = os.path.join(DATA_DIR, "static")

ACCESS_TOKEN_LIFETIME = timedelta(hours=2)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

LEGACY_DATA_REPO = os.getenv(
    "LEGACY_DATA_REPO",
    "https://gitlab+deploy-token-27:rkgNsB4g6Ai5egHVSNgw@git.dezign-api.de/ew/risk-tool-data.git",
)

LEGACY_I18N_REPO = os.getenv(
    "LEGACY_I18N_REPO",
    "https://gitlab+deploy-token-28:erJm-ZSzQM3rPxJZR28h@git.dezign-api.de/ew/risk-tool.git",
)

# SWAGGER_SETTINGS = {
#     "SECURITY_DEFINITIONS": {
#         "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
#     }
# }
SPECTACULAR_SETTINGS = {"SCHEMA_PATH_PREFIX": "/backend/masterdata/"}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = "EW Nutrition Risk Cloud <pankaj.volancs@gmail.com>"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_PASSWORD = "flnjagmhdxhyutic"
EMAIL_HOST_USER = "pankaj.volancs@gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True


#  host: 'smtp.gmail.com',
#   port: '465',
#   auth: {
#     user: 'pankaj.volancs@gmail.com',
#     pass: 'flnjagmhdxhyutic'
#   }
DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 2

if DEBUG is False:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    #äSTATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "dezign")
    AWS_S3_ENDPOINT_URL = os.getenv(
        "AWS_S3_CUSTOM_DOMAIN", "https://s3.eu-central-1.wasabisys.com"
    )
    AWS_S3_CUSTOM_DOMAIN = (
        f"{AWS_STORAGE_BUCKET_NAME}.s3.eu-central-1.wasabisys.com"
    )
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_LOCATION = "ewn-riskcloud"
    AWS_DEFAULT_ACL = "public-read"

    #STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"

    INSTALLED_APPS.append(
        "raven.contrib.django.raven_compat",
    )
    RAVEN_CONFIG = {
        "dsn": "",
        "release": os.getenv("GIT_COMMIT_SHA", "unknown"),
    }

REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379"


MASTERRISK_MOVING_RISK_FOR_MONTHS = 6


sentry_dsn = os.getenv("SENTRY_DSN", False)

if sentry_dsn and sentry_dsn != "no":
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0,
        send_default_pii=True,
    )
