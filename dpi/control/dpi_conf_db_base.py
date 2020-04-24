# coding:utf-8
__author__ = 'xcma'
from dpi.models import *
import logging
log = logging.getLogger(__name__)

class multiMode:
    def __init__(self):
        self.data = None

    def get_multimode(self, **kwargs):
        try:
            if kwargs:
                self.data = Multimode.objects.filter(status=1, **kwargs).values()
                self.data = [i for i in self.data]
            else:
                self.data = Multimode.objects.filter(status=1).values()
                self.data = [i for i in self.data]
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)
        return self.data

    def update_multimode(self, ids, **kwargs):
        try:
            if kwargs:
                self.data = Multimode.objects.filter(id=ids).update(**kwargs)
            else:
                self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)
        return self.data

    def create_multimode(self, **kwargs):
        try:
            Multimode.objects.create(**kwargs)
            self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

        return self.data

    def del_multimode(self,id):
        try:
            if id:
                self.data = Multimode.objects.filter(id=id).update(status=0)
            else:
                self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)
        return self.data

class dpiConfLog:
    def __init__(self):
        self.data = None

    def insert(self,**kwargs):
        try:
            DpiConfLog.objects.create(**kwargs)
        except Exception as e:
            log.error(e)
            pass


class dpiConf:

    def __init__(self):
        self.data = None

    def get_dpiconf(self, **kwargs):
        try:
            rlist = []
            if kwargs:
                self.data = DpiConf.objects.filter(status=1, **kwargs).values()
                self.data = [i for i in self.data]
            else:
                self.data = DpiConf.objects.filter(status=1).values().order_by('-weight')
                self.data = [i for i in self.data]
            for m in self.data:
                multimode_id = m['multimode_id']
                data = mm.get_multimode(id=multimode_id)
                type_id=''
                type_value=''
                for j in data:
                    type_id = j['type_id']
                    type_value = j['type_value']
                m['type_id']=type_id
                m['type_value']=type_value
                rlist.append(m)
        except Exception as e:
            log.error(e)
            rlist = 'error:{}'.format(e)
        return rlist
    def update_dpiconf(self, ids, **kwargs):
        try:
            if kwargs:
                self.data = DpiConf.objects.filter(id=ids).update(**kwargs)
            else:
                self.data = 1
                ids=0
            dcl.insert(rule_id=ids,op_info=str(kwargs),user=kwargs['user'])
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)
        return self.data

    def update_dpiconf_init_weight(self):
        self.data = DpiConf.objects.update(weight=0)

    def create_dpiconf(self, **kwargs):
        try:
            dpipcap_id = kwargs['dpipcap_id']
            del kwargs['dpipcap_id']
            obj, created = DpiConf.objects.update_or_create({'dpipcap_id':dpipcap_id},**kwargs)
            # obj, created = DpiConf.objects.update_or_create({'rule_name':kwargs['rule_name'],'vi_type_id':kwargs['vi_type_id'],'multimode_id':kwargs['multimode_id'],'rule_data':kwargs['rule_data'],'rule_begin_match':kwargs['rule_begin_match'],'rule_end_match':kwargs['rule_end_match'],' user':kwargs['user'],'comment':kwargs['comment'],'dpipcap_id':kwargs['dpipcap_id'],"dpipcap_id":kwargs['dpipcap_id']},**kwargs)
            # log.debug(obj)
            # log.debug(created)
            if created:
                msg = f'规则：[{obj}]新增成功'
            else:
                msg = f'规则：[{obj}]更新成功'
            dcl.insert(rule_id=kwargs['rule_name'], op_info=msg,user=kwargs['user'])
            data = msg
        except Exception as e:
            log.error(e)
            data = 'error:{}'.format(e)
        return data

    def del_dpiconf(self,id):
        try:
            if id:
                self.data = DpiConf.objects.filter(id=id).update(status=0)
            else:
                self.data = 1
                id=0
            dcl.insert(rule_id=id,op_info='delete')
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)
        return self.data

    def get_dpiConfDistinct(self,key,**kwargs):
        try:
            if kwargs:
                self.data = DpiConf.objects.filter(status=1,**kwargs).values(key).distinct()
                self.data = [i for i in self.data]
            else:
                self.data = DpiConf.objects.filter(status=1).values(key).distinct()
                self.data = [i for i in self.data]
        except Exception as e:
            self.data = f'error:{e}'
        return self.data

class modelInfo:

    def __init__(self):
        self.data = None

    def getInfo(self,**kwargs):

        try:
            if kwargs:
                self.data = MobileInfo.objects.filter(status=1,**kwargs).values()
                self.data = [i for i in self.data]
            else:
                self.data = MobileInfo.objects.filter(status=1).values()
                self.data = [i for i in self.data]
        except Exception as e:
            self.data = f'error:{e}'
        return self.data

class dpiPcap:

    def __init__(self):
        self.data = None

    def createPcap(self,**kwargs):
        try:
            DpiPcap.objects.create(**kwargs)
            self.data = True
        except Exception as e:
            self.data = f'error:{e}'
        return self.data

    def getPcap(self,**kwargs):
        try:
            rlist = []
            if kwargs:
                self.data = DpiPcap.objects.filter(status=1,**kwargs).values()
                self.data = [i for i in self.data]
            else:
                self.data = DpiPcap.objects.filter(status=1).values()
                self.data = [i for i in self.data]
            for i in self.data:
                mobileinfo_id = i['mobileinfo_id']
                data = mi.getInfo(id=mobileinfo_id)
                oem='暂无'
                os_name='暂无'
                os_version='暂无'
                oem_os_version='暂无'
                oem_os_name='暂无'
                for j in data:
                    oem = j['oem']
                    os_name = j['os_name']
                    os_version = j['os_version']
                    oem_os_version = j['oem_os_version']
                    oem_os_name = j['oem_os_name']
                i['oem']=oem
                i['os_name']=os_name
                i['os_version']=os_version
                i['oem_os_version']=oem_os_version
                i['oem_os_name']=oem_os_name
                rlist.append(i)
        except Exception as e:
            rlist = f'error:{e}'
        return rlist

mm = multiMode()
dc = dpiConf()
dcl = dpiConfLog()
dp = dpiPcap()
mi = modelInfo()