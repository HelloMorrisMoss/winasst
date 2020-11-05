import logging
from logging.config import dictConfig


# configure the logger
logging_config = dict(
    version=1,
    formatters={
        'f': {'format':
                  '%(asctime)s %(module)s>%(funcName)s>%(lineno)-4d %(levelname)s: %(message)s'}

    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG},
        'debug_rotating_file_handler': {
            'level': 'DEBUG',
            'formatter': 'f',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'debug.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10}
    },
    root={
        'handlers': ['h', 'debug_rotating_file_handler'],
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