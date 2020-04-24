# coding:utf-8
import copy
import time

__author__ = 'xcma'
import logging
log = logging.getLogger(__name__)
from dpi.control.dpi_conf_db_base import dc,mm,dp,mi
from dpi.control.iface import bm
from dpi.control.dao import appNs
from dpi.pubilc.misc import is_contain_chinese,mkdir,get_md5_big
from .generate_dpi_dat import gDpi
from dpi.conf.path import dpi_file_save_path

class DpiConfView:

    def __init__(self):
        self.data = {}
        self.res = {'code': 400, 'msg': '', 'data': self.data}
    def _res(self,data):
        if 'error' not in str(data):
            self.res['code']=200
            self.res['data']=data
        else:
            self.res['msg'] = data
        return self.res

    def view_all_dpi_conf(self):
        data = dc.get_dpiconf()
        return self._res(data)

    def view_all_dpi_multimode(self):
        data = mm.get_multimode()
        return self._res(data)

    def view_create_dpi_conf(self,**kwargs):
        rule_name =  kwargs['rule_name']
        vi_type_id =  kwargs['vi_type_id']
        multimode_id = kwargs['multimode_id']
        rule_data = kwargs['rule_data']
        rule_begin_match = kwargs['rule_begin_match']
        rule_end_match = kwargs['rule_end_match']
        if is_contain_chinese(rule_name):
            self.res['code'] = 410
            self.res['msg'] = '规则名称不能包含中文'
            return self.res
        # a = 1
        # nddata = dc.get_dpiconf(rule_name=rule_name)
        # while True:
        #     if 'error' not in str(nddata):
        #         if nddata:
        #             if (len(str(a)))==1:
        #                 s= f'00{a}'
        #             elif (len(str(a)))==2:
        #                 s= f'0{a}'
        #             else:
        #                 s = a
        #             new_rule_name = f'{rule_name}_{s}'
        #             kwargs['rule_name'] = new_rule_name
        #             a+=1
        #             nddata = dc.get_dpiconf(rule_name=new_rule_name)
        #         else:
        #             break
        un_vi_type_id = bm.api_analysis_vi_type_id(vi_type_id)
        if un_vi_type_id['code'] == 200:
            vi_data = un_vi_type_id['data']
            idata = vi_data['idata']
            bdata = vi_data['bdata']
            edata = vi_data['edata']
            identityType = idata['identityType']
            businessType = bdata['businessType']
            name = edata['name']

            if 'en' not in idata:
                self.res['code'] = 401
                self.res['msg'] = f'虚拟身份ID中，{identityType}'
                return self.res
            if 'en' not in bdata:
                self.res['code'] = 402
                self.res['msg'] = f'虚拟身份ID中，{businessType}'
                return self.res
            if 'en' not in edata:
                self.res['code'] = 403
                self.res['msg'] = f'虚拟身份ID中，{name}'
                return self.res
            comment = f'{businessType}-{name}-{identityType}'
            in_comment = kwargs['comment']
            kwargs['comment'] = f'[{comment}]{in_comment}'
        else:
            self.res['code'] = 405
            self.res['msg'] = '业务类型编码错误'
            return self.res

        mdata = mm.get_multimode(id=multimode_id)
        if 'error' not in str(mdata):
            if not mdata:
                self.res['code']=406
                self.res['msg'] = '多模id不存在'
                return self.res
        else:
            self.res['code'] = 407
            self.res['msg'] = mdata
            return self.res

        ddata = dc.get_dpiconf(multimode_id=multimode_id,rule_name=rule_name,rule_data=rule_data,rule_begin_match=rule_begin_match,rule_end_match=rule_end_match)
        if 'error' not in str(ddata):
            if ddata:
                self.res['code'] = 408
                self.res['msg'] = '该规则已经存在'
                return self.res
        else:
            self.res['code'] = 409
            self.res['msg'] = ddata
            return self.res
        data = dc.create_dpiconf(**kwargs)
        return self._res(data)

    def view_generateDpiFile(self,dev_model='全型号通用',dev_model_id='88888888',comment='',user='auto create'):
        data = gDpi.generateDpiFile(dev_model,dev_model_id,comment,user)
        return self._res(data)

    def view_upgrade_dpi_conf(self,id,**kwargs):
        data = dc.update_dpiconf(ids=id,**kwargs)
        return self._res(data)
    def view_update_dpiconf_init_weight(self):
        data = dc.update_dpiconf_init_weight()
        return self._res(data)

    def view_get_dpi_conf(self,id):
        data = dc.get_dpiconf(id=id)
        return self._res(data)

    def view_get_nsp_conf(self,id):
        rdata = []
        data = dc.get_dpiConfDistinct('vi_type_id')
        appdata = []
        idata = []
        bdata = []
        edata = []
        distinct_vi_type_id_ns_code_list = []
        vi_type_id_ns_code_list_all = []
        for i in data:
            rdict = {}
            vi_type_id = str(i['vi_type_id'])
            vi_type_id_ns_code_list = []
            un_vi_type_id = bm.api_analysis_vi_type_id(str(vi_type_id))
            if un_vi_type_id['code'] == 200:
                vi_data = un_vi_type_id['data']
                idata = vi_data['idata']
                bdata = vi_data['bdata']
                edata = vi_data['edata']
                i['idata']=idata
                i['bdata']=bdata
                i['edata']=edata
                if int(id) != 0:
                    bcode = vi_type_id[:2]
                    ecode = vi_type_id[2:6]
                    data = bm.api_get_ecId(bcode, ecode)
                    if data['code']==200:
                        vi_ec_id = data['data']
                        appdata = appNs.get_data(vi_ec_id=vi_ec_id,platformCode_id=id)
                        for appcode in appdata:
                            ns_code = appcode['ns_code']
                            vi_type_id_ns_code_list.append(ns_code)
                            if ns_code not in distinct_vi_type_id_ns_code_list:
                                distinct_vi_type_id_ns_code_list.append(ns_code)
            if vi_type_id_ns_code_list:
                rdict['vi_type_id'] =vi_type_id
                rdict['vi_type_id_ns_code_list'] = vi_type_id_ns_code_list
                vi_type_id_ns_code_list_all.append(copy.deepcopy(rdict))
                i['vi_type_id_ns_code_list'] = copy.deepcopy(rdict)
            i['adata'] = appdata
            i['idata'] = idata
            i['bdata'] = bdata
            i['edata'] = edata
            rdata.append(i)

        return self._res({'distinct_vi_type_id_ns_code_list':distinct_vi_type_id_ns_code_list,'rdata':rdata,'allmap':vi_type_id_ns_code_list_all})

