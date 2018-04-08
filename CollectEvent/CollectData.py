# coding:utf-8

import subprocess
from .IOStat import IOStatCollector
from .Blkio import BlkioCollector


class DataCollector(object):

    def __init__(self):
        self.iostatCollector = IOStatCollector()
        self.blkioCollector = BlkioCollector()

    def start(self):
        # 开始搜集数据
        self.iostatCollector.start()
        self.blkioCollector.start()

    # 停止搜集
    def stop(self):
        self.iostatCollector.stop()
        self.blkioCollector.stop()
