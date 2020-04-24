#!/usr/bin/env python3
# -*-coding: utf-8-*-
from checkout.base.redisConn import rs_conn
from checkout.base.tools import refactoring_device_data, get_test_case, StrategyRecord
from checkout.control.verifyManage import verifyResData
import json
import logging
log = logging.getLogger(__name__)


def processManage(kwargs):
    # 业务流程管控

    data = dict()
    kwargs = json.loads(kwargs)
    log.debug(kwargs)
    if kwargs['DTYPE'] == 'TIME':
        data = list()
        data.append(rs_conn.get(kwargs['TIME']['name']))
        data.append(rs_conn.get(kwargs['TIME']['client']))

    if kwargs['DTYPE'] == 'TASK':
        tm = rs_conn.get('ExecuteStrategy')
        if tm == '1':
            dev_model = refactoring_device_data()
            data = get_test_case(dev_model)

    if kwargs['DTYPE'] == 'PUSH':
        data = verifyResData(kwargs)

    if kwargs['DTYPE'] == 'TASKOK':
        db = StrategyRecord.objects.get(id=kwargs['GPEDIT'])
        db.strategyID.task_status = 0
        db.strategyID.save()
        db.strategyID.deviceID.status = 0
        db.strategyID.deviceID.save()
        db.task_status = 2
        db.save()
    if kwargs['DTYPE'] == 'UPC':
        data = rs_conn.set(kwargs['TIME']['client'], 0)

    return json.dumps(data)
