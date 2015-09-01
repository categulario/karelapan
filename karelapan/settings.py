# -*- coding:utf-8 -*-
import os
import logging
PROJECT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Abraham Toriz Cruz', 'karelapan@gmail.com'),
    ('Julio Aguilar', 'madth3@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'covi',
        'USER': 'covi',
        'PASSWORD': 'covi',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.karelapan.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Mexico_City'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-mx'

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
MEDIA_ROOT = '/home/covi/temp/staticfiles/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = 'http://static.covi.org.mx/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/covi/temp/staticfiles/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = 'http://static.covi.org.mx/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    os.path.normpath(os.path.join(os.path.dirname(__file__),'../assets')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-01jld9has!14)!p-6-av%lrp&vsr@7ud7sqs^p3mws-mv1z^@'

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

ROOT_URLCONF = 'karelapan.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'karelapan.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'apps.usuarios',
    'apps.evaluador',
    'apps.sitio',
    'gunicorn',
    'tinymce',
    'django.contrib.humanize',
    'south',
    'django_notify',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'wiki.plugins.macros',
    'apps.bootstrapy',
    'apps.karelecatl',
    'apps.libro',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

GOOGLE_ANALYTHICS = True
FACEBOOK = True
BASE_URL = 'karelapan.com'

MESSAGE_TAGS = {
    50: 'problem_debug'
}

LOGIN_URL = '/usuarios'

RECAPTCHA_PRIVATE_KEY = '6LcsLeMSAAAAAIZK9hnABwjYqePREa_UXdE2ugll'
RECAPTCHA_PUBLIC_KEY = '6LcsLeMSAAAAACtSgJKW0jCrLSC5zPg8Av2ZgT-H'

RAIZ_CODIGOS = os.path.join(MEDIA_ROOT, 'codigos')+'/'

#Cosas del demonio evaluador de karel
#Ruta absoluta al archivo del registro
LOGFILE = 'registro.log'
#Formato del registro
LOG_FORMAT = '[%(asctime)s] %(levelname)s %(message)s'
#Nivel del registro
LOG_LEVEL = logging.DEBUG
#Archivo de bloqueo para kareld
LOCKFILE = '/tmp/kareld.lock'

#Cosas relativas el envío de correos
EMAIL_SUBJECT_PREFIX = '[Karelapan] '
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-7a0sv5o4k3w2n67ffh4t0wtmf92if6k2'
MAILGUN_SERVER_NAME = 'karelapan.com'
SERVER_EMAIL = 'soporte@karelapan.com'

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'relative_urls': False
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "sekizai.context_processors.sekizai",
    "apps.sitio.processors.settings_processor",
    "apps.sitio.processors.path_processor",
    "apps.sitio.processors.avisos_processor",
    "apps.sitio.processors.concursos_processor",
)
OLIMPIADA_ACTUAL = 2015
