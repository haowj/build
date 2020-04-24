#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'

import pymysql
import os
import time

# db = pymysql.connect("47.110.226.117", "build", "build@117", "build", use_unicode=True, charset="utf8")
db = pymysql.connect("120.27.21.176", "root", "zjzy@123", "build", use_unicode=True, charset="utf8")

cursor = db.cursor()

path = os.path.dirname(os.path.abspath(__file__))
path_qy = os.path.join(path, 'qy')
path_sf = os.path.join(path, 'sf')
path_yw = os.path.join(path, 'yw')
file_qy = os.listdir(path_qy)
file_sf = os.listdir(path_sf)
file_yw = os.listdir(path_yw)


for i_sf in file_sf:
    sql = """insert into dpi_identitytypecoding (identityType, en, code, explaines, user, create_time, update_time) values ('%s', '%s', '%s', '%s', 'auto create', '%s', '%s')"""
    path_file_sf = os.path.join(path_sf, i_sf)
    data = open(path_file_sf, 'r', encoding='utf-8')
    for i_d in data:
        if '\n' in i_d:
            i_d = i_d.replace('\n', '')
        elif '\r\n' in i_d:
            i_d = i_d.replace('\r\n', '')
        else:
            pass
        tem = i_d.split('-')
        if '\ufeff' in tem[0]:
            tem[0] = tem[0].replace('\ufeff', '')
        if len(tem) == 4:
            cd = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(sql % (tem[0], tem[1], tem[2], tem[3], cd, cd))
        else:
            print('%s插入失败, 数据长度不够' % tem[0])
        db.commit()


for i_yw in file_yw:
    sql = """insert into dpi_businesstype (businessType, en, code, user, create_time, update_time) values ('%s', '%s', '%s', 'auto create', '%s', '%s')"""
    path_file_yw = os.path.join(path_yw, i_yw)
    data = open(path_file_yw, 'r', encoding='utf-8')
    for i_d in data:
        if '\n' in i_d:
            i_d.replace('\n', '')
        elif '\r\n' in i_d:
            i_d.replace('\r\n', '')
        else:
            pass
        tem = i_d.split('-')
        if '\ufeff' in tem[0]:
            tem[0] = tem[0].replace('\ufeff', '')
        if len(tem) == 3:
            cd = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(sql % (tem[0], tem[1], tem[2], cd, cd))
        elif len(tem) == 2:
            cd = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(sql % (tem[0], '', tem[1], cd, cd))
        db.commit()

sql = """select * from dpi_businesstype"""

cursor.execute(sql)
data = cursor.fetchall()
tm = dict()
for i in data:
    tm[i[1]] = i[0]

for i_qy in file_qy:
    sql = """insert into dpi_enterprisecoding (name, en, code, typeCode_id, user, create_time, update_time) values ('%s', '%s', '%s', %s, 'auto create', '%s', '%s')"""
    if i_qy[:-4] in tm:
        num_id = tm[i_qy[:-4]]
    else:
        print('%s没有找到对应的业务类型, 本次数据插入不执行' % i_qy)
        continue
    path_file_qy = os.path.join(path_qy, i_qy)
    data = open(path_file_qy, 'r', encoding='utf-8')
    for i_d in data:
        if '\n' in i_d:
            i_d = i_d.replace('\n', '')
        elif '\r\n' in i_d:
            i_d = i_d.replace('\r\n', '')
        else:
            pass
        tem = i_d.split('-')
        if '\ufeff' in tem[0]:
            tem[0] = tem[0].replace('\ufeff', '')
        if len(tem) == 3:
            cd = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(sql % (tem[0], tem[1], tem[2], num_id, cd, cd))
        elif len(tem) == 2:
            cd = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(sql % (tem[0], '', tem[1], num_id, cd, cd))
        db.commit()

db.close()