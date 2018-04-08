# coding:utf-8
import multiprocessing
from multiprocessing import Process
from pymongo import MongoClient

class OperateMongoDB(object):

    def performance_test(self):
        conn = MongoClient('127.0.0.1', 27017)
        # 连接mydb数据库，没有则自动创建
        db = conn.mydb

        # 使用test_set集合，没有则自动创建
        my_set = db.test_set

        # 插入数据
        for i in range(100000):
            my_set.insert({
                "id": i,
                "name":"zhangsan",
                "age":18,
                "location": "Beijing China",
                "phone": "123456789"
            })
