#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
import logging
from strategy.control.git_xx import GitProcess
from strategy.conf.path import superd_project_path, connector_project_path, sapiloader_c_project_path, \
    sapiloader_c_build_shell_path, supertack_file_path_name, superctl_file_path_name, get_path_day_time, \
    out_base_path, superd_build_shell_path
from strategy.base.tools import getProjectGitTag, get_md5_big, cps, executionShell, chmod_file

log = logging.getLogger(__name__)


def git_code(tag, branch='master'):
    try:
        git = GitProcess(connector_project_path)
        if 'RC' == tag:
            git.pull()
        else:
            git._init_directoy(branch)
            git.reset_tag(tag)
    except Exception as e:
        log.error(e)


def get_tag_list(types):
    if 'superd' in types:
        project_path = superd_project_path
    elif 'connector' in types:
        project_path = connector_project_path
    elif 'sapiloader' in types:
        project_path = sapiloader_c_project_path
    else:
        project_path = ''
        log.error('type[{}] is not found'.format(types))
    git = GitProcess(project_path)
    tag_list = git.getTagList()[:50]
    tag_list.insert(0, 'RC')
    return tag_list


def get_tag_code(path, tag, branch):
    """
    拉取指定tag的代码，
    :return:
    """
    try:
        git = GitProcess(path)
        git._init_directoy(branch)
        if 'RC' not in tag:
            git.reset_tag(tag)
            log.debug('拉取指定tag：{}的代码,完成'.format(tag))
            getProjectGitTag(path)
            git.active_branch()
    except Exception as e:
        log.error(e)


def cp_file(connector_type):
    package_path = out_base_path + f'connector/{get_path_day_time()}'
    try:
        if connector_type == 'c_sapiloader':
            connector_file_path_name = supertack_file_path_name
            set_path = package_path+'supertack'
        elif connector_type == 'shell_sapiloader':
            connector_file_path_name = superctl_file_path_name
            set_path = package_path + 'superctl'
        else:
            log.warning(f'复制链接数据失败，类型：{connector_type}')
            return False
        md5 = get_md5_big(connector_file_path_name)
        res = cps(connector_file_path_name, package_path)
        return res, md5, set_path
    except Exception as e:
        log.error(e)
        return False


def clear_path(build_save_path,save_path,build_shell_path_name,tag):
    """
    创建远端项目下载路径
    :param build_save_path:
    :param save_path:
    :param build_shell_path_name:
    :param tag:
    :return:
    """
    try:
        if 'sapi_bootstrap' in build_shell_path_name:
            cmd = 'rm -rf {}'.format(build_save_path + 'sapiloader')

        elif 'device_side_2' in build_shell_path_name:
            cmd = 'rm -rf {}'.format(build_save_path + 'superd')
        elif 'reverse_proxy' in build_shell_path_name:
            cmd = f'rm -rf {build_save_path}*'
        else:
            log.warning(f'在目录：{build_save_path}，中未找到匹配值。')
            cmd = ''
        log.debug(f'执行清空构建输出路径:{cmd}')
        executionShell(cmd)


        # 清空存放文件路径
        cmd = f'rm -rf {save_path}'
        log.debug(f'执行清空存放路径：{cmd}')
        executionShell(cmd)

        # 给执行文件授权
        chmod_file(build_shell_path_name)

        if 'sapi_loader' in build_shell_path_name:
            # 给加载器构建添加版本号
            change_version = "sed -i 's/\"v1.5\"/\"{}\"/g' config.h".format(tag)
            log.debug('修改加载器config.h文件:{}'.format(change_version))
            executionShell(change_version, sapiloader_c_build_shell_path)

        elif 'super2d' in build_shell_path_name:
            # 给superD构建添加版本号
            change_version = "sed -i 's/\"superd_version\"/\"{}\"/g' config.h".format(tag)
            log.debug('修改superD config.h文件:{}'.format(change_version))
            executionShell(change_version, superd_build_shell_path)

    except Exception as e:
        log.error(e)
        raise e

