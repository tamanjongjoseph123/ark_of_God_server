import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env only locally
if os.environ.get('RENDER', None) is None:
    from dotenv import load_dotenv
    load_dotenv()

# Security
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-your-default-dev-key-here")
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

# Allowed Hosts
ALLOWED_HOSTS = []
if os.environ.get("ALLOWED_HOSTS"):
    ALLOWED_HOSTS.extend(os.environ.get("ALLOWED_HOSTS").split(","))
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '10.51.148.169'])

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'api',
    'cloudinary',
    'cloudinary_storage',
]

APPEND_SLASH = False

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

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'server.wsgi.application'

#Database
DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and Media
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'api.User'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173/",
    'https://b99e3c29.ark-of-god-admin-new.pages.dev/'
]


# Storage Backend: FTP
STORAGES = {
    "default": {
        "BACKEND": "server.storage_backends.FTPStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

FTP_STORAGE_OPTIONS = {
    "host": "st60307.ispot.cc",
    "username": "nostress@st60307.ispot.cc",
    "password": "nostress2025",
    "base_path": "/",
    "port": 21,
    "passive": True,
}
# Media (uploads)
MEDIA_URL = "https://st60307.ispot.cc/nostress/"
MEDIA_ROOT = BASE_DIR / "media"