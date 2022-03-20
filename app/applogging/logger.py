from dataclasses import asdict
from logging import config as loggingconfig
from config.config_class import ConfigLogging


default_config = {
    'version': 1,
    'root': {'level': 'NOTSET', 'handlers': ['filehandler']},
    'loggers': {
        'app': {'level': 'NOTSET', 'handlers': ['stdiohandler'], 'qualname': 'app'}
    },
    'handlers': {
        'stdiohandler': {'class': 'logging.StreamHandler', 'level': 'NOTSET', 'formatter': 'basic', 'stream': 'ext://sys.stdout'},
        'filehandler': {'class': 'logging.handlers.RotatingFileHandler', 'level': 'NOTSET', 'formatter': 'detail', 'filename': 'app.log', 'encoding': 'utf-8', 'maxBytes': 5242880, 'backupCount': 0}
    },
    'formatters': {
        'detail': {'class': 'logging.Formatter', 'format': '%(asctime)s\t%(levelno)s\t%(levelname)s\t%(name)s\t%(pathname)s\t%(module)s:%(lineno)d\t%(message)s', 'datefmt': '%Y/%m/%d %H:%M:%S'},
        'basic': {'format': '[%(levelname)s] %(message)s'}
    }
}


def default_logger_config() -> None:
    loggingconfig.dictConfig(default_config)


def set_logger_config(config: ConfigLogging) -> None:
    loggingconfig.dictConfig(asdict(config))
