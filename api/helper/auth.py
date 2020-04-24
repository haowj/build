# coding:utf-8
import hashlib
import logging
log = logging.getLogger(__name__)
from api.controller.dataToJson import *

__author__ = 'xcma'

from build.settings import SECRET_KEY

class authentication:

    def get_str_md5(self,string):
        md5 = hashlib.md5(string.encode('utf-8')).hexdigest()
        log.debug('字符串:{}，md5:{}'.format(string, md5))
        return md5

    def sign(self,timestamp):
        string = SECRET_KEY+timestamp
        sign = self.get_str_md5(string)
        return sign


    def auth(self,func):
        def inner():
            timestamp = request.GET.get('timestamp')
            sign = request.GET.get('sign')
            s_sign = self.sign(timestamp)
            if sign==s_sign:
                is_auth = 1
            else:
                is_auth = 0
            log.debug('鉴权：{}'.format(is_auth))
            if is_auth:
                func()
            else:
                JsonError('auth error')
        return inner