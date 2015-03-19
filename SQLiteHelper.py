from Base import Node, NODE_STATUS
from IDBHelper import IDBHelper
from CURLMessage import CURLMessage
from ServiceExceptions import DBOpFailed
import sqlite3
import os

class SQLiteHelper(IDBHelper):
    db_path = "service.db"

    def __init__(self):
        pass

    def __dropTables(self):
        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for row in cursor:
            self.conn.execute("DROP TABLE IF EXISTS " + row['name'])
        self.conn.commit()

    def __createTables(self):
        self.conn.execute("CREATE TABLE active_nodes (ip_addr TEXT NOT NULL, mac_addr TEXT NOT NULL, manufacturer_name TEXT)")
        self.conn.execute("CREATE TABLE messages (headers TEXT, body TEXT)")
        self.conn.commit()

    def init(self, version):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.execute("PRAGMA user_version")
            row = cursor.next()
            if row["user_version"] < version:
                self.conn.execute("PRAGMA user_version = " + str(version))
                self.__dropTables()
                self.__createTables()
        except Exception, msg:
            raise DBOpFailed(msg)


    def getActiveNodes(self):
        try:
            activeNodes = []
            cursor = self.conn.execute("SELECT * FROM active_nodes")
            for row in cursor:
                node = Node()
                node.ip_addr = row["ip_addr"]
                node.mac_addr = row["mac_addr"]
                node.manufacturer_name = row["manufacturer_name"]
                activeNodes.append(node)
            return activeNodes
        except (sqlite3.Error), msg:
            raise DBOpFailed(msg)

    def saveActiveNodes(self, nodes):
        try:
            self.conn.execute("DELETE FROM active_nodes")
            for node in nodes:
                self.conn.execute("INSERT INTO active_nodes (ip_addr, mac_addr, manufacturer_name) VALUES (?,?,?)", (node.ip_addr, node.mac_addr, node.manufacturer_name))
            self.conn.commit()
        except Exception, msg:
            raise DBOpFailed(msg)

    def saveMessages(self, msgList):
        try:
            for msg in msgList:
                self.conn.execute("INSERT INTO messages (headers, body) VALUES (?,?)", (";;".join(msg.getHeaders()), msg.getBody()))
            self.conn.commit()
        except Exception, msg:
            raise DBOpFailed(msg)

    def getMessages(self):
        msgList = []
        try:
            cursor = self.conn.execute("SELECT * FROM messages")
            for row in cursor:
                msg = CURLMessage()
                msg.setHeaders(row["headers"].split(";;"))
                msg.setBody(row["body"])
                msgList.append(msg)
            self.conn.execute("DELETE FROM messages")
            self.conn.commit()
            return msgList
        except Exception, msg:
            raise DBOpFailed(msg)