import os
from pathlib import Path

import dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / '.env'
if env_path.exists():
    dotenv.load_dotenv(env_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')


def get_debug():
    debug_value = os.getenv('DEBUG')
    state = True if debug_value == '1' else False
    return state


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost'
]


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_extensions',
    'drf_spectacular',
    'import_export',

    'scores'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'faces.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
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

# WSGI_APPLICATION = 'faces.wsgi.application'
ASGI_APPLICATION = 'faces.asgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'my_faces'),
#         'USER': os.environ.get('DB_USER', 'test_user'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'touparet'),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'my_faces.sqlite3'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]


MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Restframework

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:8100'
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:8100'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}


# Redis

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')

REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:6379'

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')

RABBITMQ_USER = os.getenv('RABBITMQ_DEFAULT_USER', 'guest')

RABBITMQ_PASSWORD = os.getenv('RABBITMQ_DEFAULT_PASS', 'guest')

CELERY_BROKER_URL = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:5672'

CELERY_RESULT_BACKEND = REDIS_URL

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'Europe/Oslo'


if os.getenv('USES_HTTP_SCHEME', 'http') == 'https':
    SESSION_COOKIE_SECURE = True

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    SECURE_PROXY_SSL_HEADERSSL_REDIRECT = True


# Cache

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'TIMEOUT': 60 * 15,
        'OPTIONS': {
            'PASSWORD': REDIS_PASSWORD,
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        }
    },
    'memcache': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'memcache:11211'
    }
}


# Emailing

EMAIL_HOST = os.getenv('EMAIL_HOST')

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS = True

EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


# Channels
# https://channels.readthedocs.io/en/latest/topics/channel_layers.html

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL]
        }
    }
}
