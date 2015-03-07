__author__ = 'abdulqadir'
from abc import ABCMeta, abstractmethod

class Node:
    def __init__(self, ip_addr, mac_addr, node_status, manufacturer_name):
        self.ip_addr = ip_addr
        self.mac_addr = mac_addr
        self.node_status = node_status
        self.manufacturer_name = manufacturer_name

class NODE_STATUS:
    UP = 1
    DOWN = 0

class ShellLog:
    def __init__(self, error_log, discovery_log):
        self.error_log = error_log
        self.discovery_log = discovery_log



