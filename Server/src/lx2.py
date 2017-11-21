#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/11/11 15:42
# @Author  : Tiancc
# @Site    : 
# @File    : lx2.py
# @Software: PyCharm


import socket, subprocess, struct, json

class Ser_shou:
    def __init__(self):
        cmd = socket.socket()
        cmd.bind(('127.0.0.1', 8119))
        cmd.listen(5)
        while True:
            self.conn, self.addrs = cmd.accept()
            print('客户端[%s:%s]尝试连接...' % (self.addrs[0], self.addrs[1]))
            while True:
                data = self.reav()
                self.socket_send(data,len(data))

    def reav(self):

        header_len = self.conn.recv(4)  # 包头大小为4,里面传送的为完整的包头长度
        head_len = struct.unpack('i', header_len)[0]

        # 收包头:
        head_bytes = self.conn.recv(head_len)  # 按照发送的包头长度收取包头
        header_dic = json.loads(head_bytes.decode('utf-8'))  # 取出完整包头数据

        total_size = header_dic.get('total_size')

        # 收数据
        data = b''
        recv_size = 0
        while recv_size < total_size:
            piece_data = self.conn.recv(1024)
            data += piece_data
            recv_size += len(piece_data)
        data = data.decode()
        print(data)
        return data

    def socket_send(self,data,total_size,**kwargs):
        header_dic = {
            'total_size': total_size,
        }
        header_dic.update(kwargs)
        header_json = json.dumps(header_dic).encode('utf-8')

        self.conn.send(struct.pack('i', len(header_json)))

        # 再发包头
        self.conn.send(header_json)

        # 真实数据
        print(header_dic)
        data=data.encode()
        self.conn.send(data)
        print('已完成发送数据给客户端')

Ser_shou()