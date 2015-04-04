from abc import ABCMeta, abstractmethod
from ILogger import ILogger
import logging
import datetime
class Logger(ILogger):

    #sets the logger configurations
    def __init__(self):
        self.logger = logging.getLogger()
        self.FILENAME = "log-" + str(datetime.date.today()) + ".txt"
        logging.basicConfig(filename=self.FILENAME, level=logging.DEBUG, format=format('%(process)d %(levelname)s %(asctime)s %(message)s'))
    #return the
    def getPath(self):
        return self.FILENAME
    #empties the log file
    def empty(self):
        with open(self.FILENAME, 'w') as logFile:
            pass
    #log errors on log file
    def log_error(self, text):
        self.logger.error(text)
    #logs operations in log file
    def log_operation(self, text):
        self.logger.info(text)
    #logs debug messages in log file
    def log_debug(self, text):
        self.logger.debug(text)