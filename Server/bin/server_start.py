#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/11/8 13:21
# @Author  : Tiancc
# @Site    : 
# @File    : start.py
# @Software: PyCharm

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'src'))
import main

def choose():
    dicts ='''
        1:创建用户
        2:运行FTP Server
        9:退出
    '''
    print(dicts)

if __name__ == '__main__':
    u_choose={
        '1':main.FtpServerr.create,
        '2':main.FtpServerr,
        '9':exit
    }
    while True:
        choose()
        _input=input('选择序号>: ').strip()
        if _input not in u_choose:continue
        # elif _input == 2:
        u_choose[_input]()
