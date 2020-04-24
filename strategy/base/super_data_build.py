#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
import logging
from strategy.conf.path import out_base_path, superd_build_shell_path, get_path_day_time, superd_project_path, \
    superd_build_save_path, superd_build_shell_path_name, config_branch, out_super_data
from strategy.base.op_val import  get_map_dev_model, build, get_build_is_complate, mv_plug
from strategy.control.git_xx import GitProcess
from strategy.control.git_tool import get_tag_code, clear_path


log = logging.getLogger(__name__)


def Build(dev_model, tag, reason, user,branch=None):
    # 构建完成后，包存放的路径
    build_type = 'release'
    package_path = out_base_path + out_super_data + get_path_day_time()

    log.debug('start_build:{},tag:{},reason:{},user:{}'.format(dev_model,tag,reason,user))
    types = 'superd'
    map_dev_model = get_map_dev_model(dev_model)
    if branch:
        branch = branch
        types='superd_test'
        build_type = 'test'
    else:
        branch = config_branch['superd_branch']

    get_tag_code(superd_project_path, tag, branch)
    clear_path(superd_build_save_path,
               package_path,
               superd_build_shell_path_name,
                tag)
    build(map_dev_model, dev_model, user, tag, reason, types)
    # 这里的dev_model 必须使用原始的，就是设备的正常型号而不是cbuild中写的，因为需要入库展示使用。
    build_status = mv_plug(dev_model,
                           user,
                           tag,
                           reason,
                           types,
                           superd_build_shell_path,
                           package_path,
                           build_type)
    git = GitProcess(superd_project_path)
    git._init_directoy(branch)

    return build_status

def toBuild(dev_model, tag, reason, user):
    import threading
    t1 = threading.Thread(target=Build, args=(dev_model, tag, reason, str(user)))
    t1.start()
    return 1


def toBuild_test(dev_model, branch, reason, user, tag='RC'):
    import threading
    t1 = threading.Thread(target=Build, args=(dev_model, tag, reason, str(user), branch))
    t1.start()
    return 1

def get_superd(dev_model, tag, reason, user,is_test=None):
    types = 'superd'
    if is_test:
        types='superd_test'
    return get_build_is_complate(dev_model, tag, reason, user, types)