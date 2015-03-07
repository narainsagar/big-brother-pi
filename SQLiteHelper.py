from Base import Node, NODE_STATUS
from IDBHelper import IDBHelper
import sqlite3
import os

class SQLiteHelper(IDBHelper):
    db_path = "service.db"

    def createTables(self):
        try:
            self.conn.execute("CREATE TABLE active_nodes (ip_addr TEXT NOT NULL, mac_addr TEXT NOT NULL, manufacturer_name TEXT)")
        except sqlite3.Error, msg:
            print msg #TODO: use logger to log


    def init(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.execute("select count(*) AS table_count from sqlite_master where type = \"table\";")
            row = cursor.next()
            if row["table_count"] == 0:
                self.createTables()
        except sqlite3.Error, msg:
            print msg #TODO: use logger to log
        finally:
            pass #TODO: log operation


    def getActiveNodes(self):
        try:
            activeNodes = []
            cursor = self.conn.execute("SELECT * FROM active_nodes")
            for row in cursor:
                activeNodes.append(Node(row["ip_addr"], row["mac_addr"], NODE_STATUS.UP, row["manufacturer_name"]))
            return activeNodes
        except sqlite3.Error, msg:
            print msg #TODO: use logger to log

    def saveActiveNodes(self, nodes):
        try:
            self.conn.execute("DELETE FROM active_nodes")
            for node in nodes:
                self.conn.execute("INSERT INTO active_nodes (ip_addr, mac_addr, manufacturer_name) VALUES (?,?,?)", (node.ip_addr, node.mac_addr, node.manufacturer_name))
            self.conn.commit()
        except (sqlite3.Error, AttributeError, TypeError), msg:
            print msg #TODO: use logger to log

    def saveMessages(self):
        pass

    def getMessages(self):
        pass

    def clearMessages(self):
        pass