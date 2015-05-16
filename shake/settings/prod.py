# -*- coding: utf-8 -*-
from .common import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ['*']  # 보안을 위해, 서비스 도메인을 직접 지정해주는 것이 좋다.


'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MEDIA_URL = ''  # Amazon S3 등을 통해, 서빙할 경우 hostname 까지 지정이 필요하다.
STATIC_URL = ''

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = BROKER_URL
'''

