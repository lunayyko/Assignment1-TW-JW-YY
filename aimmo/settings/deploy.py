from .base   import *

ALLOWED_HOSTS = ['*']

SECRET_KEY = get_env_variable('DJANGO_SECRECT_KEY')
ALGORITHM = 'HS256'
DEBUG      = False

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