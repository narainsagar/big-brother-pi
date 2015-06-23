from abc import ABCMeta, abstractmethod

class IShellHandler(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def execute(self):
        pass