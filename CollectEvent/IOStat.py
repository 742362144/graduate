# coding: utf-8

import os
import re
import sys
import time
import multiprocessing
import tempfile
from multiprocessing import Process
import subprocess
from .Tools import JsonTools

class IOStatCollector(object):

    def __init__(self):
        self.cmd = 'iostat -kxt 1'
        self.flag = multiprocessing.Value('d', 1.0)
        # 子进程
        self.out_temp = tempfile.TemporaryFile(mode='w+')
        self.proc = Process(target=self.exec_cmd, args=(self.cmd, self.flag, self.out_temp))
        # cmd执行的结果
        self.rt_list = None

    # def exec_cmd(self):
    #     # 要执行的命令
    #     cmd = 'iostat -kxt 1'
    #     # 启动子进程执行命令
    #     self.sub_proc = os.popen(cmd)
    #     # 读取命令执行结果
    #     while 1:
    #         line = self.sub_proc.readline()
    #         print(line)
    #         if line.startswith('sda'):
    #             self.records.append(line)

    def exec_cmd(self, cmd, flag, out_temp):
        try:
            # 获取临时文件的文件号
            fileno = out_temp.fileno()

            # 执行外部shell命令， 输出结果存入临时文件中
            sub_proc = subprocess.Popen(cmd, shell=True, stdout=fileno, stderr=fileno)
            # 退出
            while flag.value > 0:
                time.sleep(1)
            sub_proc.terminate()

        except Exception as e:
            print(e)



    # 获取cmd的执行结果
    def get_result(self):
        result = []
        # 从临时文件读出shell命令的输出结果
        self.out_temp.seek(0)
        rt = self.out_temp.read()

        # 以换行符拆分数据，并去掉换行符号存入列表
        self.rt_list = rt.strip().split('\n')

        for line in self.rt_list:
            data = {}
            if not line.startswith('sda'):
                self.rt_list.remove(line)
            rt = line.split()
            data['id'] = rt[0]
            data['rrqm'] = rt[1]
            data['r'] = rt[2]
            data['w'] = rt[3]
            data['rsec'] = rt[4]
            data['wsec'] = rt[5]
            data['rkb'] = rt[6]
            data['wkb'] = rt[7]
            data['avgrq-sz'] = rt[8]
            data['avgqu-sz'] = rt[9]
            data['await'] = rt[10]
            data['svctm'] = rt[11]
            data['%util'] = rt[12]
            result.append(data)

        # print(self.rt_list)
        tool = JsonTools()
        tool.saveAsJson('iostat.json', result)
        # 关闭并删除临时文件
        if self.out_temp:
            self.out_temp.close()


    # 开始任务,启动子进程
    def start(self):
        self.proc.start()

    # 停止进程
    def stop(self):
        # 停止子进程
        self.flag.value = -1.0
        self.proc.terminate()
        # 结果存进文件
        self.get_result()

if __name__ == "__main__":
    io = IOStatCollector()
    io.start()
    time.sleep(10)
    io.stop()