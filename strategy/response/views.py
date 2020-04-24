#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from strategy.base.tools import authentication
from strategy.control.git_tool import get_tag_list
from strategy.base.op_val import get_all_version_data, get_super_task_data, get_info_online_log,\
    get_super_d_all, get_build_log, get_super_d_config_data, get_super_api_loader_data, \
    get_build_package_info, get_dpi_config_all, get_proxy_version_info, get_info_super_api_loader_package, get_tag_info
from strategy.conf.path import connector_type, package_contains_path_dict, save_path, superdcf_type, \
    package_type, c_sapiloader, shell_sapiloader, superd_build_test_branch_list

import logging


log = logging.getLogger(__name__)

@login_required(login_url='/admin/login/')
def get_tag(request):
    auth = authentication(request)
    if auth == 200:
        tag_data = get_tag_info(status=1)

        super_data = ['RC']
        super_api_load = ['RC']
        connector = ['RC']
        if tag_data:
            for t_i in tag_data:
                if 'superd' in t_i['project_name']:
                    super_data.append(t_i['tag'])
                elif 'sapiloader' in t_i['project_name']:
                    super_api_load.append(t_i['tag'])
                elif 'connector' in t_i['project_name']:
                    connector.append(t_i['tag'])


        vdata = {'superd':'插件版本','sapiloader':'加载器版本','connector':'连接器版本',}
        data = {'vdata':vdata,
                'superd_tag_list':super_data,
                'sapiloader_tag_list':super_api_load,
                'connector_type': connector_type,
                'connector': connector}
        return render(request, 'strategy/tag.html', data)
    return auth


@login_required(login_url='/admin/login/')
def get_super_d_config(request):
    auth = authentication(request)
    if auth == 200:
        model = get_all_version_data()['dev_model']
        model = [i['zy_model'] for i in model]
        data = get_super_d_config_data()
        return render(request, 'strategy/superdcf.html', {'data': data, 'model': model, 'type': superdcf_type})
    return auth


@login_required(login_url='/admin/login/')
def get_connector(request):
    auth = authentication(request)
    if auth == 200:
        model = get_all_version_data()['dev_model']
        dev_model_list = [i['zy_model'] for i in model]
        history_data = get_super_task_data()
        dev_model_list.insert(0, 'fitall')
        tag_list = get_tag_info(project_name='connector')
        if tag_list:
            tag_list = [i['tag'] for i in tag_list]
        else:
            tag_list = []
        data = {'dev_model': dev_model_list, 'tag': tag_list, 'connector_type': connector_type, 'history': history_data}
        return render(request, 'strategy/connector.html', data)
    return auth


@login_required(login_url='/admin/login/')
def get_super_d_data(request):
    auth = authentication(request)
    if auth == 200:
        tag_list = get_tag_info(project_name='superd', status=1)
        if tag_list:
            tag_list = [i['tag'] for i in tag_list]
        else:
            tag_list = []
        model = get_all_version_data()['dev_model']
        dev_model_list = [i['zy_model'] for i in model]
        sdata = get_super_d_all(build_type='superd')
        bldata = get_build_log(type='superd')
        data = {'sdata': sdata, 'bldata': bldata, 'tag':tag_list,'dev_model':dev_model_list}
        return render(request, 'strategy/superd.html', data)
    return auth


@login_required(login_url='/admin/login/')
def get_super_data_test(request):
    auth = authentication(request)
    if auth == 200:
        model = get_all_version_data()['dev_model']
        dev_model_list = [i['zy_model'] for i in model]
        data = get_super_d_all(build_type='test')
        bldata = get_build_log(type='superd_test')
        data = {'sdata':data,'bldata':bldata, 'dev_model': dev_model_list, 'tag': superd_build_test_branch_list}
        return render(request, 'strategy/superd_test.html',data)
    return auth


@login_required(login_url='/admin/login/')
def get_super_api_load(request):
    auth = authentication(request)
    if auth == 200:
        model = get_all_version_data()['dev_model']
        dev_model_list = [i['zy_model'] for i in model]
        data = get_super_api_loader_data()
        dev_model_list.insert(0, 'fitall')
        tag_list = get_tag_info(project_name='sapiloader', status=1)
        if tag_list:
            tag_list = [i['tag'] for i in tag_list]
        else:
            tag_list = []
        bldata = get_build_log(type='sapiloader')
        data = {'dev_model': dev_model_list, 'tag': tag_list, 'sdata':data,'bldata':bldata}
        return render(request, 'strategy/sapiloader_c.html', data)
    return auth


@login_required(login_url='/admin/login/')
def get_online_info(request):
    auth = authentication(request)
    if auth == 200:
        model = get_all_version_data()['dev_model']
        dev_model_list = [i['zy_model'] for i in model]
        rdata = get_info_online_log()
        data = {'release_log': rdata,
                'package_contains_path':package_contains_path_dict,
                'save_path':save_path,
                'dev_model_list':dev_model_list}
        return render(request, 'strategy/release.html', data)
    return auth


@login_required(login_url='/admin/login/')
def get_package(request):
    """
    打包
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        # dev_model , docking_solution
        data = get_all_version_data()

        # super data config data
        super_data_conf = get_super_d_config_data()
        if super_data_conf:
            super_data_conf = super_data_conf[:10]

        # 反向代理包
        proxydata = get_proxy_version_info()

        # dpi data
        dpi = get_dpi_config_all(dev_model_id='88888888')
        if dpi:
            dpi=dpi[:10]
        sldata = get_info_super_api_loader_package()
        rdata = {'pack_list': get_build_package_info(),
                 'pack_type': package_type['c_sapiloader'],
                 'spuer_los': [c_sapiloader, shell_sapiloader],
                 'dpi_config': dpi,
                 'super_data_conf': super_data_conf,
                 'sapiloader_pack_list': sldata,
                 'proxydata': proxydata}
        rdata.update(data)
        return render(request, 'strategy/package.html', {'data': rdata})
    return auth