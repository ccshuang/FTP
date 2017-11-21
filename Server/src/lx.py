#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/11/9 13:09
# @Author  : Tiancc
# @Site    : 
# @File    : lx.py
# @Software: PyCharm

# import json
# udict={
#     'cc':{'name':'cc','passd':'123'},
#     'yy':{'name':'yy','passd':'234'}
# }
#
# with open('a.json','w') as f:
#     f.write(json.dumps(udict))

# import json,os
# #
# # def abc():
# #     if os.path.isfile('d.json'):
# #         with open('d.json', 'r') as f:
# #             data = f.read()
# #             db = json.loads(data)
# #             # d = 'a'
# #     else:
# #         db={}
# #         # d='w'
# #     us= input('name>: ').strip()
# #     ps= input('pswd>: ').strip()
# #     db[us] = {'name':us,'pasd':ps}
# #     with open('d.json','w') as f:
# #         f.write(json.dumps(db))
# #     return db
# # #
# # print(abc())
# # if os.path.isfile('b.json'):
#     # print('OK')
#
# # def bc():
# #     with open('b.json','r')as f:
# #         print(f.read(json.dump()))
#
# # print(json.load(open('b.json','r')))
#
#
# import argparse
# parser = argparse.ArgumentParser(description="say something about this application !!")
# parser.add_argument("--age", help="this is an optional argument")
# result = parser.parse_args()
# print(result.age)

import socket,struct,json

#{'action':'auth','name':'tcc','pasd':'123'}
class shou:
    def __init__(self):
        self.cmd = socket.socket()
        self.cmd.connect(('127.0.0.1', 9007))
        while True:
            u_in = input('>>>').strip()
            if not u_in:
                u_in='hello'
            users = u_in.encode()
            self.socket_send(users,len(u_in))
            self.socket_recv()

    def socket_send(self, data, total_size, **kwargs):
        header_dic = {
            'total_size': total_size,
        }
        header_dic.update(kwargs)
        header_json = json.dumps(header_dic).encode('utf-8')

        self.cmd.send(struct.pack('i', len(header_json)))

        # 再发包头
        self.cmd.send(header_json)

        # 真实数据
        print('给服务器发送数据中...',header_dic)
        self.cmd.send(data)

    def socket_recv(self):
        # 收包头长度
        header_len = self.cmd.recv(4)  # 包头大小为4,里面传送的为完整的包头长度
        head_len = struct.unpack('i', header_len)[0]

        # 收包头:
        head_bytes = self.cmd.recv(head_len)  # 按照发送的包头长度收取包头
        # head_json = head_bytes.decode('utf-8')
        header_dic = json.loads(head_bytes.decode('utf-8'))  # 取出完整包头数据

        total_size = header_dic.get('total_size')

        # 收数据
        # with open('cachefile','wb') as f:
        cmd_res = b''
        recv_size = 0
        # open('cachefile','w')
        while recv_size < total_size:
            data = self.cmd.recv(1024)
            cmd_res += data
            # with open('cachefile','ab') as f:
            #     f.write(data)
            recv_size += len(data)
        # with open('cachefile','rb') as f1:
        #     print(f1.read().decode())


        print('服务器返回的数据>>: ',cmd_res.decode())

shou()



