import logging
from logging.config import dictConfig


class BreadcrumbFilter(logging.Filter):
    """Provides %(breadcrumbs) field for the logger formatter.

    Th breadcrumbs field returns module.funcName.lineno as a single (width controllable)-45s string.
    """
    def filter(self, record):
        record.breadcrumbs = "{}.{}.{}".format(record.module, record.funcName, record.lineno)
        return True

# configure the logger
logging_config = dict(
    version=1,
    filters={
        'column_filter': {
            '()': BreadcrumbFilter
        }
    },
    formatters={
        'console_format': {'format':
                           '%(asctime)-30s %(breadcrumbs)-45s %(levelname)s: %(message)s'},
        'log_file_format': {'format':
                            '"%(asctime)s","%(breadcrumbs)s","%(funcName)s","%(lineno)d","%(levelname)s","%(message)s"'}
    },
    handlers={
        'console_log_handler': {'class': 'logging.StreamHandler',
              'formatter': 'console_format',
              'level': logging.DEBUG,
              'filters': ['column_filter']},
        'rotating_csv_file_log_handler': {
            'level': 'DEBUG',
            'formatter': 'log_file_format',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'debug.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10}
    },
    root={
        'handlers': ['console_log_handler', 'rotating_csv_file_log_handler'],
        'level': logging.DEBUG,
    },

)

dictConfig(logging_config)

lg = logging.getLogger()

# test the logger
if __name__ == '__main__':
    lg.debug('often makes a very good meal of %s', 'visiting tourists')
