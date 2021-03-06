"""
Django settings for build project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import platform
import time
from appack.helper.misc import *
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appack',
    'api',
    'proxy',
    'checkout',
    'gunicorn',
    'dpi',
    'strategy',
    'dataplatform',
]
DEBUG = False
DATABASES = {

        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'build',
            'HOST': '127.0.0.1',
            'USER': '*',
            'PASSWORD': '*',
            'PORT': '3306',
        }
}

if 'Linux' not in platform.system():
    DEBUG = True
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'appack',
        'proxy',
        'api',
        'checkout',
        'dpi',
        'strategy',
        'sow',
        'dataplatform',

    ]
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'build',
            'HOST': '*',
            'USER': '*',
            'PASSWORD': '*',
            'PORT': '3306',
        }
    }


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''
SIGN_KEY = ''
# APPEND_SLASH=False
# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['build.superhcloud.com','127.0.0.1]

# Application definition


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'build.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'build.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

import pymysql         # 一定要添加这两行！通过pip install pymysql！
pymysql.install_as_MySQLdb()



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), '..', 'static').replace('\\','/'),
    os.path.join('static'),
)
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR,'../static'))

USERS_REGISTRATION_OPEN = True

USERS_VERIFY_EMAIL = True

USERS_AUTO_LOGIN_ON_ACTIVATION = True

USERS_EMAIL_CONFIRMATION_TIMEOUT_DAYS = 3

# Specifies minimum length for passwords:
USERS_PASSWORD_MIN_LENGTH = 5

# Specifies maximum length for passwords:
USERS_PASSWORD_MAX_LENGTH = None

# the complexity validator, checks the password strength
USERS_CHECK_PASSWORD_COMPLEXITY = True

USERS_SPAM_PROTECTION = False  # important!

#  ---------------------------------------------------------
#  Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.263.net'
EMAIL_PORT = 25
EMAIL_HOST_USER = '*'
EMAIL_HOST_PASSWORD = '*'
EMAIL_FROM = '报警邮件'
#  ---------------------------------------------------------

CACHES = {
    'default': {
        'BACKEND': 'django.contrib.sessions.backends.cached_db',
    }
}
# 阻止javascript对会话数据的访问，提高安全性。
SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

from datetime import datetime
# now = datetime.now().strftime('%Y%m%d%H%M%S')
now = datetime.now().strftime('%Y%m%d')
base = '/Users/code/log'
if 'Linux' in platform.system():
    base = '/home/log/'
file_name = base+'public.log'
file_name_new = '{}public_{}.log'.format(base,getDatetimeYesterday())

# 如果存在，则改成在名字后面加上昨天的日志，并新建一个文件
if is_have_file(file_name) and not is_have_file(file_name_new):
    cp(file_name,file_name_new)
    cmd = 'cat /dev/null>{}'.format(file_name)
    executionShell(cmd,cwd=base)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)-8s %(filename)s %(funcName)s[line:%(lineno)d] %(message)s'
        },
        'detail': {
            'format': '%(asctime)s %(levelname)-8s %(pathname)s %(funcName)s[line:%(lineno)d] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_name,
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 100,
            'formatter': 'detail',
        },
        'public': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_name,
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 100,
            'formatter': 'detail',
        },
        'api': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_name,
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 100,
            'formatter': 'detail',
        },'appack': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_name,
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 100,
            'formatter': 'detail',
        },
        'proxy': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_name,
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 100,
            'formatter': 'detail',
        },
        'checkout': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_name,
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 100,
            'formatter': 'detail',
        },
        'dpi': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_name,
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 100,
            'formatter': 'detail',
        },
        'strategy': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_name,
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 100,
            'formatter': 'detail',
        },
        'dataplatform': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': file_name,
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 100,
            'formatter': 'detail',
        },

    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO', # 这里配置django本身日志等级
            'propagate': True,
        },
        # 自定义模块日志
        'django.template': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
        'public': {
            'handlers': ['console', 'public'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'api': {
                'handlers': ['console', 'api'],
                'level': 'DEBUG',
                'propagate': True,
        },'appack': {
                'handlers': ['console', 'appack'],
                'level': 'DEBUG',
                'propagate': True,
        },
        'proxy': {
                'handlers': ['console', 'proxy'],
                'level': 'DEBUG',
                'propagate': True,
        },
        'checkout': {
                'handlers': ['console', 'checkout'],
			    'level': 'DEBUG',
                'propagate': True,
        },
        'dpi': {
                'handlers': ['console', 'dpi'],
                'level': 'DEBUG',
                'propagate': True,
        },
        'strategy': {
                'handlers': ['console', 'strategy'],
                'level': 'DEBUG',
                'propagate': True,
        },
        'dataplatform': {
                'handlers': ['console', 'dataplatform'],
                'level': 'DEBUG',
                'propagate': True,
        },

    },
}