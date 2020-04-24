# coding:utf-8
import inspect
import os
import sys
import logging,hashlib
log = logging.getLogger(__name__)

__author__ = 'xcma'


def ABSpath():
    """获取当前的绝对路径"""
    ABSPATH = os.path.abspath(sys.argv[0])
    ABSPATH = os.path.dirname(ABSPATH)+'/api/lib/'
    return ABSPATH


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

def delFile(filepath):
    if os.path.exists(filepath):
        # 删除文件，可使用以下两种方法。
        os.remove(filepath)
        log.debug('删除文件：{} 成功。'.format(filepath))

def get_md5_big(file_path):
    log.debug('md5_path:{}'.format(file_path))
    if os.path.isfile(file_path):
        f = open(file_path,'rb')
        md5_obj = hashlib.md5()
        while True:
            d = f.read(8096)
            if not d:
              break
            md5_obj.update(d)
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
    else:
        md5 = 'file not found'
        log.error('file not found:{}'.format(file_path))
    log.debug('md5:{}'.format(md5))
    return md5

def del_file_single(path):
    """只删除指定目录下的文件，子文件夹中的文件不删除"""
    log.debug('del_file：{}'.format(path))
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if not os.path.isdir(c_path):
            os.remove(c_path)
def mkdir(path,is_del=False):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    try:
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            log.debug('新建目录成功：{}'.format(path))
        else:
            # 如果目录存在则不创建，并提示目录已存在
            log.debug(path + ' 目录已存在')
            if is_del:
                del_file_single(path)
                log.debug('已删除路径下文件，未删除路径下文件夹')
        return True
    except:
        return False
