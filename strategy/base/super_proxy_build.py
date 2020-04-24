#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
import logging
from strategy.base.tools import executionShell, time_stamp, time
from strategy.conf.path import proxy_client_project_path, out_base_path, out_proxy_data, \
    proxy_client_build_save_path, proxy_client_build_shell_path_name
from strategy.base.op_val import get_map_dev_model, mv_plug, get_build_is_complate, insert_into_build_log
from strategy.control.git_tool import clear_path, GitProcess


log = logging.getLogger(__name__)


def Build(dev_model, user):
    # 构建完成后，包存放的路径
    tag = '1.0'
    types = 'proxy'
    reason = 'auto'
    # 数据存储路径
    package_path = out_base_path + out_proxy_data + dev_model + '/'

    log.debug('start_build:{},tag:{},reason:{},user:{}'.format(dev_model,tag,reason,user))

    map_dev_model = get_map_dev_model(dev_model)

    # 获取最新反向代理最新代码
    git = GitProcess(proxy_client_project_path)
    git.init_project()

    clear_path(proxy_client_build_save_path,
               package_path,
               proxy_client_build_shell_path_name,
               tag)
    cmd = f'./cbuild.sh {map_dev_model}>{dev_model}_out.log 2>&1'
    log.debug('构建{}:{}，路径：{}'.format(types, cmd, proxy_client_project_path))
    build_data = executionShell(cmd, proxy_client_project_path, 1)

    insert_into_build_log(time_stamp=time_stamp(),
                          dev_model=dev_model,
                          user=str(user),
                          build_result=build_data,
                          build_tag=tag,
                          build_reason=reason,
                          build_status=400,
                          type=types)

    # 这里的dev_model 必须使用原始的，就是设备的正常型号而不是cbuild中写的，因为需要入库展示使用。
    num = 1
    while True:
        status = mv_plug(dev_model,
                           user,
                           tag,
                           reason,
                           types,
                           proxy_client_build_save_path,
                           package_path,
                           map_dev_model=map_dev_model)
        if status == 1:
            break
        else:
            time.sleep(1)
            num += 1
        if num == 200:
            break

    return status


def to_build(dev_model, user):
    import threading
    t1 = threading.Thread(target=Build, args=(dev_model, str(user)))
    t1.start()
    return 1


def get_proxy_res(dev_model, user):
    """查询构建日志结果"""
    return get_build_is_complate(dev_model, '1.0','auto', user, 'proxy')