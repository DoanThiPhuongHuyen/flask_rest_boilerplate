import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True, verbose=True)

DEBUG = (os.environ.get('DEBUG', 'False') == 'True')

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s | %(levelname)s | %(process)d | %(thread)d | %(filename)s:%('
                      'lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s | %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'daily_http': {
            'level': 'INFO',
            'class': 'app.core.logging_handlers.PythonHTTPHandler',
            'url': 'http-daily-logger/',
            'formatter': 'verbose',
            'host': os.environ.get('LOGGING_DAILY_HTTP_HOST', '127.0.0.1:1234'),
            'method': 'POST',
            'logPath': os.environ.get('LOGGING_DAILY_HTTP_FILE_PATH',
                                      '/var/log/order-processing-backend/daily.log'),
        },
        # 'slack_notification': {
        #     'level': os.environ.get('SLACK_NOTIFICATION_LEVEL', 'ERROR'),
        #     'class': 'app.core.logging_handlers.LogSlackHandler',
        #     'formatter': 'simple',
        #     'webhook': os.environ.get('SLACK_NOTIFICATION_WEBHOOK',
        #                               'https://hooks.slack.com/services/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'),
        #     'sender': os.environ.get('SLACK_NOTIFICATION_SENDER', '[ORDER PROCESSING][Prod]'),
        #     'channel': os.environ.get('SLACK_NOTIFICATION_CHANNEL', '#order-processing'),
        # },
    },
    'loggers': {
        'main': {
            'level': 'INFO',
            'handlers': os.environ.get('LOGGER_MAIN_HANDLERS', 'console').split(','),
            'propagate': True,
        },
    },
}

TIME_ZONE = 'Asia/Ho_Chi_Minh'

DATABASES = {
    'default': {
        'ENGINE': 'core.db.backends.mysql.MySQLDB',
        'NAME': os.environ.get('DB_NAME', 'is_asia'),
        'USERNAME': os.environ.get('DB_USERNAME', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'mysql'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'ENGINE_OPTIONS': {
            'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', '3600')),
        },
    },
}

REDIS = {
    'default': {
        'HOST': os.getenv('REDIS_HOST'),
        'PORT': os.getenv('REDIS_PORT'),
        'DB': os.getenv('REDIS_DB')
    }
}

AMQP_CONFIG = {
    'default': {
        'HOST': os.environ.get('AMQP_DEFAULT_HOST', 'localhost'),
        'PORT': os.environ.get('AMQP_DEFAULT_PORT', 5672),
        'VHOST': os.environ.get('AMQP_DEFAULT_VHOST', 'localhost'),
        'USER': os.environ.get('AMQP_DEFAULT_USERNAME', 'rabbitmq'),
        'PASSWORD': os.environ.get('AMQP_DEFAULT_PASSWORD', 'rabbitmq'),
    },
}
