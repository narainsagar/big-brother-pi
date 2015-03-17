from abc import ABCMeta, abstractmethod
from ILogger import ILogger
import logging
import datetime
class Logger(ILogger):
    def log_error(self, Message):
        today = 'error_logging-' + str(datetime.date.today()) +'.txt'
        LOG_FILENAME = (today)
        logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.ERROR,
                            )
        logging.error(Message)