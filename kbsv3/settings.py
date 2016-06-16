# Django settings for untitled4 untitled4.

import copy
import logging
import os
import os
import sys
from urllib.parse import urlparse

from apps import registration

DEBUG = False


# def _is_secure(self, request):
#     if request.is_secure():
#         return True
#
#     if 'HTTP_X_SSL_PROTOCOL' in request.META:
#         return True
#
#     return False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'kbv3_database',  # Or path to database file if using sqlite3.
        'USER': 'maximus',
        'PASSWORD': 'MAXsky1995',
        'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(PROJECT_DIR)
APPS_DIR = os.path.realpath(os.path.join(ROOT_DIR, 'apps'))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(APPS_DIR)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media/media')
MEDIA_URL = '/site_media/media/'

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = 0
SECURE_CONTENT_TYPE_NOSNIFF = 0
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = False
X_FRAME_OPTIONS = 'DENY'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '104.199.154.36', 'kb.cuscom.xyz', '.kb.cuscom.xyz', 'kb.teledirectasia.com',
                 '.kb.teledirectasia.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Singapore'

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

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'site_media/media'),  # or whatever you named it
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'as-%*_93v=r5*p_7cu8-%o6b&x^g+q$#*e*fl)k)x0-t=%q0qa'

DATABASE_ROUTERS = (
    'tenant_schemas.routers.TenantSyncRouter',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'kbsv3.urls_tenants'
PUBLIC_SCHEMA_URLCONF = 'kbsv3.urls_public'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'kbsv3.wsgi.application'

SHARED_APPS = (
    'tenant_schemas',  # mandatory
    'apps.core.apps.CoreConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise',
)

TENANT_APPS = (
    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.postgres',

    'notifications',
    'django_mptt_admin',
    'mptt',
    'urllib3',
    'attachments',
    'colorfield',
    'django_summernote',
    'apps.poll.apps.PollConfig',
    'apps.registration.apps.RegistrationConfig',
    'apps.article.apps.ArticleConfig',
    'apps.manager.apps.ManagerConfig',
)

TENANT_MODEL = "core.KnowledgeBase"  # app.Model

INSTALLED_APPS = list(set(TENANT_APPS + SHARED_APPS))

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/registration/login/' \
 \
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


# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


def static_url(url):
    return os.path.join(STATIC_URL, url)


SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': False,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': False,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    # (Firefox, Chrome only)
    'styleWithTags': True,
    # Set text direction : 'left to right' is default.
    'direction': 'ltr',

    # Change editor size
    'width': '80%',
    'height': '480',

    # Use proper language setting automatically (default)
    'lang': None,

    # Customize toolbar buttons
    'toolbar': [
        ['save', ['save']],
        ['cleaner', ['cleaner']],
        ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript',
                  'strikethrough', 'clear']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video', 'hr']],
        ['view', ['fullscreen', 'codeview', 'undo', 'redo']],
        ['help', ['help']],
        ['misc', ['print']],
    ],

    # Need authentication while uploading attachments.
    'attachment_require_authentication': True,

    # Set `upload_to` function for attachments.
    # 'attachment_upload_to': my_custom_upload_to_func(),

    # Set custom storage class for attachments.
    # 'attachment_storage_class': 'my.custom.storage.class.name',

    # Set custom model for attachments (default: 'django_summernote.Attachment')
    # 'attachment_model': 'my.custom.attachment.model',   # must inherit 'django_summernote.AbstractAttachment'

    # Set common css/js media files
    'external_css': (
        '//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css',
    ),
    'external_js': (
        '//code.jquery.com/jquery-1.9.1.min.js',
        '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js',

    ),
    'internal_css': (
        static_url('django_summernote/summernote.css'),
    ),
    'internal_js': (
        static_url('django_summernote/jquery.ui.widget.js'),
        static_url('django_summernote/jquery.iframe-transport.js'),
        static_url('django_summernote/jquery.fileupload.js'),
        static_url('django_summernote/summernote.min.js'),
    ),

    # You can add custom css/js for SummernoteWidget.
    'css': (
    ),
    'js': (
    ),

    # And also for SummernoteInplaceWidget.
    # !!! Be sure to put {{ form.media }} in template before initiate summernote.
    'css_for_inplace': (
        static_url('core/css/vendor/font-awesome-4.6.3/css/font-awesome.min.css'),
        static_url('django_summernote/summernote.css'),
        static_url('django_summernote/django_summernote_inplace.css'),
    ),
    'js_for_inplace': (
        static_url('core/js/vendor/bootstrap/bootstrap.min.js'),
        static_url('core/js/vendor/summernote/summernote-ext-print.js'),
        static_url('django_summernote/jquery.ui.widget.js'),
        static_url('django_summernote/jquery.iframe-transport.js'),
        static_url('django_summernote/jquery.fileupload.js'),
        static_url('django_summernote/summernote.min.js'),
    ),

    # You can disable file upload feature.
    'disable_upload': True,
}



