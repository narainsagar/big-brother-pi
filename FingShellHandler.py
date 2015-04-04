from Base import ShellLog
from abc import ABCMeta, abstractmethod
from IShellHandler import IShellHandler
import os
from Constants import Constants

class FingShellHandler(IShellHandler):
    def execute(self):
        ret = os.system("sudo fing -r 1 -o table,csv,"+Constants.PARSED_FILE)
        if ret == 0:
            return ShellLog("", Constants.PARSED_FILE)
        else:
            ret = None