from CURLMessage import CURLMessage
from Base import Node
import json
import time
from Config import Config

class CURLMessageFactory:
    def createNodeMsg(self, nodeList):
        curlMsg = CURLMessage()
        curlMsg.setHeaders(['Content-Type: application/json'])
        curlMsg.setPath(Config.serverAddress)
        nodeDict = []
        for node in nodeList:
            nodeDict.append(node.__dict__)
        JSONDict = {'created': str(time.time()), 'type' : 'node', 'nodes': nodeDict}
        curlMsg.setBody(json.dumps(JSONDict))
        return curlMsg

    def createNodeMsgFromMultipleMsgs(self, msgList):
        curlMsg = CURLMessage()
        curlMsg.setHeaders(['Content-Type: application/json'])
        curlMsg.setPath(Config.serverAddress)
        msgBodyList = []
        for msg in msgList:
            msgBodyList.append(msg.getBody())
        curlMsg.setBody("[" + ", ".join(msgBodyList) + "]")
        return curlMsg
