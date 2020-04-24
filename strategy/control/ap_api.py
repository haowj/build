#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
import requests
import logging
import time
import hashlib
import urllib3
import json
from appack.helper.misc import base64Encode
log = logging.getLogger(__name__)

urllib3.disable_warnings()
http = urllib3.PoolManager()

# 设备管理系统服务url
ap_url = 'https://ap.superhcloud.com'

# kong地址
# kong_domain = 'http://172.16.65.131'
kong_domain = 'http://47.99.148.245'

release_domain = 'http://ap.superhcloud.com/'


def getSign(param):
    """md5($mobile.$mac.'pythonapi')"""
    ps = ''
    pdict = sorted(param.items(), key=lambda param:param[0], reverse=False)
    log.debug(pdict)
    for i in pdict:
        ps +='{}={}'.format(i[0].lower(),i[1])
    cmd = 'pythonapi{}'.format(ps)
    log.debug('str:{}'.format(cmd))
    sign = hashlib.md5(cmd.encode('utf-8')).hexdigest()
    log.debug(sign)
    return sign

def check_sign(request):
    para = request.GET
    para_dict = {}
    para_sign = ''
    for k, v in para.items():
        if k != 'sign':
            para_dict[k] = v
        else:
            para_sign = v
    sign = getSign(para_dict)
    if sign == para_sign:
        log.debug('鉴权成功')
        return True
    log.debug('鉴权失败：{}={}?{}'.format(sign, para_sign, sign == para_sign))
    return False


class apApi:
    """
    添加设备厂商
    https://ap.superhcloud.com/papi/add-oem?name=$name&code=$code

    添加设备型号
    https://ap.superhcloud.com/papi/add-oem?cate_name=$cate_name&model_name=$model_name&sales_name=$sales_name&oem_name=$oem_name

    cate_name 设备分类
    model_name 设备型号
    sales_name 设备厂商
    oem_name 生产商
    """
    def __init__(self):
        self.domain = kong_domain
        self.para = {}

    def getUrl(self,domain='',path=''):
        if not domain:
            self.url = '{}{}'.format(self.domain,path)
        else:
            self.url = '{}{}'.format(domain, path)
        return self.url

    def getPara(self, **kwargs):
        para = kwargs
        para['_time']=int(time.time())
        para['_appname']='papi'
        sign = getSign(para)
        para['_sign']=sign
        log.debug(para)
        self.para = para
        return self.para

    def getParaDict(self,para):
        para['_time'] = int(time.time())
        para['_appname'] = 'papi'
        sign = getSign(para)
        para['_sign'] = sign
        self.para=para
        return self.para


    def get(self,para={},**kwargs):
        try:
            if para:
                self.getParaDict(para)
            else:
                self.getPara(**kwargs)
            # data = http.request('GET', self.url, fields=self.para)
            data = requests.get(self.url, params=self.para,verify=False)
            try:
                log.debug(data.url)
                res = data.json()
                log.debug(res)
            except:
                res = {}
                log.error(data.text())
            return res
        except Exception as e:
            log.error(e)

    def post(self,para,base64=False):
        """
        requests.post(url, data=d):请求头中的Content-Type字段已设置为application/x-www-form-urlencoded

        requests.post(url, json=json.dumps(d)):请求头的Content-Type设置为application/json

        :param para:
        :return:
        """
        try:
            self.getParaDict(para)
            if base64:
                for k,v in self.para.items():
                    base64v =base64Encode(v)
                    self.para[k]=base64v
            data = requests.post(self.url, json=json.dumps(self.para),verify=False)
            try:
                log.debug(data.url)
                log.debug(data.headers)
                res = data.json()
                log.debug(res)

            except:
                res = {}
                log.error(data.text())
            return res
        except Exception as e:
            log.error(e)

    def post_http(self,domain,path,para_json):
        import http.client
        res={}
        params = json.dumps(para_json)
        log.debug(params)

        headers = {"Content-type": "text/json", "Accept": "text/plain"}
        conn = http.client.HTTPConnection(domain,80)
        conn.timeout = 5
        conn.request('POST', path, params, headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode('utf-8'))
        conn.close()
        try:
            # 1:查询到鉴权且已授权 0:查询到鉴权且未授权或未查询到
            log.debug('rauth:{}'.format(data))
            RESULT = data['RESULT']
            if RESULT == 'Success':
                res['code'] = 200
                res['msg'] = ''
        except:
            res['code'] = 400
            res['msg'] = '参数异常，请确认参数'
        return res

    def add_oem(self,**kwargs):
        self.getUrl('/papi/add-oem')
        res = self.get(**kwargs)
        return res

    def add_dev_model(self,**kwargs):
        self.getUrl('/papi/add-model')
        res = self.get(**kwargs)
        return res

    def release_pg(self,para):
        self.getUrl(release_domain,'apmodel/loader-plug')
        res=self.get(para)
        return res

    def release_shell_pg(self,para):
        self.getUrl(release_domain,'apmodel/plugin')
        res = self.get(para)
        return res

ap_api = apApi()