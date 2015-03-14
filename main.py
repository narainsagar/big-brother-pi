from FingParser import FingParser
from FingShellHandler import FingShellHandler
from SQLiteHelper import SQLiteHelper
from Base import Node, NODE_STATUS
from CURLMessage import CURLMessage
from CURLMessageFactory import CURLMessageFactory
from MessageDispatcher import MessageDispatcher


class Main:
    def __init__(self, parser, dbHelper):
        self.parser = parser
        self.dbHelper = dbHelper
        self.dbHelper.init()

    def startService(self):
        ret = FingShellHandler().execute()
        if ret != None:
            currActiveNodes = self.parser.parse(ret)
            prevActiveNodes = self.dbHelper.getActiveNodes()

            nodesDown = self.__getNodesDown(currActiveNodes, prevActiveNodes)
            nodesUp = self.__getNodesUp(currActiveNodes, prevActiveNodes)

            msgFactory = CURLMessageFactory()
            msgDispatcher = MessageDispatcher()

            for node in nodesDown:
                msg = msgFactory.createNodeMsg(node)
                msgDispatcher.dispatch(msg)

            for node in nodesUp:
                msg = msgFactory.createNodeMsg(node)
                msgDispatcher.dispatch(msg)

            self.dbHelper.saveActiveNodes(currActiveNodes)


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


main = Main(FingParser(), SQLiteHelper())
main.startService()