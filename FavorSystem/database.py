import sys
import sqlite3
from typing import Dict, List


class ConnectionPool(object):
    
    def __init__(self, database: str, max_conn_count: int=5):
        self.database: str = database
        self.connections: List = []
        self.max_conn_count: int = max_conn_count
        self.InitPool()
        
    def InitPool(self):
        try:
            for i in range(self.max_conn_count):
                self.connections.append(sqlite3.connect(self.database, check_same_thread=False))
        except Exception as e:
            print(f"[Error]: {e}")
            self.ClosePool()
            sys.exit("[Error]: init connection pool error!")
    
    def ClosePool(self):
        if len(self.connections) > 0:
            for conn in self.connections:
                conn.close()

    def GetConnection(self):
        if len(self.connections) == 0:
            self.InitPool()
        return self.connections.pop()

    def CloseConnection(self, conn):
        self.connections.append(conn)
