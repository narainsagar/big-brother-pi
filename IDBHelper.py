from abc import ABCMeta, abstractmethod

class IDBHelper(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def getActiveNodes(self):
        pass

    @abstractmethod
    def saveActiveNodes(self):
        pass

    @abstractmethod
    def saveMessages(self):
        pass

    @abstractmethod
    def getMessages(self):
        pass