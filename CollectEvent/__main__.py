# coding:utf-8

from .CollectData import DataCollector
from .OperateMongo import OperateMongoDB

if __name__ == '__main__' :
    collect = DataCollector()
    collect.start()
    test = OperateMongoDB()
    test.performance_test()
    collect.stop()
# {"protocol":"auth_aes128_md5", "password":"312312312", "obfs":"tls1.2_ticket_auth", "obfs_param":""}