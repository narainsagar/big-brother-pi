from abc import ABCMeta, abstractmethod
from ILogger import ILogger
import inspect,logging
import datetime
class Logger(ILogger):
    def log_error(self, Text):
        fileName = inspect.currentframe().f_back.f_code.co_filename
        lineNo = inspect.currentframe().f_back.f_lineno

        func = inspect.currentframe().f_back.f_code
        Text = "[ERROR]  "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" : "+fileName+" - "+str(lineNo)+" - "+Text
        Text = Text.upper()
        today = 'log_file-' + str(datetime.date.today()) +'.txt'
        LOG_FILENAME = (today)
        logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.ERROR,
                            format=format('%(message)s'),
                            )
        logging.error(Text)

    def log_operation(self, Text):
        fileName = inspect.currentframe().f_back.f_code.co_filename
        lineNo = inspect.currentframe().f_back.f_lineno
        Text = "[INFO]  "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" : "+fileName+" - "+str(lineNo)+" - "+Text
        today = 'log_file-' + str(datetime.date.today()) +'.txt'
        LOG_FILENAME = (today)
        logging.Formatter('%(asctime)s %(message)s')
        logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.INFO,
                            )
        logging.info(Text)
    def log_debug(self, Text):
        today = 'log_file-' + str(datetime.date.today()) +'.txt'
        LOG_FILENAME = (today)
        logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.DEBUG,
                            format=format('%(message)s'),
                            )
        logging.debug(Text)