class DpiPcapView:

    def __init__(self):
        self.data = {}
        self.res = {'code': 400, 'msg': '', 'data': self.data}
        self.md5 = ''
        self.save_path_name = ''
    def _res(self,data):
        if 'error' not in str(data):
            self.res['code']=200
            self.res['data']=data
        else:
            self.res['msg'] = data
        return self.res

    def getPath(self, file_obj):
        day_time = time.strftime('%Y/%m/%d/%H/%M/%S', time.localtime(time.time()))
        self.save_path = dpi_file_save_path + day_time
        self.save_path_name = self.save_path + '/' + file_obj.name
        mkdir(self.save_path, False)
        # 创建文件
        with open(self.save_path_name, 'wb') as new_file:
            for chunk in file_obj.chunks():
                new_file.write(chunk)
        # 创建文件后，计算文件md5
        self.md5 = get_md5_big(self.save_path_name)
        log.debug('file_path:{},md5:{}'.format(self.save_path_name, self.md5))

    def createPcap(self,**kwargs):

        try:
            kwargs['md5'] = self.md5
            kwargs['file_save_path_name'] = self.save_path_name
            un_vi_type_id = bm.api_analysis_vi_type_id(kwargs['vi_type_id'])
            if un_vi_type_id['code'] == 200:
                vi_data = un_vi_type_id['data']
                idata = vi_data['idata']
                bdata = vi_data['bdata']
                edata = vi_data['edata']
                identityType = idata['identityType']
                businessType = bdata['businessType']
                name = edata['name']

                if 'en' not in idata:
                    self.res['code'] = 401
                    self.res['msg'] = f'虚拟身份ID中，{identityType}'
                    return self.res
                if 'en' not in bdata:
                    self.res['code'] = 402
                    self.res['msg'] = f'虚拟身份ID中，{businessType}'
                    return self.res
                if 'en' not in edata:
                    self.res['code'] = 403
                    self.res['msg'] = f'虚拟身份ID中，{name}'
                    return self.res
                comment = f'{businessType}-{name}-{identityType}'
                in_comment = kwargs['comment']
                kwargs['comment'] = f'[{comment}]{in_comment}'
            else:
                self.res['code'] = 405
                self.res['msg'] = '业务类型编码错误'
                return self.res
            data = dp.createPcap(**kwargs)
        except Exception as e:
            log.error(e)
            data = e
        return self._res(data)

    def getAll(self,**kwargs):
        data = dp.getPcap(**kwargs)
        return self._res(data)

class MobileInfoView:
    def __init__(self):
        self.res = {'code': 400, 'msg': '', 'data': ''}
        self.md5 = ''
        self.save_path_name = ''
    def _res(self,data):
        if 'error' not in str(data):
            self.res['code']=200
            self.res['data']=data
        else:
            self.res['msg'] = data
        return self.res

    def getAll(self):
        data = mi.getInfo()
        return self._res(data)

dcv = DpiConfView()
dpv = DpiPcapView()
miv = MobileInfoView()