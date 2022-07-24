"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
# STATIC_DIR = os.path.join(BASE_DIR,'static')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '***************************************************'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['azaleabooks.herokuapp.com', '127.0.0.1', '.azaleabooks.com'] #'.azaleabooks.com'



DEFAULT_FROM_EMAIL = "Azalea Books <help.azaleabooks@gmail.com>"

EMAIL_HOST = "smtp.gmail.com" 
EMAIL_HOST_USER = "help.azaleabooks@gmail.com"
EMAIL_HOST_PASSWORD =  "************"
EMAIL_PORT = 587
EMAIL_USE_TLS = True


SITE_URL = "http://azaleabooks.herokuapp.com"
# if DEBUG:
#     SITE_URL = "http://127.0.0.1:8000"


# Application definition

INSTALLED_APPS = [
    'products.apps.ProductsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Blog',
    'carts',
    'orders',
    'accounts.apps.AccountsConfig',
    'crispy_forms',
    'localflavor',
    'widget_tweaks',
    'mptt',
    'ckeditor',
    'storages',
    # 'stripe',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600) #postgreSQL Database in heroku
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True



#S3 BUCKETS CONFIG

AWS_ACCESS_KEY_ID = '*******************'
AWS_SECRET_ACCESS_KEY = '***************'
AWS_STORAGE_BUCKET_NAME = 'azaleabooks-bucket'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_CUSTOM_DOMAIN = f"azaleabooks-bucket.s3.amazonaws.com"
PUBLIC_MEDIA_LOCATION = 'media'
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR,"static","static_root")

STATIC_URL = '/static/'
# MEDIA_URL = '/media/'
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
MEDIA_ROOT = os.path.join(BASE_DIR,"static","media")
# MEDIA_ROOT = 'C:/Users/yash/Desktop/azalea_books/static/media/'



STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static","static_files")
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# STRIPE_SECRET_KEY = "sk_test_51HL0NeLZHwJaveHYs5TrQTioiqkpMIYgQjo02HsSgAnJv6BtllkUIGObxwxBiJOTSySu1IekPpCFTmt0fPYutlv40072YbiYZz"
# STRIPE_PUBLISHABLE_KEY = "pk_test_51HL0NeLZHwJaveHY9ZeMTrvYHpCNZ3ofiGGRNmMCVxFbnnzXp0HXN8P1YxN8DCn7Qs2J4kQwcKnRRLjahIvh2OjS00ycvzSSx8"


CRISPY_TEMPLATE_PACK = 'bootstrap4'

#...
SITE_ID = 1

####################################
    ##  CKEDITOR CONFIGURATION ##
####################################

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = 'products/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}



# Activate Django-Heroku.
django_heroku.settings(locals(), staticfiles=False)
