# coding: utf-8

from multiprocessing import Process
import multiprocessing
import time


def task1(msg):
    print('task1: hello, %s' % msg)
    time.sleep(1)


def task2(msg):
    print('task2: hello, %s' % msg)
    time.sleep(1)


def task3(msg):
    print( 'task3: hello, %s' % msg)
    time.sleep(1)


if __name__ == '__main__':
    p1 = Process(target=task1, args=('one',))
    p2 = Process(target=task2, args=('two',))
    p3 = Process(target=task3, args=('three',))

    start = time.time()

    p1.start()
    p2.start()
    p3.start()

    print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print("child p.name: " + p.name + "\tp.id: " + str(p.pid))

    p1.join()
    p2.join()
    p3.join()

    end = time.time()
    print('3 processes take %s seconds' % (end - start))