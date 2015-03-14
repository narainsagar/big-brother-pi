from CURLMessage import CURLMessage
from Base import Node
import json
import time

class CURLMessageFactory:
    def createNodeMsg(self, node):
        curlMsg = CURLMessage()
        curlMsg.setHeaders(['Content-Type: application/json'])
        curlMsg.setPath('http://localhost:8888/pistuff/')
        msgDict = node.__dict__
        msgDict['created'] = curlMsg.getCreated()
        msgDict['type'] = 'node'
        curlMsg.setBody(json.dumps(msgDict))
        return curlMsg