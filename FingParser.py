from Base import Node, NODE_STATUS
from abc import ABCMeta, abstractmethod
from IParser import ParserBase
import os
import re

class FingParser(ParserBase):
    def parserMain(self):
        activeNodes = []
        ret = os.system("sudo fing -r 1 -o table,csv,discovery.txt")
        f = open('discovery.txt', 'r').readlines()
        if ret == 0:
            for i in range(0, len(f)):
                ip_addr = f[i].split(";")[0]
                mac_addr = f[i].split(";")[5]
                manufacturer_name = f[i].split(";")[6].split('\n')[0]
                activeNodes.append(Node(ip_addr, mac_addr, NODE_STATUS.UP, manufacturer_name))
        for node in activeNodes:
            print str(node)
        return activeNodes

FingParser().parserMain()