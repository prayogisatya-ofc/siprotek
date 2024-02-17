import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_HOSTS = ['']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'), 
        'PASSWORD': os.getenv('DB_PASS'),
        'PORT': 3306,
        'HOST': 'localhost',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}

STATIC_ROOT = "/home/username/direktoi-domain/static/"
MEDIA_ROOT = "/home/username/direktoi-domain/media/"

CSRF_TRUSTED_ORIGINS = ['']