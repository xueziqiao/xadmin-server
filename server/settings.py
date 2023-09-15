"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mlq6(#a^2vk!1=7=xhp#$i=o5d%namfs=+b26$m#sh_2rco7j^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'daphne',  # 支持websocket
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common.apps.CommonConfig',
    'system.apps.SystemConfig',
    'message.apps.MessageConfig',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'captcha',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.core.middleware.ApiLoggingMiddleware'
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

# WSGI_APPLICATION = 'server.wsgi.application'
ASGI_APPLICATION = "server.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

REDIS_PASSWORD = "nineven"
REDIS_HOST = "redis"
REDIS_PORT = 6379
DEFAULT_CACHE_ID = 1
CHANNEL_LAYERS_CACHE_ID = 2
CELERY_BROKER_CACHE_ID = 3
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{DEFAULT_CACHE_ID}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 8000},
            "PASSWORD": REDIS_PASSWORD,
            "DECODE_RESPONSES": True
        },
        "TIMEOUT": 60 * 15,
        "KEY_FUNCTION": "common.base.utils.redis_key_func",
        "REVERSE_KEY_FUNCTION": "common.base.utils.redis_reverse_key_func",
    },
}

# create database server default character set utf8 COLLATE utf8_general_ci;
# grant all on server.* to server@'127.0.0.1' identified by 'KGzKjZpWBp4R4RSa';
# python manage.py makemigrations
# python manage.py migrate
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'server',
    #     'USER': 'server',
    #     'PASSWORD': 'KGzKjZpWBp4R4RSa',
    #     'HOST': 'mariadb',
    #     'PORT': 3306,
    #     'CONN_MAX_AGE': 600,
    #     # 设置MySQL的驱动
    #     # 'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
    #     'OPTIONS': {'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"', 'charset': 'utf8mb4'}
    # },
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CHANNEL_LAYERS = {
    "default": {
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts": [f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{CHANNEL_LAYERS_CACHE_ID}"],
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "system.UserInfo"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Media配置
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "upload")

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'common.core.auth.CookieJWTAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'EXCEPTION_HANDLER': 'common.core.exception.common_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {  # {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        'anon': '60/m',
        'user': '600/m',
        'upload': '100/m',
        'download1': '10/m',
        'download2': '100/h',
        'register': '10/d',
    },
    'DEFAULT_PAGINATION_CLASS': 'common.core.pagination.PageNumber',
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        'common.core.permission.IsAuthenticated',
    ],
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # ),
}

# DRF扩展缓存时间
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 3600,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=3600),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,  # 在登录的时候更新user表  last_login 字段

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': 'x',
    'ISSUER': 'server',
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('common.core.auth.ServerAccessToken',),
    # 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-token"
)

BASE_LOG_DIR = os.path.join(BASE_DIR, "logs", "api")
TMP_LOG_DIR = os.path.join(BASE_DIR, "logs", "tmp")
CELERY_LOG_DIR = os.path.join(BASE_DIR, "logs", "task")
if not os.path.isdir(BASE_LOG_DIR):
    os.makedirs(BASE_LOG_DIR)
if not os.path.isdir(TMP_LOG_DIR):
    os.makedirs(TMP_LOG_DIR)
if not os.path.isdir(CELERY_LOG_DIR):
    os.makedirs(CELERY_LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(filename)s:%(funcName)s:%(lineno)d %(levelname)s] %(asctime)s %(process)d %(thread)d %(message)s'
        },
        'main': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(filename)s:%(funcName)s:%(lineno)d %(levelname)s] %(message)s',
        },
        'exception': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '\n%(asctime)s [%(levelname)s] %(message)s',
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(funcName)s:%(lineno)d]%(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'main'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，根据时间自动切
            'filename': os.path.join(BASE_LOG_DIR, "debug.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 100,  # 日志大小 100M
            'backupCount': 10,  # 备份数为3
            # 'when': 'W6',  # 每天一切， 可选值有S/秒 M/分 H/小时 D/天 W0-W6/周(0=周一) midnight/如果没指定时间就默认在午夜
            'formatter': 'main',
            'encoding': 'utf-8',
        },
        'drf_exception': {
            'encoding': 'utf8',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'exception',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 7,
            'filename': os.path.join(BASE_LOG_DIR, "drf_exception.log"),
        },
        'unexpected_exception': {
            'encoding': 'utf8',
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'exception',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 7,
            'filename': os.path.join(BASE_LOG_DIR, "unexpected_exception.log"),
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "sql.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {  # 默认的logger应用如下配置
            'handlers': ['file', 'console', 'drf_exception', 'unexpected_exception'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'sql'],
            'propagate': True,
            'level': 'INFO',
        },
        'drf_exception': {
            'handlers': ['console', 'drf_exception'],
            'level': 'INFO',
        },
        'unexpected_exception': {
            'handlers': ['unexpected_exception'],
            'level': 'INFO',
        },
    },
}

