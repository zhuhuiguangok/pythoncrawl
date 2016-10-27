# encoding: utf-8
import pymongo
from pymongo import MongoClient
class DBConn():
    conn = None
    servers = 'mongodb://' + 'manager' + ':' + '000' + '@' + '121.42.37.69' + ':' + '22192' +'/'+ 'admin'

    def connect(self):
        self.conn =pymongo.MongoClient('192.168.1.192', 27017)

    def close(self):
        return self.conn.disconnect()

    def getConn(self):
        return self.conn

