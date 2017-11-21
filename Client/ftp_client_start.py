#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/11/9 09:40
# @Author  : Tiancc
# @Site    : 
# @File    : start.py
# @Software: PyCharm

import socket,json,re
import argparse,struct,os


SERVER_MESSAGE = {
    0:'Unknown Error: 服务器未相应',
    99:'Bath Error: 命令错误',
    100:'Login successfully!',
    101:'Authentication Error: 用户名或密码错误.',
    102:'命令无法达到预期效果,未完成!',
    103:'文件名未找到或文件已存在',
    104:'文件夹不为空,不能执行删除操作!',
    109:'',
    110:'Execute the command successfully!'
}

class FtpClient:
    max_packet_size = 1024
    def __init__(self):
        parser = argparse.ArgumentParser(description='Used to open the FTP client')
        parser.add_argument('-s', '--server',action='store', help='FTP server IP')   #default='localhost'
        parser.add_argument('-P', '--port', type=int,default=9007, choices=[9006,9007,9008], help='FTP server Port')  #choices=range(0, 65535) 显示问题??
        parser.add_argument('-u', '--user', help='username')
        parser.add_argument('-p', '--password', help='userpassword')


        self.args = parser.parse_args()
        if self.args.server is None:
            parser.print_help()
            exit()

        self.verify_args()
        self.coon_server()

    def coon_server(self):
        self.sock = socket.socket()
        # self.sock.connect((self.args.server, self.args.port))
        self.sock.connect((self.args.server, self.args.port))

    def verify_args(self):
        while True:
            if self.args.user is None:
                self.args.user = input('username>: ').strip()
                if not self.args.user: continue
            if self.args.password is None:
                self.args.password = input('password>: ').strip()
                if not self.args.password: continue
            # print(self.args)
            # break
            return self.args.user,self.args.password

    def authentication(self):
        userdb ={
            # 'action':'auth',
            'name':self.args.user,
            'pasd':self.args.password
        }
        # userdbs = json.dumps(userdb).encode()
        # print(userdb,len(userdb),len(userdbs),len(json.dumps(userdb).encode()))
        self.socket_send(userdb,len(json.dumps(userdb).encode()),action='auth')
        datas = self.socket_recv()
        if int(datas) == 100:
            print(SERVER_MESSAGE.get(int(datas)))
            return True
        else:
            print(SERVER_MESSAGE.get(int(datas)))
            exit()



    def socket_send(self, data, total_size,action='boj',**kwargs):
        header_dic = {
            'action':action,
            'total_size': total_size,

        }
        header_dic.update(kwargs)
        # print(header_dic)
        header_json = json.dumps(header_dic).encode('utf-8')

        self.sock.send(struct.pack('i', len(header_json)))

        self.sock.send(header_json)

        if header_dic['action'] == 'put':
            pg = self.progress(header_dic['total_size'])
            pg.__next__()

            with open(data, 'rb') as f:
                for line in f:
                    self.sock.send(line)
                    try:
                        percent = pg.send(len(line))
                        # print(int(percent))
                    except StopIteration:print('\t100%')

                else:
                    # print('[%s]文件正在上传!' % os.path.basename(data))
                    return

        data = json.dumps(data).encode('utf-8')
        self.sock.send(data)

    def socket_recv(self):
        # 收包头长度
        header_len = self.sock.recv(4)  # 包头大小为4,里面传送的为完整的包头长度
        # print(header_len,type(header_len))
        if not header_len:
            print(SERVER_MESSAGE.get(0))
            exit()

        head_len = struct.unpack('i', header_len)[0]


        head_bytes = self.sock.recv(head_len)  # 按照发送的包头长度收取包头
        header_dic = json.loads(head_bytes.decode('utf-8'))  # 取出完整包头数据

        total_size = header_dic.get('total_size')
        data = b''
        recv_size = 0

        while recv_size < total_size:
            piece_data = self.sock.recv(1024)
            data += piece_data
            recv_size += len(piece_data)
        data = json.loads(data.decode())

        return data

    def length(self,args):
        '''
        此对象只用于判读用户输入是否为Key,Vuals的形式,不可有多余的参数
        :param args: 用户输入的数据
        :return:
        '''
        if  not len(args) == 2:
            print('%s,%s'%(SERVER_MESSAGE[103],SERVER_MESSAGE[102]))
            return
        else:return True

    def progress(self,total):
        received_size = 0
        current_percent = 0
        while received_size < total:
            if int((received_size / total) * 20) > current_percent:
                print('#', end='', flush=True)
                current_percent = int((received_size / total) * 20)
            new_size = yield current_percent
            received_size += new_size

    def transmit(self):
        if self.authentication():
            print('SoarFTP... '.rjust(36,'>'))
            print("\nEnter 'exit' to exit!\n")
            while True:
                cmd = input('%s > '%self.args.user)
                if not cmd:continue
                if cmd == 'exit':break
                cmd_list = cmd.split()
                if hasattr(self,'_%s'%cmd_list[0]):
                    getattr(self,'_%s'%cmd_list[0])(cmd_list)
                else:print(SERVER_MESSAGE.get(99))
                continue

    def _put(self,args):
        cmd = args[0]
        filename = args[1]
        up_dir=[]
        try:
            if args[2]:
                up_dir.append(args[2])
        except IndexError:pass
        # filepath = os.path.isfile(filename)
        # if up_dir:
        #     if os.path.isdir(up_dir):    #判读是否存在要上传的文件夹
        #         if not os.path.isfile(filename):
        #             print('file:%s is not exists' % filename)
        #             return
        #         else:
        #             filesize = os.path.getsize(filename)
        #     else:
        #         print('不存在的目录')
        #         return
        if not os.path.isfile(filename):
            print('file:%s is not exists' % filename)
            return
        else:
            filesize = os.path.getsize(filename)

        self.socket_send(filename,filesize,action=cmd,filename=os.path.basename(filename),updir=up_dir)
        # int = self.socket_recv()
        print(SERVER_MESSAGE.get(self.socket_recv()))
        # print('1.给socket_send函数了')
        # head_dic = {'cmd': cmd, 'filename': os.path.basename(filename), 'filesize': filesize}

    def _ls(self,args):
        cmd = args[0]
        file_path=''
        try:
            if args[1]:
                file_path = args[1]
        except IndexError: pass
        self.socket_send(args,len(args),action=cmd,)
        da = self.socket_recv()   #打印服务端返回结果

        # print('>>>>>>>',da,type(da))
        if type(da) is int:print(SERVER_MESSAGE[da])
        else:
            for i in da:
                print('\t%s' % i)

    def _rm(self,args):
        '''
        for 循环判断是否需要删除目录,如果不存在'-r'则进行判断是否存在要删除的文件
        :param args: 用户输入的数据
        :return:
        '''
        for i in args:
            if i == '-r':
                print('正在执行删除目录操作,只能删除空目录!')
                self.socket_send(args,len(args),action=args[0])
                res = self.socket_recv()
                if res == 110:
                    print(SERVER_MESSAGE[res])
                    return
                else:
                    print(SERVER_MESSAGE[res])
                    return

        if self.length(args):
            # print(args)
            self.socket_send(args,len(args),action=args[0])
            res = self.socket_recv()
            if res == 110 :pass
            else:print(SERVER_MESSAGE[res])

    def _mkdir(self,args):
        # print('mkdir执行 ',args)
        if self.length(args):
            if re.search(r'\/',args[1]):
                print('创建多及目录需要用门"mkdirs"')
                return
            self.socket_send(args,len(args),action=args[0])
            res = self.socket_recv()
            if res == 110 :pass
            else:print(SERVER_MESSAGE[res])

    def _mkdirs(self,args):
        pass

    def _get(self,args):
        print('get 命令准备执行',args)
        if self.length(args):
            self.socket_send(args,len(args),action=args[0])
        # res = self.socket_recv()
        # if res == 110 :pass
        # else:print(SERVER_MESSAGE[res])



if __name__ == '__main__':
    ftp = FtpClient()
    ftp.transmit()