CACHE_KEY_TEMPLATE = {
    'pending_state_key': 'pending_state',
    'make_token_key': 'make_token',
    'download_url_key': 'download_url',
    'upload_part_info_key': 'upload_part_info',
    'black_access_token_key': 'black_access_token',
}

# Celery Configuration Options
# https://docs.celeryq.dev/en/stable/userguide/configuration.html?
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# CELERY_RESULT_BACKEND = ''
# CELERY_CACHE_BACKEND = 'django-cache'

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'

# broker redis
DJANGO_DEFAULT_CACHES = CACHES['default']
CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{CELERY_BROKER_CACHE_ID}'

# CELERY_WORKER_CONCURRENCY = 10  # worker并发数
CELERY_WORKER_AUTOSCALE = [10, 3]  # which needs two numbers: the maximum and minimum number of pool processes

CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死
CELERY_RESULT_EXPIRES = 3600 * 24 * 7  # 任务结果过期时间

CELERY_WORKER_DISABLE_RATE_LIMITS = True  # 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
CELERY_WORKER_PREFETCH_MULTIPLIER = 60  # celery worker 每次去redis取任务的数量

CELERY_WORKER_MAX_TASKS_PER_CHILD = 200  # 每个worker执行了多少任务就会死掉，我建议数量可以大一些，比如200

CELERY_ENABLE_UTC = False
DJANGO_CELERY_BEAT_TZ_AWARE = True

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# celery消息的序列化方式，由于要把对象当做参数所以使用pickle
# CELERY_RESULT_SERIALIZER = 'pickle'
# CELERY_ACCEPT_CONTENT = ['pickle']
# CELERY_TASK_SERIALIZER = 'pickle'

CELERY_BEAT_SCHEDULE = {
    'auto_clean_operation_job': {
        'task': 'system.tasks.auto_clean_operation_job',
        'schedule': crontab(hour='2', minute='2'),
        'args': ()
    },
    'auto_clean_expired_captcha_job': {
        'task': 'system.tasks.auto_clean_expired_captcha_job',
        'schedule': crontab(hour='2', minute='12'),
        'args': ()
    },
    'auto_clean_black_token_job': {
        'task': 'system.tasks.auto_clean_black_token_job',
        'schedule': crontab(hour='2', minute='22'),
        'args': ()
    },
    'auto_clean_tmp_file_job': {
        'task': 'system.tasks.auto_clean_tmp_file_job',
        'schedule': crontab(hour='2', minute='32'),
        'args': ()
    }
}

# 字母验证码
CAPTCHA_IMAGE_SIZE = (120, 40)  # 设置 captcha 图片大小
CAPTCHA_LENGTH = 6  # 字符个数
CAPTCHA_TIMEOUT = 1  # 超时(minutes)

# 加减乘除验证码
CAPTCHA_OUTPUT_FORMAT = '%(image)s %(text_field)s %(hidden_field)s '
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null',
                           'captcha.helpers.noise_arcs',  # 线
                           'captcha.helpers.noise_dots',  # 点
                           )
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

APPEND_SLASH = False

HTTP_BIND_HOST = '0.0.0.0'
HTTP_LISTEN_PORT = 8896
# celery flower 任务监控配置
CELERY_FLOWER_PORT = 5566
CELERY_FLOWER_HOST = '127.0.0.1'
CELERY_FLOWER_AUTH = 'flower:flower123.'
PERMISSION_WHITE_URL = [
    "^/api/system/login$",
    "^/api/system/userinfo/self$",
    "^/api/system/notice/unread$",
    "^/api/system/routes$",
]

PERMISSION_SHOW_PREFIX = [
    'api/system',
    'api/flower',
]

API_LOG_ENABLE = locals().get("API_LOG_ENABLE", True)
API_LOG_METHODS = locals().get("API_LOG_METHODS", ["POST", "DELETE", "PUT"])  # 'ALL'

# 在操作日志中详细记录的请求模块映射
API_MODEL_MAP = locals().get("API_MODEL_MAP", {
    "/api/system/refresh": "Token刷新",
    "/api/system/upload": "文件上传",
    "/api/system/login": "用户登录",
    "/api/system/logout": "用户登出",
    "/api/flower": "定时任务",
})
