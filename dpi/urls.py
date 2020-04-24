#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'

from django.urls import path
from . import views
from dpi.pubilc import api
app_name = 'dpi'
urlpatterns = [
    # view
    path('showData/', views.show_data, name='showData'),
    path('showPData/', views.show_p_data, name='showPData'),
    path('dpi_conf/', views.dpi_conf, name='dpi_conf'),
    path('api_getDpiConfAll/', api.api_getDpiConfAll, name='api_getDpiConfAll'),
    path('api_getNSPAll/', api.api_getNSPAll, name='api_getNSPAll'),
    path('api_getDpiMultimodeAll/', api.api_getDpiMultimodeAll, name='api_getDpiMultimodeAll'),
    path('api_createDPIConf/', api.api_createDPIConf, name='api_createDPIConf'),
    path('api_generateDpi/', api.api_generateDpi, name='api_generateDpi'),
    path('api_createDpiPcap/', api.api_createDpiPcap, name='api_createDpiPcap'),
    path('api_getDpiPcapAll/', api.api_getDpiPcapAll, name='api_getDpiPcapAll'),
    path('api_delDpiConf/', api.api_delDpiConf, name='api_delDpiConf'),
    path('api_getDpiConf/', api.api_getDpiConf, name='api_getDpiConf'),
    path('api_getPlatformViType/', api.api_getPlatformViType, name='api_getPlatformViType'),
    path('api_get_ec/', api.api_get_ec, name='api_get_ec'),
    path('api_set_weight/', api.api_set_weight, name='api_set_weight'),
    path('api_get_net_safety_platform/', api.api_get_net_safety_platform, name='api_get_net_safety_platform'),
    path('api_get__app_pro_code/', api.api_get__app_pro_code, name='api_get__app_pro_code'),


    path('delData/', views.del_data, name='delData'),
    path('api_getAllEC/', views.api_getAllEC, name='api_getAllEC'),
    path('api_searchEC/', views.api_searchEC, name='api_searchEC'),
    path('api_analysis_vi_type_id/', views.api_analysis_vi_type_id, name='api_analysis_vi_type_id'),
    path('api_get_platform/', views.api_get_platform, name='api_get_platform'),
    path('api_get_type/', views.api_get_type, name='api_get_type'),
    path('api_get_app/', views.api_get_app, name='api_get_app'),
    path('api_updateEC/', views.api_updateEC, name='api_updateEC'),
    path('api_createEC/', views.api_createEC, name='api_createEC'),
    path('api_getNsVi/', views.api_get_ns_vi_rule, name='api_getNsVi'),
]