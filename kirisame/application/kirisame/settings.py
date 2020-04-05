import os

from kombu import Exchange, Queue
from celery.schedules import crontab


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = False if os.environ.get('DJANGO_DEBUG') == 'False' else True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'kirisame.apps.KirisameConfig',
    'django_celery_beat',
    'django_celery_results',
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

ROOT_URLCONF = '{}.urls'.format(os.environ.get('PROJECT_NAME'))

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

WSGI_APPLICATION = '{}.wsgi.application'.format(os.environ.get('PROJECT_NAME'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'redis://{BROKER_HOST}:{BROKER_PORT}/{BROKER_QUEUE}'.format(**os.environ)

CELERY_TASK_QUEUES = (
    Queue('default',  Exchange('default'), routing_key='default'),
    Queue('downloads',  Exchange('downloads'), routing_key='downloads'),
)
CELERY_TASK_ROUTES = {
    'kirisame.tasks.media.download_media': {'queue': 'downloads'},
}
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'

CELERY_BEAT_SCHEDULE = {
    'parse-ranking-day': {
        'task': 'kirisame.tasks.ranking.parse_ranking',
        'schedule': crontab(minute='10', hour='*/4'),
        'kwargs': {'mode': 'day'},
    },
    'parse-ranking-week': {
        'task': 'kirisame.tasks.ranking.parse_ranking',
        'schedule': crontab(minute='20', hour='*/4'),
        'kwargs': {'mode': 'week'},
    },
    'parse-ranking-month': {
        'task': 'kirisame.tasks.ranking.parse_ranking',
        'schedule': crontab(minute='30', hour='*/4'),
        'kwargs': {'mode': 'month'},
    },
    'generate-timetable': {
        'task': 'kirisame.tasks.timetable.generate_timetable',
        'schedule': crontab(minute='0', hour='0'),
        'kwargs': {'count': 48, 'period': 24, 'mode': 'ranking', 'bot': 'artworkkun'},
    },
    'remove-old-toots': {
        'task': 'kirisame.tasks.timetable.remove_old_toots',
        'schedule': crontab(minute='0', hour='0'),
    },
}
