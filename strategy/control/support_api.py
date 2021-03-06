#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
import requests
import logging
import hashlib
log = logging.getLogger(__name__)


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


class supportApi:

    def __init__(self):
        self.url = ''
        self.para = ''

    def getUrl(self,path):
        self.url = 'http://support.superhcloud.com{}'.format(path)
        return self.url

    def getPara(self,**kwargs):
        self.para = kwargs
        sign = getSign(self.para)
        self.para['sign']=sign
        return self.para

    def get(self,**kwargs):
        try:
            self.getPara(**kwargs)
            data = requests.get(self.url, params=self.para)
            try:
                res = data.json()
            except:
                res = {}
                log.error(data.text())
            return res
        except Exception as e:
            log.error(e)


    def addNewSVersionInfo(self,**kwargs):
        self.getUrl('/api/addNewSVersionInfo')
        res = self.get(**kwargs)
        return res

    def addoem(self,**kwargs):
        self.getUrl('/api/addOem')
        res = self.get(**kwargs)
        return res

    def adddev_model(self,**kwargs):
        self.getUrl('/api/addDev_model')
        res = self.get(**kwargs)
        return res

sp_api =supportApi()