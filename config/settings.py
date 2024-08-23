from datetime import timedelta
from pathlib import Path
from decouple import config

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '{asctime} ({levelname}) {module}:{lineno} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
        },
        # Define a custom formatter for 12-hour format
        'custom_12hr': {
            'format': '%(message)s  -%(levelname)s  [%(asctime)s]',
            'datefmt': '%I:%M:%S %p : %m/%d/%Y'  # Set format for 12-hour time with AM/PM
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'custom_12hr',  # Use your custom formatter
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = f"'{config('SECRET_KEY')}'"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '192.168.1.*', 'localhost', '*']
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

CUSTOM_APPS = [
    'user',
    'permission'
]

INSTALLED_LIBRARIES = [
    'rest_framework',
    'corsheaders',
    'django_userforeignkey',
    'drf_spectacular',
    'rest_framework_simplejwt.token_blacklist',
]

INSTALLED_APPS = [
                     'django.contrib.admin',
                     'django.contrib.auth',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.messages',
                     'django.contrib.staticfiles',
                 ] + CUSTOM_APPS + INSTALLED_LIBRARIES

ADDED_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django_userforeignkey.middleware.UserForeignKeyMiddleware',
    'middleware.request_logger.RequestLoggingMiddleware',
]

MIDDLEWARE = [
                 'django.middleware.security.SecurityMiddleware',
                 'django.contrib.sessions.middleware.SessionMiddleware',
                 'django.middleware.common.CommonMiddleware',
                 'django.middleware.csrf.CsrfViewMiddleware',
                 'django.contrib.auth.middleware.AuthenticationMiddleware',
                 'django.contrib.messages.middleware.MessageMiddleware',
                 'django.middleware.clickjacking.XFrameOptionsMiddleware',
             ] + ADDED_MIDDLEWARE

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config('DB_ENGINE', cast=str),
        "NAME": config('DB_NAME', cast=str),
        "USER": config('DB_USER', cast=str),
        "PASSWORD": config('DB_PASSWORD', cast=str),
        "HOST": config('DB_HOST', cast=str),
        "PORT": config('DB_PORT', cast=int),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Directory where collected static files will be stored
STATIC_ROOT = BASE_DIR / 'static/collect_static'

# Additional directories to look for static files during development
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Swagger',
    'DESCRIPTION': 'Django project',
    'VERSION': '1.0.0',
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'docExpansion': 'none',
        # To prevent schema to be appeared uncomment the following
        # 'defaultModelsExpandDepth': -1,
    },
    'DEFAULT_AUTO_SCHEMA': 'drf_spectacular.openapi.AutoSchema',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PUBLIC': True,
    'USE_SESSION_AUTH': False,
    'REDUCER': 'drf_spectacular.reducing.RouterDepthReducer',
    'COMPONENT_SPLIT_REQUEST': True,

    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest",
    "SWAGGER_UI_FAVICON_HREF": STATIC_URL + "images/api.ico",

    'DEFAULT_FIELD_INSPECTORS': [
        'drf_spectacular.inspectors.CamelCaseJSONFilter',
        'drf_spectacular.inspectors.InlineSerializerInspector',
        'drf_spectacular.inspectors.RelatedFieldInspector',
        'drf_spectacular.inspectors.ChoiceFieldInspector',
        'drf_spectacular.inspectors.FileFieldInspector',
        'drf_spectacular.inspectors.DictFieldInspector',
        'drf_spectacular.inspectors.SimpleFieldInspector',
        'drf_spectacular.inspectors.StringDefaultFieldInspector',
    ],

}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=60),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
