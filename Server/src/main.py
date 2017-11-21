#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/11/9 10:54
# @Author  : Tiancc
# @Site    : 
# @File    : main.py
# @Software: PyCharm

import configparser,struct
import json,os,socket
from conf import settings as conf
from multiprocessing import Process

class FtpServerr:
    max_packet_size = 1024
    def __init__(self):
        print('The FTP server program began to run!')
        cmd = socket.socket()
        cmd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cmd.bind((conf.HOST,conf.PORT))
        cmd.listen(5)

        while True:
            self.coon, self.addrs = cmd.accept()
            print('客户端[%s:%s]尝试连接...' % (self.addrs[0], self.addrs[1]))
            process = Process(target=self.dispense)
            process.start()
        cmd.close()

    def dispense(self):
        while True:
            try:
                header_len = self.coon.recv(4)  # 包头大小为4,里面传送的为完整的包头长度
                head_len = struct.unpack('i', header_len)[0]
                head_bytes = self.coon.recv(head_len)  # 按照发送的包头长度收取包头
                header_dic = json.loads(head_bytes.decode('utf-8'))  # 取出完整包头数据

                if header_dic['action'] == 'put':
                    self._put(header_dic)  # 如果是上传文件执行执行_put函数
                    continue

                total_size = header_dic.get('total_size')

                # 收数据
                data = b''
                recv_size = 0
                while recv_size < total_size:
                    piece_data = self.coon.recv(self.max_packet_size)
                    data += piece_data
                    recv_size += len(piece_data)
                data = json.loads(data.decode())

                print('包头数据 > ', header_dic)
                print('真实数据 > ', data)

                if hasattr(self, '_%s' % header_dic['action']):
                    func = getattr(self, '_%s' % header_dic['action'])
                    func(data)
                    # print('22 准备传数据给_auth',data)
                else:
                    self.socket_send(99, 2)
            except Exception as a:
                print('!>>! : ', a)
                # self.coon.close()
                break
        self.coon.close()


    def socket_send(self,data,total_size,action='obj',**kwargs):
        header_dic = {
            'action':action,
            'total_size':total_size
        }
        header_dic.update(kwargs)
        header_json = json.dumps(header_dic).encode('utf-8')

        self.coon.send(struct.pack('i', len(header_json)))

        # 再发包头
        self.coon.send(header_json)

        # 真实数据
        data = json.dumps(data).encode('utf-8')
        self.coon.send(data)
        return True

    def _auth(self,data):
        certification = os.path.join(conf.USER_PWD, 'conf.json')
        with open(certification, 'r') as f:
            user_db = json.loads(f.read())

        self.user = data['name']

        if self.user in user_db and data['pasd'] == user_db[self.user]['pasd']:
            self.socket_send(100,3)
            print('用户:[{u}],通过[{i}:{p}] 成功登录FTP'.format(i=self.addrs[0],p=self.addrs[1],u=self.user))
            # self.user_swarm
        else:self.socket_send(101,3)

    def _put(self,data):
        print('put命令: ',data,len(data['updir']))
        # if len(data['updir']) > 0:
        if  data['updir']:
            up_dir = data['updir'][0]
            f_path = os.path.join(conf.USER_HOME, self.user,up_dir)
            if os.path.isdir(f_path):
                file_path = os.path.join(f_path,data['filename'])
            else:self.socket_send(103,3)
        else:
            file_path = os.path.join(conf.USER_HOME,self.user,data['filename'])

        filesize =  data['total_size']
        recv_size = 0
        with open(file_path, 'wb') as f:
            while recv_size < filesize:
                piece_data = self.coon.recv(self.max_packet_size)
                f.write(piece_data)
                recv_size += len(piece_data)
                print('以上传大小:%s 总大小:%s' % (recv_size, filesize))
            else:self.socket_send(110,3)
            # old = os.path.basename(file_path)
            # new = os.path.join(conf.USER_HOME,self.)
            # os.rename(os.path.basename(file_path),data['filename'])

    def _ls(self,args):
        print('执行ls',args,type(args),len(args))
        if len(args) > 1:
            f_path = args[1]
            d_path = os.path.join(conf.USER_HOME,self.user,f_path)
            if os.path.isdir(d_path):
                filename=os.listdir(d_path)
            else:self.socket_send(103,3)
        else:
            filename = os.listdir(os.path.join(conf.USER_HOME,self.user))

        if not filename:self.socket_send(109,3)
        else:self.socket_send(filename,len(filename))

    def _rm(self,args):
        print('rm命令执行',args)
        user_path = os.path.join(conf.USER_HOME,self.user)
        file_path = os.path.join(user_path,args[1])
        for i in args:
            if i == '-r':
                print('准备删除目录')
                if os.path.isdir(os.path.join(user_path,args[2])):
                    # n = len(os.listdir(os.path.join(user_path,args[2])))
                    if len(os.listdir(os.path.join(user_path,args[2]))) == 0:
                        os.rmdir(os.path.join(user_path,args[2]))
                        self.socket_send(110,3)
                        return
                    else:
                        self.socket_send(104,3)
                        return
                elif os.path.isdir(file_path):
                    if len(file_path) == 0:
                        os.rmdir(file_path)
                        self.socket_send(110,3)
                        return
                    else:
                        self.socket_send(104, 3)
                        return

                elif not os.path.isdir(os.path.join(user_path,args[2]))\
                    and os.path.isdir(file_path):
                    self.socket_send(103,3)
                    return

        if os.path.isfile(file_path):
            os.remove(file_path)
            self.socket_send(110,3)
            # print(file_path,type(file_path))
        else:self.socket_send(103,3)

    def _mkdir(self,args):
        # print('mkdir命令执行 ',args)
        user_path = os.path.join(conf.USER_HOME,self.user)
        dir_name = os.path.join(user_path,args[1])
        if os.path.isdir(dir_name):
            self.socket_send(103,3)
        else:
            os.mkdir(dir_name)
            self.socket_send(110,3)

    def _get(self,args):
        print('get命令执行',args)
        # print(a,len(a))
        # self.socket_send(a,len(a))

    @staticmethod
    def create():
        db_path = os.path.join(conf.USER_PWD, 'conf.json')
        while True:
            print("\n'exit' 退出\n")
            if (os.path.isfile(db_path)):
                with open(db_path, 'r') as f:
                    # data = f.read()
                    # db = json.loads(data)
                    db = json.loads(f.read())
                    # d = 'a'
            else:db = {}
            u_name = input('输入账号>: ').strip()
            if not u_name:continue
            elif u_name == 'exit':break
            u_pasd = input('输入密码>: ').strip()
            if not u_pasd: continue
            u_pasds = input('确认密码>: ').strip()
            if not u_pasd == u_pasds:print('两次密码输入不匹配,重新创建.')
            elif u_name in db:print('用户名已存在!请重新创建.')
            else:
                db[u_name] = {'name':u_name,'pasd':u_pasd}
                # db_path = os.path.join(conf.USER_PWD,'conf.json')
                with open(db_path,'w') as f:
                    f.write(json.dumps(db))
                config = configparser.ConfigParser()
                config[u_name] = {
                    'password': u_pasd,
                    'quota': 100
                }
                with open(conf.USER_CONF, 'a') as configfile:
                    config.write(configfile)
                os.mkdir(os.path.join(conf.USER_HOME,u_name))   #创建用户家目录
                print('创建成功')
                break
            continue

if __name__ == '__main__':
    FtpServerr.auth()