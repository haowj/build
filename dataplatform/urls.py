#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'

from django.urls import path
from . import views

app_name = 'dataplatform'

urlpatterns = [
    # 数据查询
    path('getphone/', views.get_phone_number_info, name='getphone'),
    path('getAppInfo/', views.get_app_info, name='getAppInfo'),
    path('getAppUser/', views.get_app_name, name='getAppUser'),
    path('getPhoneApp/', views.get_phone_application_info, name='getPhoneApp'),
    # 新增数据
    path('setPhoneNumber/', views.set_phone_number_info, name='setPhoneNumber'),
    path('setPhoneAppInfo/', views.set_phone_app_info, name='setPhoneAppInfo'),
    # 删除数据
    path('deletePhone/', views.del_phone_number_info, name='deletePhone'),
    path('deleteApp/', views.del_applications_info, name='deleteApp'),

    # 更新数据
    path('alterPhoneNumber/', views.alter_phone_number_info, name='alterPhoneNumber'),
    path('alterPhoneAppInfo/', views.alter_phone_application_info, name='alterPhoneAppInfo'),
]