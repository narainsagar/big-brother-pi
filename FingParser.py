from Base import Node, NODE_STATUS
from abc import ABCMeta, abstractmethod
from IParser import IParser
import os
import re

class FingParser(IParser):
    def parse(self):
        activeNodes = []
        ret = os.system("sudo fing -r 1 -o table,csv,discovery.txt")
        f = open('discovery.txt', 'r').readlines()
        if ret == 0:
            for i in range(0, len(f)):
                node = Node()
                node.ip_addr = f[i].split(";")[0]
                node.mac_addr = f[i].split(";")[5]
                node.manufacturer_name = f[i].split(";")[6].split('\n')[0]
                node.node_status = NODE_STATUS.UP
                activeNodes.append(node)

        return activeNodes