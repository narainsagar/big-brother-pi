from abc import ABCMeta, abstractmethod

class ParserBase(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def parserMain(self):
        pass