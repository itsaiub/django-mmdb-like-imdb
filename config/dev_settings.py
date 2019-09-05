import os
from config.common_settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEBUG = True
SECRET_KEY = 'jt!w#h^cb6_+9rwr*^ikbb0=stl8kvg(l1$*uzp2iejb5m+=&v'

INSTALLED_APPS += [
    'debug_toolbar',
]

# Django Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


CASHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-locmemcache',
        'TIMEOUT': 5,  # 5 seconds
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')
