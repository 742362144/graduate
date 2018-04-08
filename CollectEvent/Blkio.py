# coding:utf-8

import os
import sys
import time
import tempfile
import multiprocessing
from multiprocessing import Process

from .Tools import JsonTools

"""
1.获取docker blikio
2.获取容器的 blkio
"""


class BlkioCollector(object):
    # 一次读取的数据记录的结构
    """
        name: ,
        time: ,
        data: {
        },
        container[
            name: ,
            time: ,
            data: ,
        ]

    """

    def __init__(self):
        self.fs_path = '/sys/fs/cgroup/blkio/docker'
        self.blkio_filenames = ['blkio.io_merged',
                                'blkio.io_merged_recursive',
                                'blkio.io_queued',
                                'blkio.io_queued_recursive',
                                'blkio.io_service_bytes',
                                'blkio.io_service_bytes_recursive',
                                'blkio.io_serviced',
                                'blkio.io_serviced_recursive',
                                'blkio.io_service_time',
                                'blkio.io_service_time_recursive',
                                'blkio.io_wait_time',
                                'blkio.io_wait_time_recursive',
                                'blkio.leaf_weight',
                                'blkio.leaf_weight_device',
                                'blkio.reset_stats',
                                'blkio.sectors',
                                'blkio.sectors_recursive',
                                'blkio.throttle.io_service_bytes',
                                'blkio.throttle.io_serviced',
                                'blkio.throttle.read_bps_device',
                                'blkio.throttle.read_iops_device',
                                'blkio.throttle.write_bps_device',
                                'blkio.throttle.write_iops_device',
                                'blkio.time',
                                'blkio.time_recursive',
                                'blkio.weight',
                                'blkio.weight_device',
                                'cgroup.clone_children',
                                'cgroup.procs',
                                'notify_on_release',
                                'tasks']
        self.container_filenames = []
        # 子进程
        self.out_temp = tempfile.TemporaryFile(mode='w+')
        self.flag = multiprocessing.Value('i', 1)
        self.proc = Process(target=self.task, args=(self.flag, self.out_temp))

    # 获得文件内容(以string的形式)
    def get_file_content(self, filename):
        # 打开文件，并记录句柄
        try:
            fw = open(filename, "r")
        except IOError:
            print("Error: 文件" + filename + "没有找到或读取失败")
            return 'error'
        else:
            lines = fw.readlines()
            return lines

    # 读取当前docker目录下所以的blkio记录
    def get_record(self, out_temp):
        record = {}
        record['name'] = 'docker'
        # 记录时间
        record['time'] = time.time()
        # 读取docker的cgroup blkio信息
        record['data'] = self.get_blkio_record(self.fs_path)
        record['containers'] = []
        # 获得当前的container文件名
        container_ids = self.get_container_id()
        # 读取container的cgroup blkio信息
        for filename in container_ids:
            path = self.fs_path + '/' + filename
            record['containers'].append(self.get_blkio_record(path))
        # 写入临时文件
        out_temp.write(str(record) + '\n')

    # 获得当前所有的container
    def get_container_id(self):
        path = "/sys/fs/cgroup/blkio/docker"  # 文件夹目录
        filenames = os.listdir(path)  # 得到文件夹下的所有文件名称
        ids = []
        for filename in filenames:
            if len(filename) == 64:
                ids.append(filename)
        return ids

    # 获得一个路径下的blkio事件
    def get_blkio_record(self, path):
        record = {}
        for filename in self.blkio_filenames:
            record[filename] = self.get_file_content(self.fs_path + '/' + filename)
        return record

    def task(self, flag, out_temp):
        # 死循环获取记录
        while flag.value > 0:
            self.get_record(out_temp)
            sys.stdout.flush()
            time.sleep(1)

    def get_result(self):
        result = []
        tool = JsonTools()
        # 从临时文件读出结果
        self.out_temp.write(']')
        self.out_temp.seek(0)
        rt = self.out_temp.read()

        # 以换行符拆分数据，并去掉换行符号存入列表
        self.rt_list = rt.strip().split('\n')
        for line in self.rt_list:
            result.append(tool.decode_from_str(line))

        tool.saveAsJson('blkio.json', result)
        # 关闭并删除临时文件
        if self.out_temp:
            self.out_temp.close()

    # 主要有两部分
    # 1.整个cgroup的事件
    # 2.每个容器的事件
    # 开个子进程去搜集blkio子系统的信息
    def start(self):
        self.out_temp.write('[')
        self.proc.start()

    # 停止搜集blkio
    def stop(self):
        self.flag.value = -1
        self.proc.terminate()
        self.get_result()


if __name__ == "__main__":
    io = BlkioCollector()
    io.start()
    time.sleep(10)
    io.stop()