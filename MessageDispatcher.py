from CURLMessage import CURLMessage
import pycurl
import cStringIO

class MessageDispatcher:
    def dispatch(self, curlMsg):
        buf = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.WRITEFUNCTION, buf.write)
        c.setopt(c.URL, curlMsg.getPath())
        c.setopt(c.POSTFIELDS, 'data='+curlMsg.getBody())
        c.setopt(c.VERBOSE, True)
        c.setopt(c.FAILONERROR, True)

        try:
            c.perform()
        except pycurl.error, msg:
            print msg #TODO: log error
        finally:
            print buf.getvalue() #TODO: log value in buffer

