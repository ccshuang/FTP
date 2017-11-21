#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/11/8 14:06
# @Author  : Tiancc
# @Site    : 
# @File    : a.py
# @Software: PyCharm


#/Users/Tcc/Desktop/python/projects/WinFTP/Client/css.py
# db='100'
# try:
#
#     if int(db) == 100:
#         print('OK')
#
# except Exception:pass
#
# print('123')


# SERVER_MESSAGE = {
#     0:'Unknown Error: 服务器未相应',
#     99:'Bath Error: 命令错误',
#     100:'Login successfully!',
#     101:'Authentication Error: 用户名或密码错误',
#     102:'命令无法达到预期效果,未完成',
#     109:'',
#     110:'Command execute!'
# }
# da={'action': 'ls', 'total_size': 2}
#
# if not int(da):
#     print('ok')
# else:print('no')

# if da in SERVER_MESSAGE:
#     print('OK')
# else:print('NO')

# a=['rm', 'abc.txt,css.py']
# print(len(a))


# aa=6
#
# if aa == 1:
#     print('1,OK')
# elif aa == 2:
#     print('2.OK')
# # else:print('NO')
# print(aa)
#
# da = {'action': 'ls', 'total_size': 2, 'f_path': 'a'}
# ab = da['f_path']
# if ab:
#     print('OK',type(da))
# else:print('NO')


##########
import time
# def progress(total):
#     received_size = 0  #
#     current_percent = 0 #
#     while received_size < total:
#         if (received_size / total) * 10 > current_percent :
#             print('#%s'%current_percent,end='',flush=True)
#             current_percent = (received_size / total) * 10
#         new_size = yield
#         received_size += new_size
# data_size = 100
# runin = progress(data_size)
#
# runin.__next__()   #next(runin)
#
# receive_size=0
#
# while receive_size < data_size :
#     # print(i)
#     try:
#         runin.send(receive_size)
#     except StopIteration:
#         print('100%')
#         # break
#     time.sleep(0.8)
#     receive_size+=10

#循环
# import time
# for i in range(10):
#     print('#',end='',flush=True)
#     time.sleep(0.4)

#
data_size = 800

def progress(total):    #800
    received_size = 0   #0,110,210,310,410,510,610
    current_percent = 0 #0,2  ,5  ,7  ,10 ,12,15
    while received_size < total:
        if int((received_size / total) * 100)  > current_percent :
            print('#', end='', flush=True)
            current_percent = int((received_size / total) * 100 )
        new_size = yield
        received_size += new_size


pg = progress(data_size)
pg.__next__()

line = 0
while line < data_size:
    try:
        a=pg.send(line)
    except StopIteration :
        print('\t100%')
        break
    line += 3
    time.sleep(0.1)
print('yes')

if __name__ == '__main__':



