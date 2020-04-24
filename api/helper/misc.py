# coding:utf-8
import inspect
import os
import sys
from appack.models import advertising
import logging,hashlib
log = logging.getLogger(__name__)

__author__ = 'xcma'


def ABSpath():
    """获取当前的绝对路径"""
    ABSPATH = os.path.abspath(sys.argv[0])
    ABSPATH = os.path.dirname(ABSPATH)+'/api/lib/'
    return ABSPATH

def getadvertising(type=None,location=None):
    data = advertising.objects.filter(type=type,location=location).values()
    return data


def getFuncCalled():
    """
    获取当前方法被调用路径,从1开始，因为0是自己，不能被用作公共方法
    :return:
    """
    src = inspect.stack()
    info = []
    for i in range(1, len(src)):
        func_name = src[i][3]
        func_path = src[i][1]
        func_line = src[i][2]
        if not func_name.count('<') and not func_path.count('python2.7'):
            called_func_info = [func_name, func_line, func_path]
            info.append(called_func_info)
    return info[1]

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

def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False