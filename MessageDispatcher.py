from CURLMessage import CURLMessage
from ServiceExceptions import DispatcherFailed
import pycurl
import cStringIO
from Config import Config
import time


class MessageDispatcher:
    def dispatch(self, curlMsg):
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.setopt(c.URL, curlMsg.getPath())
        c.setopt(c.POSTFIELDS, 'data='+curlMsg.getBody())
        #c.setopt(c.VERBOSE, True)
        c.setopt(c.FAILONERROR, True)

        try:
            c.perform()
        except pycurl.error, msg:
            raise DispatcherFailed(msg)
        finally:
            print buf.getvalue() #TODO: log value in buffer

    def dispatchMulti(self, curlMsgList):
        buf = cStringIO.StringIO()
        mc = pycurl.CurlMulti()
        for msg in curlMsgList:
            c = pycurl.Curl()
            c.setopt(c.WRITEFUNCTION, buf.write)
            c.setopt(c.URL, msg.getPath())
            c.setopt(c.POSTFIELDS, 'data='+msg.getBody())
            c.setopt(c.FAILONERROR, True)
            mc.add_handle(c)

        #TODO: implement rest of the function

    def sendCurlFileRequest(self, fileName):
        url = Config.serverAddress
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.POST, 1)
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, ['Content-Type: multipart/form-data'])
        c.setopt(c.HTTPPOST, [('file', (c.FORM_FILE, fileName)), ('created',(str(time.time()))), ('type',('log'))])
        c.setopt(c.VERBOSE, 1)
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.perform()
        c.close()