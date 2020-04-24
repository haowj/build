#!/usr/bin/env python3
# -*-coding:utf-8-*-
from checkout.models import CaseSet, StrategyRecord, TestCase, StrategyData, InitData
from checkout.testCase.sapigetb import SuperApiGetB
import json


def verifyResData(args):

    """
    根据操作函数不同，对应校验返回数据
    :param args:
    :return:
    """

    edit_id = args['GPEDIT']
    record = StrategyRecord.objects.get(id=edit_id)
    record.task_status = '数据上传中'
    record.save()
    rt = True
    for k, v in args['DATAVALUES'].items():
        if 'Error :' in v:
            StrategyData.objects.create(strategyRID=record, deviceID=record.strategyID.deviceID, command=k, data=v)
            record.task_status = '异常数据'
            record.save()
            rt = False
        else:
            InitData.objects.create(strategyRID=record, command=k, initData='没有返回值' if v == '没有返回值' else json.dumps(v))
    if rt:

        for case_set in record.caseID.split(','):
            dct = CaseSet.objects.get(id=case_set)

            for cs in dct.case_action.split(','):
                try:
                    ddt = TestCase.objects.get(id=cs)
                    if ddt.args_command == 'sapigetb':
                        data = getattr(SuperApiGetB(args['DATAVALUES'], record.strategyID.deviceID, ddt.args_vales),
                                       ddt.args_name, '')
                    else:
                        data = [k for k in args['DATAVALUES'].items()][0]

                    StrategyData.objects.create(strategyRID=record, deviceID=record.strategyID.deviceID,
                                                command=ddt.args_command,
                                                check_rule=ddt.args_name, check_data=ddt.args_vales,
                                                data=data[0], result=data[1])
                except:
                    pass
    return 'Im ok'
