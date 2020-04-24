#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from checkout.models import ExecuteStrategy, StrategyRecord, CaseSet, TestCase, DeviceDB
from dss.Serializer import serializer
from django.shortcuts import HttpResponse
import inspect


def response_as_json(data, foreign_penetrate=False):
    json_string = serializer(data=data, output_type="json", foreign=foreign_penetrate)
    response = HttpResponse(
            json_string,
            content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200, foreign_penetrate=False, **kwargs):
    data = {
        "code": code,
        "msg": "成功",
        "data": data,
    }
    return response_as_json(data, foreign_penetrate=foreign_penetrate)


def json_response_ori(data, foreign_penetrate=False):
    return response_as_json(data, foreign_penetrate=foreign_penetrate)


def json_error(error_string="", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


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


def refactoring_device_data():
    """
    修改直接获取记录表中数据
    并置状态为新建，


    策略数据获取
    :return:
    """
    obj = ExecuteStrategy.objects.filter(task_status=1)
    srd = StrategyRecord.objects.filter(task_status=0)

    gpedit = list()
    for i in obj:
        i.deviceID.status = '2'
        i.deviceID.save()
        i.task_status = 2
        i.save()
    for j in srd:
        gpedit.append(j.id)
        j.task_status = 1
        j.save()
    return gpedit


def get_test_case(args):
    """
    获取用例信息
    :param args:
    :return:
    """
    data = dict()
    for dit in args:
        data[dit] = dict()
        data[dit]['command'] = set()
        aDit = StrategyRecord.objects.get(id=dit)

        for i in aDit.caseID.split(','):
            set_case = CaseSet.objects.filter(status=1).get(id=i)
            case_id = set_case.case_action.split(',')
            for cid in case_id:
                try:
                    cdd = TestCase.objects.filter(status=1).get(id=cid)
                    if cdd.args_vales in ['local_ifname', 'wan_ifname', 'gwip', 'gwmask']:
                        data[dit][cdd.args_command] = 'ifconfig'
                    data[dit]['command'].add(cdd.args_command)
                except:
                    pass
        data[dit]['command'] = list(data[dit]['command'])
        data[dit]['dev_info'] = {'ip': aDit.strategyID.deviceID.dev_ip,
                                 'password': aDit.strategyID.deviceID.dev_password,
                                 'port': aDit.strategyID.deviceID.dev_port,
                                 'user': aDit.strategyID.deviceID.dev_user,
                                 'remark': aDit.strategyID.deviceID.remark}

    return data

