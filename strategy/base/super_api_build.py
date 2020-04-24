#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
import threading
from strategy.conf.path import config_branch, get_path_day_time, sapiloader_c_project_path, sapiloader_c_build_shell_path, \
    sapiloader_c_build_shell_path_name, out_base_path, out_super_api_loader
from strategy.base.op_val import get_map_dev_model, build, get_build_is_complate, mv_plug
from strategy.control.git_tool import get_tag_code, clear_path
from strategy.control.git_xx import GitProcess


class SuperApi:
    def __init__(self):
        self.types = 'sapiloader'
        self.branch = config_branch['sapiloader_branch']
        self.package_path = out_base_path + out_super_api_loader + get_path_day_time()

    def Build(self, dev_model, tag, reason, user):

        map_dev_model = get_map_dev_model(dev_model)
        get_tag_code(sapiloader_c_project_path, tag, self.branch)
        clear_path(sapiloader_c_build_shell_path, self.package_path, sapiloader_c_build_shell_path_name,
                        tag)
        build(map_dev_model, dev_model, user, tag, reason, self.types)
        # 这里的dev_model 必须使用原始的，因为需要入库展示使用。
        build_status = mv_plug(dev_model, user, tag, reason, self.types, sapiloader_c_build_shell_path,
                                    self.package_path)

        git = GitProcess(sapiloader_c_project_path)
        git._init_directoy(self.branch)
        return build_status

    def to_build(self, dev_model, tag, reason, user):
        t1 = threading.Thread(target=self.Build, args=(dev_model, tag, reason, str(user)))
        t1.start()
        return 1

def get_log_info_super_api_loader(dev_model, tag, reason, user):
    """
    构建结果查询
    :param dev_model:
    :param tag:
    :param reason:
    :param user:
    :return:
    """
    return get_build_is_complate(dev_model, tag, reason, user, 'sapiloader')