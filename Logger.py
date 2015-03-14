from abc import ABCMeta, abstractmethod
from ILogger import ILogger
import logging
import datetime
class Logger(ILogger):
    def log_error(self):
        today = 'error_logging.out-' + str(datetime.date.today()) +'.txt'
        LOG_FILENAME = (today)
        logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.ERROR,
                            )
        return LOG_FILENAME