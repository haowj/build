#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'

from pypinyin import pinyin, lazy_pinyin
import time
import jieba
import pymysql
import os


# db = pymysql.connect("47.110.226.117", "build", "build@117", "build", use_unicode=True, charset="utf8")
db = pymysql.connect("120.27.21.176", "root", "zjzy@123", "build", use_unicode=True, charset="utf8")
cursor = db.cursor()

path = os.path.dirname(os.path.abspath(__file__))
path_qy = os.path.join(path, 'wa', '派博')
pt = os.listdir(path_qy)
ns_pb = os.path.join(path_qy, '虚拟身份.txt')
with open(ns_pb, 'r', encoding='gbk') as fp:
    while fp:
        data = fp.readline()
        if data == '' or data is None:
            break
        tmp = data.split()
        if tmp[0] == '多玩YY':
            tmp[0] = 'YY语音'
        if tmp[0] == '网易POPO':
            tmp[0] = 'POPO网易泡泡'
        if tmp[0] == '穿越火线':
            tmp[0] = 'CF(穿越火线）'
        if tmp[0] == '暗黑3':
            tmp[0] = '暗黑破坏神3'
        if tmp[0] == '126邮箱':
            tmp[0] = '网易126邮箱'
        if tmp[0] == '163邮箱':
            tmp[0] = '网易163邮箱'

        if tmp[0] == '新华论坛':
            tmp[0] = '新华网论坛'
        if tmp[0] == '凤凰社区':
            tmp[0] = '凤凰网论坛'
        if tmp[0] == '京东商城':
            tmp[0] = '京东'
        if tmp[0] == '拍拍网':
            tmp[0] = '腾讯购物（拍拍网）'
        if tmp[0] == '淘宝网':
            tmp[0] = '淘宝'

        if tmp[0] == '7天连锁酒店':
            tmp[0] = '7天'
        if tmp[0] == '携程网':
            tmp[0] = '携程'
        if tmp[0] == '微信':
            tmp[0] = '微信(腾迅推出的手机聊天工具)'
        if tmp[0] == '米聊':
            tmp[0] = '米聊(小米推出的手机聊天工具)'
        if tmp[0] == 'KC网络电话':
            tmp[0] = 'KC'

        if tmp[0] == '搜Q':
            tmp[0] = 'SOQ'
        if tmp[0] == '卡萌':
            tmp[0] = '卡盟(KAMUN)'
        if tmp[0] == 'UU':
            tmp[0] = 'UU通'
        if tmp[0] == '天涯':
            tmp[0] = '天涯论坛'
        if tmp[0] == '猫扑':
            tmp[0] = '猫扑论坛'



        cursor.execute("""select * from dpi_enterprisecoding where name = '%s'""" % tmp[0])
        ids = cursor.fetchone()
        if ids:
            if tmp[0] == 'YY语音':
                tmp[0] = '多玩YY'

            if tmp[0] == 'POPO网易泡泡':
                tmp[0] = '网易POPO'
            if tmp[0] == 'CF(穿越火线）':
                tmp[0] = '穿越火线'
            if tmp[0] == '暗黑破坏神3':
                tmp[0] = '暗黑3'
            if tmp[0] == '网易126邮箱':
                tmp[0] = '126邮箱'
            if tmp[0] == '网易163邮箱':
                tmp[0] = '163邮箱'

            if tmp[0] == '新华网论坛':
                tmp[0] = '新华论坛'
            if tmp[0] == '凤凰网论坛':
                tmp[0] = '凤凰社区'
            if tmp[0] == '京东':
                tmp[0] = '京东商城'
            if tmp[0] == '腾讯购物（拍拍网）':
                tmp[0] = '拍拍网'
            if tmp[0] == '淘宝':
                tmp[0] = '淘宝网'

            if tmp[0] == '7天':
                tmp[0] = '7天连锁酒店'
            if tmp[0] == '携程':
                tmp[0] = '携程网'
            if tmp[0] == '微信(腾迅推出的手机聊天工具)':
                tmp[0] = '微信'
            if tmp[0] == '米聊(小米推出的手机聊天工具)':
                tmp[0] = '米聊'
            if tmp[0] == 'KC':
                tmp[0] = 'KC网络电话'

            if tmp[0] == 'SOQ':
                tmp[0] = '搜Q'
            if tmp[0] == '卡盟(KAMUN)':
                tmp[0] = '卡盟'
            if tmp[0] == 'UU通':
                tmp[0] = 'UU'
            if tmp[0] == '天涯论坛':
                tmp[0] = '天涯'
            if tmp[0] == '猫扑论坛':
                tmp[0] = '猫扑'

            cd = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""insert into dpi_appprocode (ns_appname, ns_code, vi_ec_id, platformCode_id, user, create_time, update_time) VALUES ('%s', '%s', %s, 2, 'auto create', '%s', '%s')""" % (tmp[0], tmp[1], ids[0], cd, cd))
            db.commit()
        else:
            print(tmp[0])
# for i in pt:
    # cursor.execute("""select id from dpi_netsafetyplatform where wname='%s' """ % i)
    # t_d = cursor.fetchone()
    # if t_d is None:
    #     code = ''.join(lazy_pinyin(i)).upper()
    #     cursor.execute("""insert into dpi_netsafetyplatform (wname, code, status) VALUES ('%s', '%s', '0')""" % (i, code))
    #     db.commit()
    #     cursor.execute("""select id from dpi_netsafetyplatform where wname='%s' """ % i)
    #     t_d = cursor.fetchone()[0]
    # else:
    #     t_d = t_d[0]
    #
    # print(i)