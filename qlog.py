import logging
from logging.config import dictConfig


# configure the logger
logging_config = dict(
    version=1,
    formatters={
                'console_format': {'format':
                                   '%(asctime)s %(module)s.%(funcName)s.%(lineno)-4d %(levelname)s: %(message)s'},
                'log_file_format': {'format':
                                    '"%(asctime)s","%(module)s.%(funcName)s.%(lineno)d","%(levelname)s","%(message)s"'}
    },
    handlers={
        'console_log_handler': {'class': 'logging.StreamHandler',
              'formatter': 'console_format',
              'level': logging.DEBUG},
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




# from datetime import datetime
# def qlog(msg):
#     log_here = r"C:\my documents\assistant_log.txt"
#     # print(datetime.now())
#     with open(log_here, 'a') as lf:
#         lf.writelines('{tm} {msg}.\n'.format(tm=datetime.now(), msg=msg))