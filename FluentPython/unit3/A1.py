"""
对容器的'in'运算符做性能测试
"""

import sys
import timeit

SETUP = '''
import array
selected = array.array('d')
wht
'''