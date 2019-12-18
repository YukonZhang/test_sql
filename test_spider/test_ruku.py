# -*- coding: utf-8 -*-
import cx_Oracle
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

conn = cx_Oracle.connect('crawler/crawler@168.61.2.2:1521/servdb')
cur = conn.cursor()

cur
