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
from Config import Config
import sys

class Main:
    def __init__(self, shellHandler, parser, dbHelper, logger):
        self.shellHandler = shellHandler
        self.parser = parser
        self.dbHelper = dbHelper
        self.dbHelper.init(1)
        self.logger = logger

    def startService(self):
        self.logger.log_operation("service started");
        shellLog = self.shellHandler.execute()
        if shellLog != None:

            currActiveNodes = []
            prevActiveNodes = []

            try:
                self.logger.log_operation("Parsing fing output")
                currActiveNodes = self.parser.parse(shellLog)
            except ParserFailed, msg:
                self.logger.log_error("service ended with exception: " + msg+"\n")
                sys.exit(1)

            try:
                self.logger.log_operation("fetching previous active nodes from database")
                prevActiveNodes = self.dbHelper.getActiveNodes()
            except DBOpFailed, msg:
                self.logger.log_error("service ended with exception: " + msg+"\n")
                sys.exit(1)

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
                self.logger.log_operation("fetching previous failed messages from database")
                prevMessages = self.dbHelper.getMessages()
            except DBOpFailed, msg:
                self.logger.log_error(msg)

            msgList = msgList + prevMessages

            if msgList.__len__() > 0:
                curlMsg = msgFactory.createNodeMsgFromMultipleMsgs(msgList)

                try:
                    self.logger.log_operation("dispatching the message")
                    self.logger.log_debug(curlMsg.getBody())
                    msgDispatcher.dispatch(curlMsg)
                except DispatcherFailed, msg:
                    self.logger.log_error(str(msg))
                    failedMsgs = msgList

            if failedMsgs.__len__() > 0:
                try:
                    self.logger.log_operation("saving the failed messages into the database")
                    self.dbHelper.saveMessages(failedMsgs)
                except DBOpFailed, msg:
                    self.logger.log_error(msg)
            else:
                self.logger.log_operation("All messages dispatched successfully!")

            try:
                self.logger.log_operation("saving the currently parsed active nodes into the database")
                self.dbHelper.saveActiveNodes(currActiveNodes)
            except DBOpFailed, msg:
                self.logger.log_error("service ended with exception: " + msg+"\n")
                sys.exit(1)

        else:
            self.logger.log_error("service ended with exception: shell execution failed!\n")
            sys.exit(1)

        self.logger.log_operation("service ended\n")


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
