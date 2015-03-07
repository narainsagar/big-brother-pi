from abc import ABCMeta, abstractmethod

class IParser(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self):
        pass