class Node:
    def __init__(self):
        pass

    def __init__(self):
        self.ip_addr = ""
        self.mac_addr = ""
        self.node_status = 0
        self.manufacturer_name = ""

    def __str__(self):
        return "ip_addr: " + self.ip_addr + "; mac_addr: " + self.mac_addr + "; manufacturer_name: " + self.manufacturer_name

    def __repr__(self):
        return self.__str__()

class NODE_STATUS:
    UP = 1
    DOWN = 0

class ShellLog:
    def __init__(self, error_log, discovery_log):
        self.error_log = error_log
        self.discovery_log = discovery_log