# coding:utf-8
import inspect
import os
import pathlib
import platform
import sys
import logging
import shlex
import subprocess
import time
import base64

log = logging.getLogger(__name__)
__author__ = 'xcma'
import datetime
from datetime import  date, timedelta
def getDatetimeToday():
        t = date.today()  #date类型
        dt = datetime.datetime.strptime(str(t),'%Y-%m-%d') #date转str再转datetime
        return dt

def getNowTime(sw=''):
    if sw:
        format = "%Y-%m-%d %H:%M:%S"
    else:
        format = "%Y%m%d%H%M%S"

    struct_time=time.strftime(format, time.localtime(time.time()))
    return struct_time

def getDatetimeYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday

def timeTotime(data):
    """
    ori：2018-04-30 00:00:00
    out：2018-4-16 21:32:32
    :param data:
    :return:
    """
    import time
    struct_time = time.strptime(str(data).strip(), "%Y-%m-%d %H:%M:%S")
    time = "{}-{}-{} {}:{}:{}".format(struct_time.tm_year, struct_time.tm_mon, struct_time.tm_mday, struct_time.tm_hour,
                                      struct_time.tm_min, struct_time.tm_sec)
    return time

def time_stamp():
    '返回时间戳'
    return int(time.time())

def timeToSigtime(data):
    """
    ori：2018-04-30 00:00:00
    out：2018-4-16
    :param data:
    :return:
    """
    import time
    struct_time = time.strptime(str(data).strip(), "%Y-%m-%d %H:%M:%S")
    time = "{}-{}-{}".format(struct_time.tm_year, struct_time.tm_mon, struct_time.tm_mday)
    return time

def getYesDayFormart():
    yesday = getDatetimeYesterday()
    yesday_formart = timeTotime(yesday)
    return yesday_formart
def getYesDaySignFormart():
    yesday = getDatetimeYesterday()
    yesday_formart = timeToSigtime(yesday)
    return yesday_formart


def get_day_nday_ago(date,n):
    "获取指定时间的前n天的日期"
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - timedelta(n)).split()
    return Date[0]

def compare_time( start_t, end_t):
    log.debug('start_t:{},end_t:{}'.format(start_t,end_t))
    s_time = time.mktime(time.strptime(start_t, '%Y-%m-%d %H:%M:%S'))  # get the seconds for specify date
    e_time = time.mktime(time.strptime(end_t, '%Y-%m-%d %H:%M:%S'))
    diff_time = int(e_time) - int(s_time)
    log.debug('form:start_t:{},end_t:{},diff_time:{}'.format(s_time,e_time,diff_time))
    if diff_time>600:
        return False
    return True

def get_nday_list(n):
    "获取今天的前n天的日期列表"
    import datetime
    before_n_days = []
    for i in range(1, n + 1)[::-1]:
        before_n_days.append(str(datetime.date.today() - datetime.timedelta(days=i)))
    return before_n_days

def getDayago(days):
    '获取指定天之前的时间'
    return str((datetime.datetime.now() - timedelta(days)).strftime("%Y-%m-%d %H:%M:%S"))

def is_have_file(path_name):
    '这个路径 是否存在，只能是路径'
    log.debug('判断目录是否存在：{}'.format(path_name))
    try:
        res = os.path.exists(path_name)
        log.debug('判断目录是否存在结果：{}'.format(res))
        return res
    except Exception as e:
        log.error(e)
def del_file(path):
    """递归删除指定路径下所有文件，包括子文件夹文件，dir不删除"""
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

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

def cp_normal(oldname,newname):
    cmd = 'cp -f {} {}'.format(oldname, newname)
    cmd_list = [cmd]
    try:
        for cmd in cmd_list:
            s = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            out = s.communicate()
            # log.debug('md5num:{}'.format(out))
            res = str(out[0]).split('/')[0].replace("'", '').strip()[1:]
            return out,res
    except Exception as e:
        log.error(e)
        raise e

def chmod_file(file_path):
    # 给文件赋执行权限  很重要！！！！
    if file_is_have(file_path):
        chmod_cmd = 'chmod a+x {}'.format(file_path)
        check_cmd = 'll {}'.format(file_path)
        log.debug('授权文件{}：开始,cmd:{}'.format(file_path,chmod_cmd))
        cmd_list = [chmod_cmd,check_cmd]
        for cmd in cmd_list:
            s = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            out = s.communicate()
            res = str(out[0]).split('/')[0].replace("'", '').strip()[1:]
        return True
    else:
        return False

