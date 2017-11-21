#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/11/16 11:32
# @Author  : Tiancc
# @Site    : 
# @File    : jdt.py
# @Software: PyCharm



##########
# def progress(total):
#     received_size = 0
#     current_percent = 0
#     while received_size < total:
#         if int((received_size / total) * 100 ) > current_percent :
#             print('#',end='',flush=True)
#             current_percent = int((received_size / total) * 100 )
#             new_size = yield
#             received_size += new_size
#
# runin = progress(100)
#
# runin.__next__()   #next(runin)
#
# i=0
# b = 52
# while i < b :
#     print('zhixing')
#     runin.send(i)
#     i+=2

#循环
import time
for i in range(10):
    print('#',end='',flush=True)
    time.sleep(0.4)