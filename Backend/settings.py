import os
from pathlib import Path
print("CURRENT ALLOWED_HOSTS =", ALLOWED_HOSTS)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
 
 
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
 
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_0hafal#t73@!b0ori-!e(gq*l$!_9hqzr+838q1!=#g@govx0'
 
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
 
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mes-backend-1.onrender.com']
 
 
# Application definition
 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'auth_app',
    'Backend',

 
 
    # 'Backend.auth_app',
    # 'auth_app',
    # 'auth_app.apps.AuthAppConfig'
 
]
 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  
 
 
]
 
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Angular development server
    'mes-backend-1.onrender.com',  # render server

]
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
]
ROOT_URLCONF = 'Backend.urls'
CORS_ALLOW_ALL_ORIGINS = True
 
 
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
 
WSGI_APPLICATION = 'Backend.wsgi.application'
 
 
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',  # Replace with your PostgreSQL server's address if necessary
        'PORT': '5432',          # Leave empty to use the default PostgreSQL port (usually 5432)
    }
}
 
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
 
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/
 
LANGUAGE_CODE = 'en-us'
 
TIME_ZONE = 'UTC'
 
USE_I18N = True
 
USE_TZ = True
 
 
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
 
STATIC_URL = 'static/'
 
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
 
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'auth_app.User'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER ='karim01atigui@gmail.com'
EMAIL_HOST_PASSWORD = 'jlyk atjv kivq zxiu'

DEFAULT_FROM_EMAIL = 'Karim Atigui <karim01atigui@gmail.com>'




MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