def getCpath():
    return os.path.split(os.path.realpath(__file__))[0]

def ABSpath():
    """获取当前项目的绝对路径"""
    ABSPATH = os.path.abspath(sys.argv[0])
    ABSPATH = os.path.dirname(ABSPATH)
    return ABSPATH


import hashlib
def getMd5(file_path_name):
    log.debug('md5_path:{}'.format(file_path_name))
    try:
        m = hashlib.md5()
        n = 1024 * 10
        inp = open(file_path_name, 'rb')
        while True:
            buf = inp.read(n)
            if buf:
                m.update(buf)
            else:
                break
        md5=m.hexdigest()
        log.debug('md5:{}'.format(md5))
        return md5
    except Exception as e:
        log.error(e)
        return False

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

def get_str_md5(string):
    md5 = hashlib.md5(string.encode('utf-8')).hexdigest()
    log.debug('字符串:{}，md5:{}'.format(string,md5))
    return md5

def executionShell( cmdstring, cwd=None, timeout=None, shell=True):

    """
    执行一个SHELL命令
    封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
    参数:
        cwd: 到指定路径下，执行shell命令
        timeout: 超时时间，秒，支持小数，精度0.1秒
        shell: 是否通过shell运行
    """
    try:
        if shell:
            cmdstring_list = cmdstring
        else:
            cmdstring_list = shlex.split(cmdstring)
        p = subprocess.Popen(cmdstring_list,cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,bufsize=1,shell=shell)
        p.wait(timeout)
        data = []
        for line in iter(p.stdout.readline, b''):
            try:
                if len(line)>1:
                    try:
                        line = line.replace('\n','')
                    except:
                        pass
                    try:
                        line = line.decode('utf-8')
                    except:
                        pass
                    log.debug('{}'.format(line))
            except:
                log.warning('异常输出信息：{}'.format(line))
                pass
            finally:
                data.append (line)
        p.stdout.close()
        return data
    except Exception as e:
        log.error(e)
def monitorLog(cmd,timeout):
    line =''
    try:
        handle = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        handle.wait(timeout)
        try:
            line = handle.stdout.readline().strip()
            log.debug('data:{}'.format(line))
        except Exception as e:
            handle.kill()
            log.error(e)
        # 判断内容是否为空
    except Exception as e:
        log.error(e)
    return line
def is_linux_platfrom():
    if 'Linux' in platform.system():
        return 1
    return 0

def file_is_have(file_path):
    """
    path.exist()  检查路径是否存在
    path.is_file() 检查文件是否存在
    :param file_path:
    :return:
    """
    log.debug('开始检查目录：{}'.format(file_path))
    try:
        fp = str(file_path)
        path = pathlib.Path(fp)
        if path.exists():
            if path.is_file():
                log.debug('已找到路径:{}'.format(fp))
                return 1
        return 0
    except Exception as e:
        log.error(e)


def mv(old,new):
    try:
        mkdir(new)
        cmd = 'mv {} {}'.format(old,new)
        log.debug('移动:{}'.format(cmd))
        return executionShell(cmd)
    except Exception as e:
        raise e

def cp(old,new):
    if file_is_have(old):
        if not is_have_file(new):
            mkdir(new)
        cmd = 'cp {} {}'.format(old,new)
        log.debug('复制:{}'.format(cmd))
        executionShell(cmd)
        return True
    else:
        log.error('文件不存在：{}'.format(old))
        return False

def getProjectGitTag(project_path):
    tag = "git describe --always --tags"
    commit_code = 'git rev-parse HEAD'
    data = []
    for cmd in [tag,commit_code]:
        res = executionShell(cmd,project_path)
        data.append(res)
    log.debug('project:{},当前tag及commit_code:{}'.format(project_path,data))
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



def base64Encode(string):
    #转成bytes string
    bytesString = str(string).encode(encoding="utf-8")
    #base64 编码
    encodestr = base64.b64encode(bytesString)
    # print(encodestr)
    # print(encodestr.decode())
    log.debug(string)
    log.debug(encodestr.decode())
    return encodestr.decode()

def base64Decode(encodestr):
    #解码
    decodestr = base64.b64decode(encodestr)
    log.debug(encodestr)
    log.debug(decodestr.decode())
    return decodestr.decode()