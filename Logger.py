from abc import ABCMeta, abstractmethod
from ILogger import ILogger
import logging
import datetime
class Logger(ILogger):

    def __init__(self):
        self.logger = logging.getLogger()
        LOG_FILENAME = "log-" + str(datetime.date.today()) + ".txt"
        logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format=format('%(levelname)s %(asctime)s %(message)s'))
        self.logger.info("service started")

    def returnLogFile(self):
        return ("log-" + str(datetime.date.today()) + ".txt")

    def log_error(self, text):
        self.logger.error(text)

    def log_operation(self, text):
        self.logger.info(text)

    def log_debug(self, text):
        self.logger.debug(text)

    def __del__(self):
        self.logger.info("service ended\n")