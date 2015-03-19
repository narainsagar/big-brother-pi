from Base import Node, NODE_STATUS, ShellLog
from abc import ABCMeta, abstractmethod
from IParser import IParser
import os
import re
import logging
from FingShellHandler import FingShellHandler
from ServiceExceptions import ParserFailed

class FingParser(IParser):
    def parse(self, shellLog):
        activeNodes=[]
        try:
            f = open(shellLog.discovery_log, 'r').readlines()
            for i in range(0, len(f)):
                node = Node()
                node.ip_addr = f[i].split(";")[0]
                node.mac_addr = f[i].split(";")[5]
                node.manufacturer_name = f[i].split(";")[6].split('\n')[0]
                node.node_status = NODE_STATUS.UP
                activeNodes.append(node)
            return activeNodes
        except Exception, msg:
            raise ParserFailed(msg)