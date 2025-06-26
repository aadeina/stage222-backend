import os
from pathlib import Path
from decouple import config, Csv
from datetime import timedelta

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ======================
# EMAIL CONFIGURATION
# ======================
# Email Settings
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')


# Email Verification Redirect Base (Frontend)
FRONTEND_URL = config('FRONTEND_URL')

# settings.py
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ======================
# PASSWORD VALIDATORS
# ======================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ======================
# SECURITY
# ======================

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


ALLOWED_HOSTS = [
    "stage222-backend.onrender.com",
    "api.stage222.com",
    "localhost",
    "127.0.0.1"
]


# ======================
# APPLICATIONS
# ======================

INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework.authtoken',


    # Allauth core
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',


    # Project apps
    'accounts',
    'candidates',
    'recruiters',
    'organizations',
    'internships',
    'applications',
    'messaging',  # Renamed to avoid conflict with Django's built-in messages
    "bookmarks",
    'adminpanel'
]
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Google already verifies

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_SECRET'),
        }
    },
    'facebook': {
        'APP': {
            'client_id': os.environ.get('FACEBOOK_CLIENT_ID'),
            'secret': os.environ.get('FACEBOOK_SECRET'),
        }
    }
}


# ======================
# MIDDLEWARE
# ======================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# ======================
# URL & WSGI / ASGI
# ======================

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# ======================
# DATABASE
# ======================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# ======================
# REST FRAMEWORK & JWT
# ======================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,  # You can change this number as needed
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
# 🔐 Tell Allauth clearly: No username field used at all
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True

# ✅ Login method
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# ✅ Only these fields in signup
ACCOUNT_SIGNUP_FIELDS = ['email', 'password1', 'password2']

# ✅ Clean modern config for dj-rest-auth
REST_AUTH = {
    "SIGNUP_FIELDS": {
        "email": {"required": True},
        "password1": {"required": True},
        "password2": {"required": True}
    }
}


REST_USE_JWT = True



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_BLACKLIST_ENABLED': True,
}


# ======================
# CUSTOM USER MODEL
# ======================

AUTH_USER_MODEL = 'accounts.User'


# ======================
# INTERNATIONALIZATION
# ======================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nouakchott'
USE_I18N = True
USE_TZ = True

# ======================
# STATIC & MEDIA FILES
# ======================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ======================
# DEFAULT PRIMARY KEY TYPE
# ======================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================
# CORS SETTINGS
# ======================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",        # Vite default
    "http://localhost:5174",        # Your current dev server
    "http://127.0.0.1:5173",        # Access via 127.0.0.1
    "https://stage222.com",         # Your production domain
]
CORS_ALLOW_CREDENTIALS = True

# ======================
# CHINGUISOFT SMS API
# ======================

CHINGUISOFT_VALIDATION_KEY = config('CHINGUISOFT_VALIDATION_KEY')
CHINGUISOFT_VALIDATION_TOKEN = config('CHINGUISOFT_VALIDATION_TOKEN')
CHINGUISOFT_API_BASE_URL = config('CHINGUISOFT_API_BASE_URL')

# ======================
# SENDGRID API
# ======================

SENDGRID_API_KEY = config("SENDGRID_API_KEY")

