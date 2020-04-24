#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
import logging
import inspect
from dss.Serializer import serializer
from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponse


log = logging.getLogger(__file__)

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
    json_string = serializer(data=data, output_type="json", foreign=foreign_penetrate)
    response = HttpResponse(
            json_string,
            content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200, foreign_penetrate=False):
    data = {
        "code": code,
        "msg": "成功",
        "data": data,
    }
    return response_as_json(data, foreign_penetrate=foreign_penetrate)


def json_error(error_string="", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)