import logging
from pathlib import Path

string_path = "log\outputlog\logger.log"
path_file = Path(string_path)

logging_config = dict(
    version=1,
    formatters={
        'simple': {'format':'%(levelname)s %(asctime)s { module name : %(module)s Line no : %(lineno)d} %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.handlers.RotatingFileHandler',
              'filename': path_file,
              'maxBytes': 1024 * 1024 * 5,
              'backupCount': 5,
              'level': 'DEBUG',
              'formatter': 'simple',
              'encoding': 'utf8'}
    },

    root={
        'handlers': ['h'],
        'level': logging.DEBUG,
    },
)