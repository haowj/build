# coding:utf-8
__author__ = 'xcma'

import copy
from checkout.base.op_db import *
log = logging.getLogger(__name__)


class bizM:
    def __init__(self):
        self.res = {'code': 400, 'msg': '', 'data': ''}
    """ api  start"""

    def api_getBasicsInfoList(self, ids):
        data = oprd.getBasicsInfoList(ids)
        if data:
            rs = list()
            for i in data:
                tem = dict()
                v = oprd.getBasicsInfo(i)
                tem[i] = v
                rs.append(tem)
            self.res['code'] = 200
            self.res['data'] = rs
        else:
            self.res['msg'] = data
        return self.res

    def api_setBasicsInfoList(self, ids, x, y):
        data = oprd.setBasicsInfoList(ids, x)
        dst = oprd.setBasicsInfo(x, y)
        if data and dst:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            if not data:
                self.res['msg'] = data
            elif not dst:
                self.res['msg'] = dst
            else:
                self.res['msg'] = [data, dst]
        return self.res

    def api_delBasicsInfoList(self, ids, x):
        data = oprd.delBasicsInfoList(ids, x)
        dst = oprd.delBasicsInfo(x)
        if data and dst:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            if not data:
                self.res['msg'] = data
            elif not dst:
                self.res['msg'] = dst
            else:
                self.res['msg'] = [data, dst]
        return self.res

    def api_getBasicsInfo(self, ids):
        data = oprd.getBasicsInfo(ids)
        if data:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res

    def api_delBasicsInfo(self, ids):
        data = oprd.delBasicsInfo(ids)
        if data:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res

    def api_setBasicsInfo(self, ids):
        data = oprd.setBasicsInfo(ids)
        if data:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res

    def api_getDevModelList(self, oem_name):
        data = opdmd.getdevModelList(oem_name)
        if data:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res

    def api_addTestAP(self, **kwargs):
        data = opdd.addTestAP(**kwargs)
        if data == 1:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res

    def api_delTestAP(self, ids):
        data = opdd.delTestAP(ids)
        if data == 1:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res

    def api_delTestAPSetList(self, ids):
        data = opes.setStatus(ids, 0)
        if data == 1:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res

    def api_getTestAPSetListInfo(self, ids):
        rdata= []
        data = opes.getTestSetInfo(id=ids)
        if 'error' not in data:
            self.res['code'] = 200
            if data:
                for i in data:
                    rdict = {}
                    rdict['id'] = i['id']
                    caseSetId = str(i['caseID']).split(',')
                    for cid in caseSetId:
                        caseSetData = opcs.getCaseSet(cid)
                        caseSet_action = caseSetData['case_action']
                        for caseId in caseSet_action.split(','):
                            caseInfo = optestcase.get_test_case_info(caseId)
                            rdata.append(caseInfo)
                self.res['data'] = rdata
            else:
                self.res['code'] = 400
                self.res['msg'] = '该型号未配置测试策略'
        return self.res

    def api_getTestSetListInfo(self, id):
        rdata= []
        data = opcs.getCaseSet(id=id)
        if 'error' not in data:
            self.res['code'] = 200
            caseSet_action = data['case_action']
            for caseId in caseSet_action.split(','):
                caseInfo = optestcase.get_test_case_info(caseId)
                rdata.append(caseInfo)
            self.res['data'] = rdata
        else:
            self.res['code'] = 400
            self.res['msg'] = '该型号未配置测试策略'
        return self.res


    def api_upTestAP(self, ids, **kwargs):
        data = opdd.upTestAP(ids, **kwargs)
        if data == 1:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res

    def api_addTestCase(self, **kwargs):
        data = optestcase.addTestCase(**kwargs)
        if data == 1:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res
    def api_addTestSet(self, **kwargs):
        data = opcs.addTestSet(**kwargs)
        if data == 1:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res


    def api_addTestApSet(self, **kwargs):
        data = opes.addApSet(**kwargs)
        if data == 1:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res


    def api_upTestCase(self, ids, **kwargs):
        data = optestcase.upTestCase(ids, **kwargs)
        if data == 1:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res

    def api_delTestCase(self, ids):
        data = optestcase.delTestCase(ids)
        if data == 1:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res

    def api_delTestSet(self, ids):
        data = opes.getESList(ids)
        ishave=0
        ddata=0
        if 'error' not in data:
            if not data:
                ishave=0
                ddata = opcs.setStatus(ids,0)
            else:
                ishave=1
        if ishave == 0 and ddata==1:
            self.res['code'] = 200
            self.res['data'] = data
        elif ishave==1:
            self.res['msg'] = '当前测试集正在被使用，请删除对应策略后在操作'
        else:
            self.res['msg'] = ddata
        return self.res

    def getTestAPInfo(self, id):
        data = opdd.getDeviceDBIdInfo(id)
        if data:
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['msg'] = data
        return self.res

    def get_test_set_all(self):
        dat = []
        data = opcs.get_test_set_all
        if 'error' not in data:
            self.res['code'] = 200
            if data:
                for i in data:
                    red = dict()
                    red['setId'] = i.id
                    red['setName'] = i.case_name
                    dat.append(red)
        return self.res

    def get_strategy_data(self, ids):
        temp_list = list()
        data = opsd.get_case_result(ids)
        if 'error' not in data:
            if data:
                self.res['code'] = 200
                for i in data:
                    temp = dict()
                    temp['id'] = i.id
                    temp['command'] = i.command
                    temp['check_rule'] = i.check_rule
                    temp['check_data'] = i.check_data
                    temp['data'] = i.data
                    temp['result'] = i.result
                    temp['create_time'] = i.create_time
                    temp_list.append(temp)
                self.res['data'] = temp_list
            else:
                self.res['code'] = 400
                self.res['msg'] = '未找到执行策略返回结果'
        else:
            self.res['msg'] = data
        return self.res

    def get_case_result(self, ids):
        case_result = list()
        for ik in ids.split(','):
            data = opsd.get_case_result(ik)
            ast = opsr.get_strategy_record(ik)
            if ast:
                if ast['task_status'] == '2':
                    self.res['code'] = 200
                else:
                    self.res['code'] = 300
            if 'error' not in data:
                if data:
                    for i in data:
                        crdr = dict()
                        crdr['crid'] = i.id
                        crdr['oem_name'] = i.deviceID.oem_name
                        crdr['dev_model'] = i.deviceID.dev_model
                        crdr['command'] = i.command
                        crdr['check_rule'] = i.check_rule
                        crdr['check_data'] = i.check_data
                        crdr['data'] = i.data
                        crdr['result'] = i.result
                        case_result.append(crdr)
                    self.res['data'] = case_result
            else:
                self.res['msg'] = data
        return self.res

    def get_test_case(self, ids):
        case_list = list()
        data = optestcase.get_test_case_info(ids)
        if 'error' not in data:
            self.res['code'] = 200
            if data:
                rdict = {}
                args_command = data['args_command']
                args_name = data['args_name']
                args_vales = data['args_vales']
                args_remark = data['args_remark']
                rdict['args_command'] = args_command
                rdict['args_name'] = args_name
                rdict['args_vales'] = args_vales
                rdict['args_remark'] = args_remark
                case_list.append(copy.deepcopy(rdict))
                self.res['data'] = case_list
            else:
                self.res['code'] = 400
                self.res['msg'] = '未找到改測試用例'
        else:
            self.res['msg'] = data
        return self.res

    def get_test_set(self, ids):
        case_list = list()
        data = opcs.getCaseSet(ids)
        if 'error' not in data:
            self.res['code'] = 200
            if data:
                for i in data:
                    rdict = {}
                    test_case = str(i['case_action']).split(',')
                    for cid in test_case:
                        case_data = opes.get_test_case_info(cid)
                        args_command = case_data['args_command']
                        args_name = case_data['args_name']
                        args_vales = case_data['args_vales']
                        rdict['args_command'] = args_command
                        rdict['args_name'] = args_name
                        rdict['args_vales'] = args_vales
                        case_list.append(copy.deepcopy(rdict))
                self.res['data'] = case_list
            else:
                self.res['code'] = 400
                self.res['msg'] = '该型号未配置测试策略'
        else:
            self.res['msg'] = data
        return self.res

    def getTestSet(self, id):
        # id=设备id
        rdata = []
        data = opes.getTestSetInfo(id)
        if 'error' not in data:
            self.res['code'] = 200
            if data:
                for i in data:
                    rdict = {}
                    rdict['id'] = i['id']
                    caseSetId = str(i['caseID']).split(',')
                    for cid in caseSetId:
                        caseSetData = opcs.getCaseSet(cid)
                        caseSetId = caseSetData['id']
                        caseSet_name = caseSetData['case_name']
                        caseSet_action = caseSetData['case_action']
                        rdict['caseSetId'] = caseSetId
                        rdict['caseSet_name'] = caseSet_name
                        rdict['caseSet_action'] = caseSet_action
                        rdata.append(copy.deepcopy(rdict))
                self.res['data'] = rdata
            else:
                self.res['code'] = 400
                self.res['msg'] = '该型号未配置测试策略'
        else:
            self.res['msg'] = data
        return self.res

    def runTestAP(self, caseSetList, dev_model_id, user):
        if dev_model_id:
            opdd.setStatus(dev_model_id, 1)
        if caseSetList:
            self.res['code'] = 200
            gpedit = list()
            for i in str(caseSetList).split(','):
                strategyId = i.split('|')[0]
                caseId = i.split('|')[1]
                bb = ExecuteStrategy.objects.get(id=strategyId)
                bb.task_status = '1'
                bb.save()
                srd = StrategyRecord.objects.create(strategyID=bb, caseID=caseId, task_status='0',
                                                    operator=str(user))
                gpedit.append(srd.id)
            self.res['data'] = gpedit
        else:
            self.res['code'] = 500
            self.res['msg'] = '任务执行失败'
        return self.res

    """ api  end"""

    """view start"""
    def view_gettestApListData(self):
        data = {}
        ddata = opdd.getDeviceDB()
        data['list_testap'] = ddata
        oem_list = opod.getoemList()
        data['add_testap_oem'] = oem_list
        return data

    def view_getApSetList(self):
        rdict = {}
        rlist = []
        data = opes.getApSetList()
        for i in data:
            info = opdd.getDeviceDBIdInfo(i['deviceID_id'])
            dev_model = info['dev_model']
            i['dev_model'] = dev_model
            caseSetId = i['caseID']
            cinfo = opcs.getCaseSet(caseSetId)
            caseSetName = cinfo['case_name']
            case_action = cinfo['case_action']
            i['caseSetName'] = caseSetName
            i['case_action'] = case_action
            rlist.append(i)
        rdict['ApSetList']=rlist
        devList = opdd.getDeviceDBDevModelList()
        testSetList = opcs.getCaseSet()
        rdict['devList']=devList
        rdict['testSetList']=testSetList
        return rdict

    def view_getTestCase(self):
        data = optestcase.getTestCase()
        return data

    def view_getSetList(self):
        data = opcs.getCaseSet()
        return data

    def view_getRecordList(self):
        data = opsr.getRecordList()
        rlist = list()
        for i in data:
            temp = dict()
            temp['id'] = i.id
            temp['oem_name'] = i.strategyID.deviceID.oem_name
            temp['dev_model'] = i.strategyID.deviceID.dev_model
            temp['case_name'] = opcs.getCaseSet(i.caseID)['case_name']
            temp['status'] = i.task_status
            temp['operator'] = i.operator
            temp['create_time'] = i.create_time
            yield temp

    """view end"""


bm = bizM()
