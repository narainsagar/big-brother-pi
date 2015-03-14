__author__ = 'analytics'
from Base import ShellLog
from abc import ABCMeta, abstractmethod
from IShellHandler import IShellHandler
import os

class FingShellHandler(IShellHandler):
    def execute(self):
        ret = os.system("sudo fing -r 1 -o table,csv,discovery.txt")
        if ret == 0:
            return ShellLog("", "discovery.txt")
        else:
            ret = None