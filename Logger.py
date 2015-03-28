from abc import ABCMeta, abstractmethod
from ILogger import ILogger
import logging
import datetime
class Logger(ILogger):

    def __init__(self):
        self.logger = logging.getLogger()
        self.FILENAME = "log-" + str(datetime.date.today()) + ".txt"
        logging.basicConfig(filename=self.FILENAME, level=logging.INFO, format=format('%(levelname)s %(asctime)s %(message)s'))

    def getPath(self):
        return self.FILENAME

    def empty(self):
        with open(self.FILENAME, 'w') as logFile:
            pass

    def log_error(self, text):
        self.logger.error(text)

    def log_operation(self, text):
        self.logger.info(text)

    def log_debug(self, text):
        self.logger.debug(text)