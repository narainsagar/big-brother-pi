import sys

from core import *
from base import *
from core.ServiceExceptions import *


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
            #tries to parse the shellLog file created by fing
            try:
                self.logger.log_operation("Parsing fing output")
                currActiveNodes = self.parser.parse(shellLog)
                self.logger.log_debug("Parsed fing output and current Active nodes are :\n"+currActiveNodes.__repr__())
            #throws an error in log file if unable to parse and stops the functions
            except ParserFailed, msg:
                self.logger.log_error("service ended with parser failed: " + str(msg)+"\n")
                sys.exit(1)
            #tries to fetch previous node that were active from database
            try:
                self.logger.log_operation("fetching previous active nodes from database")
                prevActiveNodes = self.dbHelper.getActiveNodes()
                self.logger.log_debug("fetched previous active nodes from database:\n"+prevActiveNodes.__repr__())
            #throws an error in log file if unable to get previous active nodes and stops the functions
            except DBOpFailed, msg:
                self.logger.log_error("service ended while fetching previous active nodes: \n" + msg+"\n")
                sys.exit(1)

            msgFactory = CURLMessageFactory()
            msgDispatcher = MessageDispatcher()

            nodeList = self.__getNodes(currActiveNodes, prevActiveNodes)

            prevMessages = []
            msgList = []
            failedMsgs = []

            if nodeList.__len__() > 0:
                msgList.append(msgFactory.createNodeMsg(nodeList))
            #trying to fetch previous failed message from database
            try:
                self.logger.log_operation("fetching previous failed messages from database")
                prevMessages = self.dbHelper.getMessages()
                self.logger.log_debug("fetched previous failed message from database:\n"+prevMessages.__repr__())
            except DBOpFailed, msg:
                self.logger.log_error(msg)
            msgList = msgList + prevMessages

            if msgList.__len__() > 0:
                curlMsg = msgFactory.createNodeMsgFromMultipleMsgs(msgList)

                #tries to dispatch the current and previous failed messages to server
                try:
                    self.logger.log_operation("dispatching the message")
                    self.logger.log_debug(curlMsg.getBody())
                    msgDispatcher.dispatch(curlMsg)
                except DispatcherFailed, msg:
                    self.logger.log_error(str(msg))
                    failedMsgs = msgList

            if failedMsgs.__len__() > 0:
                #tries to save failed messages in database
                try:
                    self.logger.log_operation("saving the failed messages into the database")
                    self.dbHelper.saveMessages(failedMsgs)
                    self.logger.log_debug("successfully saved failed message to database:\n"+failedMsgs.__repr__())
                except DBOpFailed, msg:
                    self.logger.log_error("saving of failed messages to database was unsuccessful:\n"+msg)
            else:
                self.logger.log_operation("All messages dispatched successfully!")
            #saves active nodes to database
            try:
                self.logger.log_operation("saving the currently parsed active nodes into the database")
                self.dbHelper.saveActiveNodes(currActiveNodes)
                self.logger.log_debug("saved current active nodes to database:\n"+currActiveNodes.__repr__())
            except DBOpFailed, msg:
                self.logger.log_error("service ended while saving active node in database :\n" + msg)
                sys.exit(1)

        else:
            self.logger.log_error("service ended with exception: shell execution failed!\n")
            sys.exit(1)

        self.logger.log_operation("service ended\n")

    #checks which node went up(Became active)and which went down(Became Inactive)
    def __getNodes(self, currActiveNodes, prevActiveNodes):
        nodesUp = []
        nodesDown = []
        #loops through all the active nodes and compare them with previous active node to see which node went up
        for currNode in currActiveNodes:
            bool = False
            for prevNode in prevActiveNodes:
                if currNode.mac_addr == prevNode.mac_addr:
                    bool = True

            if bool == False:
                currNode.node_status = NODE_STATUS.UP
                nodesUp.append(currNode)
        #loops through all the a nodes in previous active node then compare it with the active nodes to see which node went down
        for prevNode in prevActiveNodes:
            bool = False
            for currNode in currActiveNodes:
                if prevNode.mac_addr == currNode.mac_addr:
                    bool = True

            if bool == False:
                prevNode.node_status = NODE_STATUS.DOWN
                nodesDown.append(prevNode)

        return nodesDown + nodesUp


main = Main(FingShellHandler(), FingParser(), SQLiteHelper(), Logger())

main.startService()
