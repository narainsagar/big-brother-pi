from CURLMessage import CURLMessage
from Base import Node
import json
import time
from Config import Config

class CURLMessageFactory:
    #creates a single node message
    def createNodeMsg(self, nodeList):
        curlMsg = CURLMessage()
        curlMsg.setHeaders(['Content-Type: application/json'])
        curlMsg.setPath(Config.NODE_ADDR)
        nodeDict = []
        for node in nodeList:
            nodeDict.append(node.__dict__)
        JSONDict = {'created': str(time.time()), 'type': 'node', 'company_id': Config.COMPANY_ID, 'nodes': nodeDict}
        curlMsg.setBody(json.dumps(JSONDict))
        return curlMsg
    #merges all node messgaes to a single node message
    def createNodeMsgFromMultipleMsgs(self, msgList):
        curlMsg = CURLMessage()
        curlMsg.setHeaders(['Content-Type: application/json'])
        curlMsg.setPath(Config.NODE_ADDR)
        msgBodyList = []
        for msg in msgList:
            msgBodyList.append(msg.getBody())
        curlMsg.setBody("[" + ", ".join(msgBodyList) + "]")
        return curlMsg
