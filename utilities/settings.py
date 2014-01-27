# Django settings for utilities project.
# import djcelery
import os
# djcelery.setup_loader()


DBBACKUP_STORAGE = 'dbbackup.storage.dropbox_storage'
DBBACKUP_TOKENS_FILEPATH = '/home5/shopmroc/utilities/dropbox_token.txt'
DBBACKUP_DROPBOX_APP_KEY = '7q8n3p6j4guc9oj'
DBBACKUP_DROPBOX_APP_SECRET = 'rkduwp7icvs0nhe'

EMAIL_HOST_USER = 'reports@shopmro.com'
EMAIL_HOST_PASSWORD = 'mumunache13!'


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

ADMINS = (
    ('admin', 'stats.infographics@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'shopmroc_utilities',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'shopmroc_utility',
        'PASSWORD': 'mumunache13!',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['shopmro.com', 'www.shopmro.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Denver'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/home5/shopmroc/public_html/images/utilities/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = 'http://shopmro.com/images/utilities/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pnd*5*wukia4r$ufemv=5z!e^j&)4%dl4m%9$+l8tqf)-t-xc#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'utilities.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'utilities.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home5/shopmroc/utilities/utilities/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'supply',
    'tracking',
    'shipping',
    'freightsolution',
    'resale_cert',
    'prices',
    'prices.tools',
    'graph',
    'tutorials',
    'south',
    #'djcelery',
    #'kombu.transport.django',
    'dbbackup',
    # 'csvimport',
    #'chronograph',
    #'django-chartit',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'quiz',
    'djangoChat',
    #'datagrid'
)

# djcelery settings

#BROKER_URL = "django://"
BROKER_URL = "redis://localhost:6379/0"
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACKS_LATE = True

import djcelery
from celery.schedules import crontab

djcelery.setup_loader()
# Where the Django project is.
#CELERYBEAT_CHDIR="/home5/shopmroc/utilities/"

# Name of the projects settings module.
#export DJANGO_SETTINGS_MODULE="settings"

# Path to celerybeat
#CELERYBEAT="/home5/shopmroc/utilities/manage.py celerybeat"

# Extra arguments to celerybeat
#CELERYBEAT_OPTS="--schedule=/home5/shopmroc/utilities/celerybeat-schedule"
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYBEAT_SCHEDULE = {
    # Executes once per day.
    'daily_graph': {
        'task': 'graph.tasks.daily_graph',
        'schedule': crontab(hour=0),
        'args': (),
    },
   
}




# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': "/home5/shopmroc/utilities/logs/logfile",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'prices': {
            'handlers': ['console', 'logfile', 'mail_admins'],
            'level': 'DEBUG',
        },
        'supply': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        'tracking': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        'shipping': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        'resale_cert': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
