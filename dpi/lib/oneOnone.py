#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'

from pypinyin import pinyin, lazy_pinyin
import time
import jieba
import pymysql
import os

db = pymysql.connect("47.110.226.117", "build", "build@117", "build", use_unicode=True, charset="utf8")
# db = pymysql.connect("120.27.21.176", "root", "zjzy@123", "build", use_unicode=True, charset="utf8")
cursor = db.cursor()
sql = """select id from dpi_netsafetyplatform where wname='%s' """
sql_type = """insert into dpi_protocoltype (typeName, code, status, platformCode_id) values ('%s', '%s', 0, %s)"""
sql_app = """insert into dpi_protocolapplication (appName, code, status, platformCode_id, typeCode_id) VALUES ('%s', '%s', 0, %s, %s)"""
sql_ana = """select * from dpi_enterprisecoding where name = '%s'"""
sql_ono = """select * from dpi_enterprisecoding where name like '%s'"""
sql_ini = """insert into dpi_appprocode (ns_appname, ns_code, vi_ec_id, platformCode_id, user, create_time, update_time) VALUES ('%s', '%s', %s, 1, 'auto create', '%s', '%s')"""
path = os.path.dirname(os.path.abspath(__file__))
path_qy = os.path.join(path, 'wa')
pt = os.listdir(path_qy)

for i in pt:
    cursor.execute(sql % i)
    t_d = cursor.fetchone()
    if t_d is None:
        code = ''.join(lazy_pinyin(i)).upper()
        cursor.execute("""insert into dpi_netsafetyplatform (wname, code, status) VALUES ('%s', '%s', '0')""" % (i, code))
        db.commit()
        cursor.execute(sql % i)
        t_d = cursor.fetchone()[0]
    else:
        t_d = t_d[0]
    wapt = os.path.join(path_qy, i)
    for j in os.listdir(wapt):
        with open(os.path.join(wapt, j), 'r', encoding='gbk') as fp:
            data = fp.readlines()

            for j_b in data[1:]:
                jb = j_b.replace('\n', '').split('\t')
                cursor.execute(sql_ana % jb[1])

                da = cursor.fetchone()
                # if da is None:
                #     seg = list(jieba.cut(jb[1]))
                #     print(seg)
                #     cursor.execute("""select * from dpi_enterprisecoding where name like '%%%s%%'""" % seg[0])
                #     t = cursor.fetchall()
                #     print(t)
                if da:
                    cd = time.strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute(sql_ini % (jb[1].replace(' ', ''), jb[0], da[0], cd, cd))
                    db.commit()
                    # print('%s==========%s======%s' % (jb[1].replace(' ', ''), jb[0], da[0]))
                    # pass
                # else:
                #     try:
                #         seg = list(jieba.cut(jb[1]))
                #         cursor.execute("""select * from dpi_enterprisecoding where name like '%%%s%%'""" % seg[0])
                #         t = cursor.fetchall()
                #         print('%s================%s' % (''.join(seg), '-'.join([i[1] for i in t])))
                #     except IndexError:
                #         print(jb[1], j)
                #         print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                #         break
db.close()


class InsertIData:
    def __init__(self, ids):
        """
        ids : 1-测试库数据导入， 2-生产库数据导入
        :param ids:
        """
        self.file = None
        self.path = None
        if ids == 1:
            self.db = pymysql.connect("120.27.21.176", "root", "zjzy@123", "build", use_unicode=True, charset="utf8")
        elif ids == 2:
            self.db = pymysql.connect("47.110.226.117", "build", "build@117", "build", use_unicode=True, charset="utf8")
        self.cursor = self.db.cursor()

    def get_file_path(self, file = None):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(self.path, 'wa')
        if file is None:
            self.file = os.listdir(self.path)
        else:
            self.file = list(file)

    def insert_into_data(self, file = None):
        sql_path = """select id from dpi_netsafetyplatform where wname='%s' """
        self.get_file_path(file=file)
        for p_d in self.file:
            self.cursor.execute(sql_path % p_d)
            t_d = cursor.fetchone()
            if t_d is None:
                code = ''.join(lazy_pinyin(i)).upper()
                cursor.execute(
                    """insert into dpi_netsafetyplatform (wname, code, status) VALUES ('%s', '%s', '0')""" % (i, code))
                db.commit()
                cursor.execute("""select id from dpi_netsafetyplatform where wname='%s' """ % i)
                t_d = cursor.fetchone()[0]
            else:
                t_d = t_d[0]

            wapt = os.path.join(self.path, p_d)
            for j in os.listdir(wapt):
                with open(os.path.join(wapt, j), 'r', encoding='gbk') as fp:
                    data = fp.readlines()

                    for j_b in data[1:]:
                        jb = j_b.replace('\n', '').split('\t')
                        cursor.execute("""select * from dpi_enterprisecoding where name = '%s'""" % jb[1])

                        da = cursor.fetchone()

                        if da:
                            cd = time.strftime('%Y-%m-%d %H:%M:%S')
                            cursor.execute("""insert into dpi_appprocode (ns_appname, ns_code, vi_ec_id, platformCode_id, user, create_time, update_time) VALUES ('%s', '%s', %s, 1, 'auto create', '%s', '%s')""" % (jb[1].replace(' ', ''), jb[0], da[0], cd, cd))
                            db.commit()