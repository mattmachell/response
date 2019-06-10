"""
Django settings for incident project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
import logging
from slackclient import SlackClient
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c+*z3&f$!v@am35()o57_l885=t$2vlw*w#*jusz0qiyi#h_iz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ui.apps.UiConfig',
    'after_response',
    'rest_framework',
    'bootstrap4',
    'core.apps.CoreConfig',
    'slack.apps.SlackConfig',
    'pagerduty.apps.PagerdutyConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'response.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'ui/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'response.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_ROOT = 'static'
STATIC_URL = '/static/'


# Django Rest Framework
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Markdown Filter

MARKDOWN_FILTER_WHITELIST_TAGS = [
    'a',
    'p',
    'code',
    'h1',
    'h2',
    'ul',
    'li',
    'strong',
    'em',
    'img',
]

MARKDOWN_FILTER_WHITELIST_ATTRIBUTES = [
    'src',
    'style',
]

MARKDOWN_FILTER_WHITELIST_STYLES = [
    'width', 'height', 'border-color', 'background-color',
    'white-space', 'vertical-align', 'text-align',
    'border-style', 'border-width', 'float', 'margin',
    'margin-bottom', 'margin-left', 'margin-right', 'margin-top'
]


# Useful Functions for env specific settings

def get_user_id(user_name, token):
    slack_client = SlackClient(token)
    response = slack_client.api_call(
        "users.list"
    )
    if not response.get("ok", False):
        raise ImproperlyConfigured(f"Failed to get user id of \"{user_name}\" : {response['error']}")
    for user in response['members']:
        if user['name'] == user_name:
            return user['id']

    raise ImproperlyConfigured(f"Failed to get user id of \"{user_name}\"")


def get_channel_id(channel_name, token):
    slack_client = SlackClient(token)
    response = slack_client.api_call(
        "channels.list",
        exclude_archived=True,
        exclude_members=True,
    )
    if not response.get("ok", False):
        raise ImproperlyConfigured(f"Failed to get channel id for \"{channel_name}\" : {response['error']}")

    for channel in response['channels']:
        if channel['name'] == channel_name:
            return channel['id']

    raise ImproperlyConfigured(f"Failed to get channel id for \"{channel_name}\"")


def get_env_var(setting, warn_only=False):
    value = os.getenv(setting, None)

    if not value:
        error_msg = f"ImproperlyConfigured: Set {setting} environment variable"
        if warn_only:
            logger.warn(error_msg)
        else:
            raise ImproperlyConfigured(error_msg)
    else:
        value = value.replace('"', '')  # remove start/end quotes

    return value
