#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'

import pymysql
import os

db = pymysql.connect("47.110.226.117", "build", "build@117", "build", use_unicode=True, charset="utf8")
# db = pymysql.connect("120.27.21.176", "root", "zjzy@123", "build", use_unicode=True, charset="utf8")
cursor = db.cursor()
sql = """select id from dpi_netsafetyplatform where wname='%s' """
sql_type = """insert into dpi_protocoltype (typeName, code, status, platformCode_id) values ('%s', '%s', 0, %s)"""
sql_app = """insert into dpi_protocolapplication (appName, code, status, platformCode_id, typeCode_id) VALUES ('%s', '%s', 0, %s, %s)"""
path = os.path.dirname(os.path.abspath(__file__))
path_qy = os.path.join(path, 'wa')
pt = os.listdir(path_qy)
for i in pt:
    cursor.execute(sql % i)
    t_d = cursor.fetchone()[0]
    wapt = os.path.join(path_qy, i)
    for j in os.listdir(wapt):
        with open(os.path.join(wapt, j), 'r', encoding='gbk') as fp:
            data = fp.readlines()
            cursor.execute(sql_type % (j[:-4], data[0].replace('\n', '').split('\t')[0], t_d))
            db.commit()
            cursor.execute("""select id from dpi_protocoltype where typeName='%s' and platformCode_id=%s""" % (j[:-4], t_d))
            type_ = cursor.fetchone()
            if type_:
                type_id = type_[0]
                for j_b in data[1:]:
                    jb = j_b.replace('\n', '').split('\t')
                    cursor.execute(sql_app % (jb[1], jb[0], t_d, type_id))
                    db.commit()
db.close()