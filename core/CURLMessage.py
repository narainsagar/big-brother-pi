import time

class CURLMessage:
    __headers = {}
    __body = ""
    __url = ""

    def setHeaders(self, dict):
        self.__headers = dict

    def getHeaders(self):
        return self.__headers

    def setBody(self, body):
        self.__body = body

    def getBody(self):
        return self.__body

    def setPath(self, url):
        self.__url = url

    def getPath(self):
        return self.__url
