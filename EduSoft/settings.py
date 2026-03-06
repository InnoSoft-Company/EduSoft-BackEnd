from datetime import timedelta
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-_!5_u_8o94o@m5@_i2a%jz-77q5!_($)t&yi6+43z@%l(9zm+l')

ProjectName = "EduSoft"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
  "http://localhost:8000",
  "http://127.0.0.1",
  "https://back-end.edusoft.midoghanam.site",
  'https://e50909ae31ae52a5-156-201-21-94.serveousercontent.com',
]

INSTALLED_APPS = [
  'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.messages', 'django.contrib.staticfiles', 'django.contrib.sessions',
  'drf_yasg',
  'authentication', 'core', 
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

ROOT_URLCONF = f'{ProjectName}.urls'
AUTH_USER_MODEL = 'authentication.Users'

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

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WSGI_APPLICATION = f'{ProjectName}.wsgi.application'
ASGI_APPLICATION = f'{ProjectName}.asgi.application'

# Use custom user model from authentication app
AUTH_USER_MODEL = 'authentication.Users'

# REST Framework defaults
SIMPLE_JWT = {
  "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
  "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
  "ROTATE_REFRESH_TOKENS": True,
  "BLACKLIST_AFTER_ROTATION": True,
  "AUTH_HEADER_TYPES": ("Bearer",),
}

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
      'rest_framework.authentication.TokenAuthentication',
      'rest_framework.authentication.SessionAuthentication',
      'rest_framework_simplejwt.authentication.JWTAuthentication',
  ),
  'DEFAULT_PERMISSION_CLASSES': (
      'rest_framework.permissions.IsAuthenticatedOrReadOnly',
  ),
}

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
#DATABASES = {
#  'default': {
#      'ENGINE': 'django.db.backends.sqlite3',
#      'NAME': BASE_DIR / 'main.db',
#  }
#}

DATABASES = { 
    'default': { 
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': 'edusoft', 
        'USER': 'edusoft', 
        'PASSWORD': 'EduSoft@2026@',
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }, 
}

# Password validation
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
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True
USE_I18N = True
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'),]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
#STATICFILES_DIRS = [BASE_DIR / 'website/static/staticDir']
STATIC_ROOT = BASE_DIR / 'website/static/collectedStatic'  # ده لو هتعمل collectstatic

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'website/static/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
  "default": {
  "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
  "LOCATION": "caches",
  }
}

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
