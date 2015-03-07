from FingParser import FingParser
from SQLiteHelper import SQLiteHelper

dbHelper = SQLiteHelper()
dbHelper.init()
activeNodes = dbHelper.getActiveNodes()
for node in activeNodes:
    print str(node)
