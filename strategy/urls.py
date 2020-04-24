#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
from django.urls import path
from . import views
from strategy.response import views as vs
from strategy.response import api

app_name = 'strategy'

urlpatterns = [
    # 获取数据 view
    path('getsapiloader/', vs.get_super_api_load, name='getsapiloader'),
    path('getsuperdcf/', vs.get_super_d_config, name='getsuperdcf'),
    path('getdevmodel/', views.get_dev_model, name='getdevmodel'),
    path('getoem/', views.get_oem, name='getoem'),
    path('getsuperd/', vs.get_super_d_data, name='getsuperd'),
    path('getsuperdtest/', vs.get_super_data_test, name='getsuperdtest'),
    path('gettag/', vs.get_tag, name='gettag'),
    path('getconnector/', vs.get_connector, name='getconnector'),
    path('getpackage', vs.get_package, name='getpackage'),
    path('getonline/', vs.get_online_info, name='getonline'),

    # 数据查询接口
    path('taginfo/', api.tag_info, name='taginfo'),
    path('buildloginfo/', api.build_log_info, name='buildloginfo'),
    path('getpackageinfo/', api.get_package_one_info, name='getpackageinfo'),
    path('getfirpackage/', api.get_filter_package_info, name='getfirpackage'),
    path('getonlineinfo/', api.get_online_log, name='getonlineinfo'),
    path('getTagList/', api.get_tag_list_info, name='getTagList'),
    path('getspailoadpack', api.get_super_api_loader_package, name='getspailoadpack'),
    path('getProxyDownUrl/', api.get_proxy_down_url, name='getProxyDownUrl'),

    # 数据插入
    path('setStrategy/', api.set_strategy, name='setStrategy'), # 插件一键打包
    path('setoem/', views.set_oem, name='setoem'),
    path('setdevmodel/', views.set_dev_model, name='setdevmodel'),
    path('setsuperdcf/', views.set_super_config, name='setsuperdcf'),
    path('settag/', api.tag_add, name='settag'),
    path('setconnector/', api.connector_add, name='setconnector'),
    path('setonline/', api.set_online_log, name='setonline'),
    path('setsapiloder/', api.set_sapiloder_package, name='setsapiloder'),
    path('setproxy/', api.set_proxy_package, name='setproxy'),


    # 数据删除接口
    path('deltag/', api.del_tag, name='deltag'),


    # 构建接口 super_data_build
    path('superd_build/', api.super_data_build, name='superd_build'),
    path('sapiloader_c_build/', api.super_api_loader_build, name='sapiloader_c_build'),
    path('superd_build_test/', api.super_data_build_test, name='superd_build_test'),


    # 构建结果查询
    path('superd_build_result/', api.super_data_build_result, name='superd_build_result'),
    path('sapiloader_c_build_result/', api.get_info_super_api_loader, name='sapiloader_c_build_result'),

]