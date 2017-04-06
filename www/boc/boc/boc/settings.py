"""
Django settings for boc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*$sgsrt2f=qu-k1lgddp^^)x0+qk0s#9z)y(n&fwb^2eiegw#q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['.betoncombat.com']

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
                  
      'django.contrib.auth',
      'django.contrib.admin',
      'django.contrib.sites',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.flatpages',
      'django.contrib.staticfiles',
      'django.contrib.contenttypes',
      'django.contrib.humanize',
      'django.contrib.sitemaps',
      #'django_comments',
      
      'boc',
      
      'allauth',
      'allauth.account',
      'allauth.socialaccount',
      
      
      'carousel',
      'opportunity',
      'testimonial',
      'followpost',
      'advisory',
      'userprofile',
      'odds',
      'predictions',
      'statistics',
      'bookmakers',
      'mma',
      'investor',
      'news',
      'fantasy',
      'chat',
      'consulting',
      
      'locality',
      'clever_selects',
      'bootstrapform',
      'tinymce',
      'ckeditor',
      'mptt',
       
       'django_forms_bootstrap',
       'payments',
       'django_crontab',
       'autoslug'
       
)

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

TEMPLATE_LOADERS = (
    'app_namespace.Loader',
    'django.template.loaders.app_directories.Loader'
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Already defined Django-related contexts here
               'django.core.context_processors.i18n',
               'django.core.context_processors.request',
               'django.core.context_processors.media',
               'django.core.context_processors.request',
               'django.contrib.auth.context_processors.auth',
               'boc.context_processors.stripekey',
               'django.core.context_processors.static',
                # `allauth` needs this from django
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth'
            ],
        },
    },
]


ROOT_URLCONF = 'boc.urls'

WSGI_APPLICATION = 'boc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

TIME_ZONE = 'UTC'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'boc',  # Or path to database file if using sqlite3.
        'USER': 'root',
        'PASSWORD': 'Unfightable7!',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',  # Set to empty string for default.
        'OPTIONS': {
        'init_command': ("SET time_zone='%s'" % TIME_ZONE),
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'boc/static'),)

TEMPLATE_DIRS = (
                 os.path.join(BASE_DIR, 'boc/templates'),
                 )

TEMPLATE_LOADERS = (
'django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader',
'app_namespace.Loader', 
)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


TINYMCE_DEFAULT_CONFIG = {
  'allow_script_urls': True,
  'allow_html_in_named_anchor': True,
  'width': '80%',
  'height': 500
}

#STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "pk_test_Wwl9beC1fBYmPmEBAxl4CxjB")
#STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test_29br76r10UWEnAn8JfCCTLTj")


STRIPE_PUBLIC_KEY = "pk_live_31WsGOogsEYXi99QVSwBMQGh"
STRIPE_SECRET_KEY = "sk_live_vm70F1EbyOY5YboOHWggiWBi"


CRONJOBS = [
    ('6 3 * * *', 'boc.cron.pull_mma_feed', '> /cron/pull_mma_feed.log'),
    ('*/5 * * * *', 'boc.cron.pull_odds_feed', '> /cron/pull_odds.log'),
]



PAYMENTS_PLANS = {
    "weekly": {
        "stripe_plan_id": "premium_week",
        "name": "Premium Account ($49/week)",
        "description": "The weekly subscription plan to Bet on Combat",                                                                   
        "price": 49.99,
        "currency": "usd",
        "interval": "week"
    },
    "monthly": {
        "stripe_plan_id": "premium",
        "name": "Premium Account ($99/month)",
        "description": "The monthly subscription plan to Bet on Combat",
        "price": 99.99,
        "currency": "usd",
        "interval": "month"
    },
    "yearly": {
        "stripe_plan_id": "premium_year",
        "name": "Premium Account ($999/year)",
        "description": "The yearly subscription plan to Bet on Combat",
        "price": 999.99,
        "currency": "usd",
        "interval": "year"
    }
}

#allauth Settings
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
MAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = True
EMAIL_HOST = 'smtpout.secureserver.net'
EMAIL_HOST_USER = 'info@betoncombat.com'
EMAIL_HOST_PASSWORD = 'makemoney'
EMAIL_PORT = 80
DEFAULT_FROM_EMAIL = 'info@betoncombat.com'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of 'allauth'
    "django.contrib.auth.backends.ModelBackend",
    # 'allauth' specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_USERNAME_MIN_LENGTH = 3

LOGIN_REDIRECT_URL = "/"

SOCKETIO_HOST = '127.0.0.1'

SOCKETIO_PORT = '9000'

ACCOUNT_SIGNUP_FORM_CLASS = 'boc.forms.SignupForm'
"""
try:
    from local_settings import *
except ImportError:
    pass
"""
