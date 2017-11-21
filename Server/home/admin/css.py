#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/11/9 10:35
# @Author  : Tiancc
# @Site    : 
# @File    : cs.py
# @Software: PyCharm


# import socket
#
# cmd = socket.socket()
# cmd.connect(('127.0.0.1',9001))
# while True:
#     _input = input('>>: ').strip()
#     if not _input:continue
#     cmd.send(_input.encode('utf-8'))
#     data = cmd.recv(1024)
#     print(data)
#
# cmd.closer()
#/Users/Tcc/Desktop/python/projects/WinFTP/Client/cs.py


#
# with open('.tcc','a') as data:
#     data.write()

# data = open('.tcc','a')
# recv_size = 0
# total_size=714
# while recv_size < total_size:
#     piece_data = self.coon.recv(1024)
#     data += piece_data
#     recv_size += len(piece_data)
# data = json.loads(data.decode())



header_dic = {
    'total_size': 12333,
    'actions':'put'
}


# if not header_dic['action']:
#     pass
# elif header_dic['action'] == 'put':
#     print('OK')
# print('abc')

try:
    if header_dic['action'] is 'put':
        print('ok')
except KeyError:pass
    # print('no')
print('abc')

# if hasattr(header_dic,header_dic['action']):
#     print('y')
#     if header_dic['action'] == 'put':
#         print('OK')
#     else:print('no')

# if  header_dic['action']:
#     if header_dic['action'] == 'put':
#         print('OK')
#     else:print('M')
#
# else:print('NO')

