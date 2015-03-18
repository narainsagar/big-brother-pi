from abc import ABCMeta, abstractmethod

class ILogger(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def log_operation(self, Message):
        pass
    @abstractmethod
    def log_error(self, Message):
        pass