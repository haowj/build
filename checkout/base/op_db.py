# coding:utf-8
__author__ = 'xcma'
from checkout.models import *
from appack.models import dev_model_db, oem_db
import logging
log = logging.getLogger(__name__)


class opDeviceDB:
    """
    设备状态表
    """
    def getDeviceDB(self):
        data = DeviceDB.objects.values()
        return data

    def getDeviceDBIdInfo(self,id):
        data = DeviceDB.objects.filter(id=id).values().first()
        return data

    def getDeviceDBDevModelList(self):
        rlist = []
        data = self.getDeviceDB()
        for i in data:
            dev_model = i['dev_model']
            id = i['id']
            if dev_model not in rlist:
                rd = {}
                rd['dev_model']=dev_model
                rd['id']=id
                rlist.append(rd)
        return rlist

    def addTestAP(self, **kwargs):
        try:
            data = DeviceDB.objects.create(**kwargs)
            return 1
        except Exception as e:
            log.error(e)
            return e

    def delTestAP(self, ids):
        try:
            data = DeviceDB.objects.filter(id=ids).delete()
            return 1
        except Exception as e:
            log.error(e)
            return e

    def upTestAP(self, ids, **kwargs):
        try:
            data = DeviceDB.objects.filter(id=ids).update(**kwargs)
            return 1
        except Exception as e:
            log.error(e)
            return e

    def setStatus(self, dev_model_id, status):
        data = DeviceDB.objects.filter(id=dev_model_id).update(status=str(status))
        return data


class opDevModelDB:
    """
    设备型号
    """
    def getdevModelList(self, oem_name):
        # log.debug(oem_name)
        data = dev_model_db.objects.filter(oem_name=oem_name).values('zy_model')
        # log.debug(data)
        return data

    def getDevModelInfo(self,dev_model):
        data = dev_model_db.objects.filter(zy_model=dev_model).values().order_by('-id').first()
        return data

class opOemDB:
    """
    厂商信息
    """
    def getoemList(self):
        data = oem_db.objects.values('oem_name')
        return data


class opTestCase:
    """
    测试用例
    """
    def upTestCase(self, ids, **kwargs):
        try:
            data = TestCase.objects.filter(id=ids).update(**kwargs)
            return 1
        except Exception as e:
            log.error(e)
            return e

    def delTestCase(self, ids):
        try:
            data = TestCase.objects.filter(id=ids).update(status=str(0))
            return 1
        except Exception as e:
            log.error(e)
            return e

    def addTestCase(self, **kwargs):
        try:
            data = TestCase.objects.create(**kwargs)
            return 1
        except Exception as e:
            log.error(e)
            return e

    def getTestCase(self):
        data = TestCase.objects.filter(status=1).values().order_by('-id')
        return data

    def get_test_case_info(self, case_id):
        try:
            data = TestCase.objects.filter(id=case_id).values().order_by('-id').first()
            return data
        except Exception as e:
            log.error(e)
            return 'error:{}'.format(e)


class opStrategyRecord:
    """
        执行策略记录表
    """
    # def getRecordList(self):
    #     data =StrategyRecord.objects.values().order_by('-id')[:100]
    #     return data
    def getRecordList(self):
        data =StrategyRecord.objects.all().order_by('-id')[:100]
        return data

    def get_strategy_record(self, ids):
        try:
            data = StrategyRecord.objects.filter(id=ids).values().first()
            return data
        except Exception as e:
            log.error(e)
            return 'error:{}'.format(e)


class opStrategyData:
    """
    策略执行返回数据表
    """
    @property
    def get_record_data(self):
        data = StrategyData.objects.all().order_by('-id')[:100]
        return data

    def get_case_result(self, ids):
        try:
            data = StrategyData.objects.filter(strategyRID=ids)
            return data
        except Exception as e:
            log.error(e)
            return 'error:{}'.format(e)


class opExecuteStrategy:
    """
    执行策略
    """
    def getApSetList(self):
        data = ExecuteStrategy.objects.filter(status=1).values()
        return data

    def getTestSetInfo(self, dev_id='',id=''):
        try:
            if dev_id:
                data = ExecuteStrategy.objects.filter(deviceID=dev_id).values()
            else:
                data = ExecuteStrategy.objects.filter(id=id).values()
            return data
        except Exception as e:
            log.error(e)
            return 'error:{}'.format(e)

    def setStatus(self,id,status):
        try:
            ExecuteStrategy.objects.filter(id=id).update(status=status)
            data =1
        except Exception as e:
            log.error(e)
            data =0
        return data

    def addApSet(self,**kwargs):
        try:
            ExecuteStrategy.objects.create(**kwargs)
            data =1
        except Exception as e:
            log.error(e)
            data =e
        return data

    def getESList(self,caseID):
        try:
            data = ExecuteStrategy.objects.filter(caseID__contains=caseID).values()
            return data
        except Exception as e:
            log.error(e)
            return 'error:{}'.format(e)

class opCaseSet:
    """
    测试集
    """
    def getCaseSet(self, id=''):
        try:
            if id:
                data = CaseSet.objects.filter(id=id).values().first()
            else:
                data = CaseSet.objects.filter(status=1).values()
            return data
        except Exception as e:
            log.error(e)
            return 'error:{}'.format(e)

    def setStatus(self,id,status):
        try:
            CaseSet.objects.filter(id=id).update(status=status)
            data = 1
        except Exception as e:
            data=e
        return data

    def addTestSet(self,**kwargs):
        try:
            CaseSet.objects.create(**kwargs)
            data = 1
        except Exception as e:
            data = e
        return data

    @property
    def get_test_set_all(self):
        try:
            data = CaseSet.objects.all()
            return data
        except Exception as e:
            log.error(e)
            return 'error:{}'.format(e)


class opredisData:
    """
    获取基础信息

    """
    def getBasicsInfoList(self, ids):
        data = rs_conn.smembers(ids)
        return data

    def setBasicsInfoList(self, ids, x):
        try:
            data = rs_conn.sadd(ids, x)
            return 1
        except Exception as e:
            log.error(e)
            return e

    def delBasicsInfoList(self, ids, x):
        try:
            rs_conn.srem(ids, x)
            return 1
        except Exception as e:
            log.error(e)
            return e

    def getBasicsInfo(self, ids):
        data = rs_conn.get(ids)
        return data

    def setBasicsInfo(self, ids, x):
        try:
            data = rs_conn.set(ids, x)
            return 1
        except Exception as e:
            log.error(e)
            return e

    def delBasicsInfo(self, ids):
        try:
            data = rs_conn.delete(ids)
            return 1
        except Exception as e:
            log.error(e)
            return e

opdd = opDeviceDB()
opdmd = opDevModelDB()
opod = opOemDB()
optestcase = opTestCase()
opes = opExecuteStrategy()
opcs = opCaseSet()
opsr = opStrategyRecord()
opsd = opStrategyData()
oprd = opredisData()