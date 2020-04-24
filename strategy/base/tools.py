#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
import inspect
import shlex
import os
import time
import hashlib
import subprocess
import pathlib
import logging
from dss.Serializer import serializer
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import Group
from strategy.conf.path import get_path_day_time, out_base_path


log = logging.getLogger(__name__)

def authentication(request):
    """
    登录认证方法
    :param request:
    :return:
    """
    authent = 400
    if request.user.is_authenticated:
        log.debug('current_user[{}] operation {} '.format(request.user,get_func_called()))
        current_user_set = request.user
        current_group_set = current_user_set
        if not request.user.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
        authent = 400

        if '第三方' not in str(current_group_set) or request.user.is_superuser:
            authent = 200
        log.debug('user:{},group:{},authentication:{}'.format(request.user,current_group_set,authent))
        return authent
    if authent !=200:
        log.debug('render')
        return render(request, 'appack/autherror.html', {
            'message': {'msg': '权限不足'}
        })

def get_func_called():
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


def response_as_json(data, foreign_penetrate=False):
    jsonString = serializer(data=data, output_type="json", foreign=foreign_penetrate)
    response = HttpResponse(
            jsonString,
            content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def JsonResponse(data, code=200, foreign_penetrate=False, **kwargs):
    data = {
        "code": code,
        "msg": "成功",
        "data": data,
    }
    return response_as_json(data, foreign_penetrate=foreign_penetrate)

def JsonResponseori(data,foreign_penetrate=False):
    return response_as_json(data, foreign_penetrate=foreign_penetrate)


def JsonError(error_string="", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


def del_file_single(path):
    """只删除指定目录下的文件，子文件夹中的文件不删除"""
    log.debug('del_file：{}'.format(path))
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if not os.path.isdir(c_path):
            os.remove(c_path)


def is_have_file(path_name):
    '这个路径 是否存在，只能是路径'
    log.debug('判断目录是否存在：{}'.format(path_name))
    try:
        res = os.path.exists(path_name)
        log.debug('判断目录是否存在结果：{}'.format(res))
        return res
    except Exception as e:
        log.error(e)


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


def executionShell(cmdstring, cwd=None, timeout=None, shell=True):

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


def getProjectGitTag(project_path):
    """
    git 代码获取
    :param project_path:
    :return:
    """
    tag = "git describe --always --tags"
    commit_code = 'git rev-parse HEAD'
    data = []
    for cmd in [tag,commit_code]:
        res = executionShell(cmd,project_path)
        data.append(res)
    log.debug('project:{},当前tag及commit_code:{}'.format(project_path,data))
    return data


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


def time_stamp():
    '返回时间戳'
    return int(time.time())


def cps(old,new):
    """
    复制文件
    :param old:
    :param new:
    :return:
    """
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


def mv(old,new):
    """
    移动文件
    :param old:
    :param new:
    :return:
    """
    try:
        mkdir(new)
        cmd = 'mv {} {}'.format(old,new)
        log.debug('移动:{}'.format(cmd))
        return executionShell(cmd)
    except Exception as e:
        raise e


def del_file(path):
    """递归删除指定路径下所有文件，包括子文件夹文件，dir不删除"""
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


def get_now_time(sw=''):
    if sw:
        format = "%Y-%m-%d %H:%M:%S"
    else:
        format = "%Y%m%d%H%M%S"

    struct_time=time.strftime(format, time.localtime(time.time()))
    return struct_time


def compression(pack_type, dev_model, superd_version, package_contains_path, sw, work_path, source_save_path=''):
    """
    打包并压缩，移动到包存放路径

    :param pack_type:
    :param dev_model:
    :param superd_version:
    :param package_contains_path:
    :param sw:
    :param source_save_path:
    :return:
    """
    '打包并且压缩，移动到包存放路径'
    tarname = ''
    package_save_path_name = ''
    day_time_for_name = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    package_path = 'package/{}'.format(get_path_day_time())
    save_package_path = out_base_path + package_path
    dir_name = package_contains_path
    dev_model = dev_model.replace('-', '_')
    is_ok = False
    try:
        if pack_type == 'gzip':
            if sw == 'superd':
                # 如果是shell版本加载器，则需要将版本号中的横线替换成下划线，因为shell脚本不识别横线。
                if 'sapi' not in str(dir_name):
                    superd_version = superd_version.replace('-', '.')
                tarname = 'pgpack.{}.{}_{}.tar.gz'.format(dev_model, day_time_for_name, superd_version)
            else:
                tarname = 'sapiloaderpack.{}.{}_{}.tar.gz'.format(dev_model, day_time_for_name, superd_version)
            cmd = 'tar zcvf {} {}'.format(tarname, dir_name)
        elif pack_type == 'lzma':
            if sw == 'superd':
                tarname = 'pgpack.{}.{}_{}.tar.lzma'.format(dev_model, day_time_for_name, superd_version)
            else:
                tarname = 'sapiloaderpack.{}.{}_{}.tar.lzma'.format(dev_model, day_time_for_name, superd_version)
            cmd = f'sudo tar -c -lzma -f {tarname} {dir_name}'
        else:
            log.warning(f'没有获取到指定的压缩方式 {pack_type}')
            return False, False, False, False

        log.debug('开始打包:{},name:{}'.format(cmd, tarname))
        executionShell(cmd, work_path)
        source_path_name = work_path + tarname

        log.debug('开始移动包到保存路径：{}，{}'.format(source_path_name, save_package_path))
        if is_have_file(source_path_name):
            try:
                mv(source_path_name, save_package_path)
                if sw == 'superd':
                    del_file(work_path)
                    log.debug('清理工作路径')
                log.debug('包名称：{}'.format(tarname))
                is_ok = True
            except Exception as e:
                is_ok = False
                log.error(e)
        else:
            is_ok = False
            log.error(source_path_name)

        package_save_path_name = save_package_path + tarname
        return is_ok, tarname, package_path, package_save_path_name
    except Exception as e:
        log.error(e)
        return is_ok, tarname, package_path, package_save_path_name


def monitorLog(cmd,timeout):
    """
    使用cmd 命令读取文件内容 每次一行
    :param cmd: 要执行的命令
    :param timeout: 等待时长
    :return:
    """
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