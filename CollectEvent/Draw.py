# coding:utf-8

import matplotlib.pyplot as plt
from .Tools import JsonTools

class Draw(object):

    def __init__(self, file):
        self.tool = JsonTools()
        self.data = self.tool.decodeFromFile('')

    def draw(self):
        pass

plt.plot([3, 1, 4, 5, 2])
plt.ylabel('grade')
#保存文件
plt.savefig('test', dpi=600)
plt.show()
