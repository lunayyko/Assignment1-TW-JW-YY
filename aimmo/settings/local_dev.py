from .base   import *

ALLOWED_HOSTS = ['*']


SECRET_KEY = get_env_variable('DJANGO_SECRECT_KEY')
ALGORITHM = 'hs265'
DEBUG      = True

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': get_env_variable('DB_NAME'),
        'CLIENT': {
            'host': get_env_variable('DB_HOST'),
            'port': int(get_env_variable('DB_PORT')),
        }
    },
}

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'djongo': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,                        
        },
    },
}