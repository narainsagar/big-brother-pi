from FingParser import FingParser
from FingShellHandler import FingShellHandler
from SQLiteHelper import SQLiteHelper
from Base import Node, NODE_STATUS
from CURLMessage import CURLMessage
from CURLMessageFactory import CURLMessageFactory
from MessageDispatcher import MessageDispatcher
from ServiceExceptions import DispatcherFailed, ParserFailed, DBOpFailed
import logging
from Logger import Logger

class Main:
    def __init__(self, shellHandler, parser, dbHelper, logger):
        self.shellHandler = shellHandler
        self.parser = parser
        self.dbHelper = dbHelper
        self.dbHelper.init(1)
        self.logger = logger

    def startService(self):
        self.logger.log_debug("===================================  Service Started  ===================================")
        shellLog = self.shellHandler.execute()
        if shellLog != None:

            currActiveNodes = []
            prevActiveNodes = []

            try:
                currActiveNodes = self.parser.parse(shellLog)
                self.logger.log_operation("Successfully Parsed Shell Log",)
            except ParserFailed, msg:
                self.logger.log_error(msg)

            try:
                prevActiveNodes = self.dbHelper.getActiveNodes()
                self.logger.log_operation("Successfully got Previous Active Nodes")
            except DBOpFailed, msg:
                self.logger.log_error(msg)

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
                self.logger.log_operation("DB Helper Getting Previous Message")
            except DBOpFailed, msg:
                self.logger.log_error(msg)

            msgList = msgList + prevMessages

            if msgList.__len__() > 0:
                curlMsg = msgFactory.createNodeMsgFromMultipleMsgs(msgList)

                try:
                    msgDispatcher.dispatch(curlMsg)
                    self.logger.log_operation("Message is being Dispatched")
                except DispatcherFailed, msg:
                    self.logger.log_error(str(msg))
                    failedMsgs = msgList

            if failedMsgs.__len__() > 0:
                try:
                    self.dbHelper.saveMessages(failedMsgs)
                except DBOpFailed, msg:
                    self.logger.log_error(msg)
            else:
                self.logger.log_operation("All messages dispatched successfully!")

            try:
                self.dbHelper.saveActiveNodes(currActiveNodes)
                self.logger.log_operation("Successfully Saved Active Nodes")
            except DBOpFailed, msg:
                self.logger.log_error(msg)
            self.logger.log_debug("===================================  Service Ended  ===================================")
        else:
            self.logger.log_error("shell execution failed!")


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


main = Main(FingShellHandler(), FingParser(), SQLiteHelper(), Logger())
main.startService()
