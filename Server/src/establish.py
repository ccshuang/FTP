#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/11/9 11:05
# @Author  : Tiancc
# @Site    : 
# @File    : establish.py
# @Software: PyCharm

class Create:
    def __init__(self,name,pwd):
        self.name = name
        self.pasd = pwd
        print(self.name,self.pasd)

    @staticmethod
    def create():
        while True:
            print("\n'exit' 退出\n")
            u_input = input('账号>: ').strip()
            if not u_input:continue
            elif u_input == 'exit':break

            u_pasd = input('pasword>: ').strip()
            if not u_pasd: continue
            u_pasds = input('确认>: ').strip()
            if not u_pasd == u_pasds:
                print('两次密码输入不匹配,重新创建.')
                continue
            else:print('OK')


