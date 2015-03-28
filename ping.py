import pycurl
import cStringIO
from Config import Config
import time
from Logger import Logger

class Ping:
    def __init__(self, logger):
        self.logger = logger

    def ping(self):
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        # c.setopt(c.POST, 1)
        # c.setopt(c.URL, "http://localhost:9000/api/records/getlog")
        # c.setopt(c.HTTPHEADER, ['Content-Type: multipart/form-data'])
        # c.setopt(c.HTTPPOST, [('file', (c.FORM_FILE, self.logger.getPath()))])
        # c.setopt(c.VERBOSE, 1)
        c.setopt(c.HTTPHEADER, ['Content-Type: multipart/form-data'])
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.setopt(c.FAILONERROR, True)
        c.setopt(c.URL, 'http://127.0.0.1:9000/api/records/getlog')
        c.setopt(c.HTTPPOST,[ ("fieldname1", "value1"), ("fieldname2", "value2"), ("uploadfieldname", (c.FORM_FILE, self.logger.FILENAME))])
        c.setopt(c.VERBOSE, 1)
        print self.logger.FILENAME
        try:
            c.perform()
        except pycurl.error, msg:
            self.logger.log_error(msg)
        finally:
            c.close()


pingModule = Ping(Logger())
pingModule.ping()