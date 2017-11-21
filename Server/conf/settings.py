#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/11/9 11:36
# @Author  : Tiancc
# @Site    : 
# @File    : settings.py
# @Software: PyCharm

import os,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER_PWD = os.path.join(BASE_DIR,'db','user_pasd')
USER_CONF = os.path.join(BASE_DIR,'conf','user.cnf')
USER_HOME= os.path.join(BASE_DIR,'home')


HOST = '127.0.0.1'
PORT = 9007

# print(USER_PWD)
