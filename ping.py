import pycurl
import cStringIO
from Config import Config
import time
from Logger import Logger
from Constants import Constants

class Ping:
    def __init__(self, logger):
        self.logger = logger

    #sends the log file to server and clears the log file
    def ping(self):
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.HTTPHEADER, ['Content-Type: multipart/form-data'])
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.setopt(c.FAILONERROR, True)
        c.setopt(c.URL, Config.LOG_ADDR)
        c.setopt(c.HTTPPOST,[ ("log", (c.FORM_FILE, self.logger.getPath())), ("company_id", Config.COMPANY_ID) ])
        c.setopt(c.VERBOSE, 1)
        try:
            c.perform()
        except pycurl.error, msg:
            self.logger.log_error(msg + "\n")
        else:
            self.logger.empty()
        finally:
            c.close()


pingModule = Ping(Logger())
pingModule.ping()