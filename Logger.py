from abc import ABCMeta, abstractmethod
from ILogger import ILogger
import logging
import datetime
class Logger(ILogger):
    def log_error(self, Text):
        Text = "============================= ERROR =============================\n    "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" : "+Text+"\n================================================================"
        Text = Text.upper()
        today = 'log_file-' + str(datetime.date.today()) +'.txt'
        LOG_FILENAME = (today)
        logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.ERROR,
                            format=format('%(message)s'),
                            )
        logging.error(Text)
    def log_operation(self, Text):
        Text = "============================= INFO =============================\n    "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" : "+Text+"\n================================================================"
        today = 'log_file-' + str(datetime.date.today()) +'.txt'
        LOG_FILENAME = (today)
        logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.INFO,
                            format=format('%(message)s'),
                            )
        logging.info(Text)