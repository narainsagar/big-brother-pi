from CURLMessage import CURLMessage
from ServiceExceptions import DispatcherFailed
import pycurl
import cStringIO

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

