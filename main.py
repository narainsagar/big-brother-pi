from FingParser import FingParser
from FingShellHandler import FingShellHandler
from SQLiteHelper import SQLiteHelper
from Base import Node, NODE_STATUS
from CURLMessage import CURLMessage
from CURLMessageFactory import CURLMessageFactory
from MessageDispatcher import MessageDispatcher
from ServiceExceptions import DispatcherFailed, ParserFailed, DBOpFailed

class Main:
    def __init__(self, shellHandler, parser, dbHelper):
        self.shellHandler = shellHandler
        self.parser = parser
        self.dbHelper = dbHelper
        self.dbHelper.init(1)

    def startService(self):
        shellLog = self.shellHandler.execute()
        if shellLog != None:

            currActiveNodes = []
            prevActiveNodes = []

            try:
                currActiveNodes = self.parser.parse(shellLog)
            except ParserFailed, msg:
                print msg

            try:
                prevActiveNodes = self.dbHelper.getActiveNodes()
            except DBOpFailed, msg:
                print msg

            nodesDown = self.__getNodesDown(currActiveNodes, prevActiveNodes)
            nodesUp = self.__getNodesUp(currActiveNodes, prevActiveNodes)

            msgFactory = CURLMessageFactory()
            msgDispatcher = MessageDispatcher()

            nodeList = nodesDown + nodesUp

            prevMessages = []
            msgList = []
            failedMsgs = []

            if nodeList.__len__() > 0:
                msgList.append(msgFactory.createNodeMsg(nodeList))

            try:
                prevMessages = self.dbHelper.getMessages()
            except DBOpFailed, msg:
                print msg

            msgList = msgList + prevMessages

            if msgList.__len__() > 0:
                curlMsg = msgFactory.createNodeMsgFromMultipleMsgs(msgList)
                print curlMsg.getBody()
                try:
                    msgDispatcher.dispatch(curlMsg)
                except DispatcherFailed, msg:
                    print msg
                    failedMsgs = msgList

            if failedMsgs.__len__() > 0:
                try:
                    self.dbHelper.saveMessages(failedMsgs)
                except DBOpFailed, msg:
                    print msg
            else:
                print "All messages dispatched successfully!"

            try:
                self.dbHelper.saveActiveNodes(currActiveNodes)
            except DBOpFailed, msg:
                print msg
        else:
            print "shell execution failed!"


    def __getNodesUp(self, currActiveNodes, prevActiveNodes):
        nodesUp = []
        for currNode in currActiveNodes:
            bool = False
            for prevNode in prevActiveNodes:
                if currNode.mac_addr == prevNode.mac_addr:
                    bool = True

            if bool == False:
                currNode.node_status = NODE_STATUS.UP
                nodesUp.append(currNode)

        return nodesUp

    def __getNodesDown(self, currActiveNodes, prevActiveNodes):
        nodesDown = []
        for prevNode in prevActiveNodes:
            bool = False
            for currNode in currActiveNodes:
                if prevNode.mac_addr == currNode.mac_addr:
                    bool = True

            if bool == False:
                prevNode.node_status = NODE_STATUS.DOWN
                nodesDown.append(prevNode)

        return nodesDown


main = Main(FingShellHandler(), FingParser(), SQLiteHelper())
main.startService()
