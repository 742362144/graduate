# coding:utf-8
import json
import time

class JsonTools(object):

    def decode_from_str(self, str):
        return json.loads(str)

    # 从文件中获取json数据
    def decodeFromFile(self, filename) :
        with open(filename, 'r') as f:
            data = json.load(f)
        return data

    # 将数据写入json文件
    def saveAsJson(self, filename, data):
        # 存入文件
        json_str = json.dumps(data)
        f = open(filename, 'w')
        f.write(json_str)