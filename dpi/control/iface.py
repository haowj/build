#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
from .dao import identity, enterprise, business, platform, typeCode, appCode, appNs
from .dpi_conf_db_base import mi
import logging
log = logging.getLogger(__name__)

class bizM:
    def __init__(self):
        self.data = {}
        self.res = {'code': 400, 'msg': '', 'data': self.data}
    """ api  start"""

    def _res(self,data):
        if 'error' not in str(data):
            self.res['code'] = 200
            self.res['data'] = data
        else:
            self.res['code'] = 500
            self.res['msg'] = data
        return self.res

    def api_response(self,data=''):
        if data:
            self.data=data
        if 'error' not in str(self.data):
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_get_identity(self, **kwargs):
        identity.get_identity(**kwargs)
        self.data = identity.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_alter_identity(self, ids, **kwargs):
        identity.alter_identity(ids, **kwargs)
        self.data = identity.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_add_identity(self, **kwargs):
        identity.add_identity(**kwargs)
        self.data = identity.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_del_identity(self, **kwargs):
        identity.del_identity(**kwargs)
        self.data = identity.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_get_business(self, **kwargs):
        business.get_business(**kwargs)
        self.data = business.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_alter_business(self, ids, **kwargs):
        business.alter_business(ids, **kwargs)
        self.data = business.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_add_business(self, **kwargs):
        business.add_business(**kwargs)
        self.data = business.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_del_business(self, **kwargs):
        business.del_business(**kwargs)
        self.data = business.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_get_enterprise_like(self,typeCode_id):
        enterprise.get_enterprise_like_ByenterpriseType(typeCode_id)
        self.data = enterprise.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_get_enterprise(self, **kwargs):
        enterprise.get_enterprise(**kwargs)
        self.data = enterprise.data
        if 'error' not in str(self.data):
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_get_enterprise_last(self,**kwargs):
        enterprise.get_enterprise_last(**kwargs)
        self.data = enterprise.data
        if 'error' not in str(self.data):
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_create_enterprise(self,**kwargs):
        # 去重name
        name = kwargs['name']
        user = kwargs['user']
        en = kwargs['en']
        comment = kwargs['comment']
        typeCode_id = kwargs['typeCode_id']
        name_data = self.api_get_enterprise(name=name)
        if name_data['data']:
            self.res['code']=401
            self.res['msg']= f'企业名称[{name}]已经存在了，请换一个'
            return self.res
        # 去重en
        en_data = self.api_get_enterprise(en=en)
        if en_data['data']:
            self.res['code']=402
            self.res['msg']= f'企业英文[{en}]已经存在了，请换一个'
            return self.res
        # 检查类型是否存在
        ty_data = self.api_get_business(id=typeCode_id)
        if not ty_data['data']:
            self.res['code'] = 403
            self.res['msg'] =  f'业务类型[{typeCode_id}]不存在了，请换添加该业务类型'
            return self.res
        # 计算code使用
        data = self.api_get_enterprise_last(typeCode_id=typeCode_id)
        if data['data']:
            last_code = data['data'][0]['code']
        else:
            last_code = ''
        if last_code:
            add = 1
            while True:
                new_code = int(last_code)+add
                add +=1
                if len(str(new_code))==1:
                    bw = '000'
                elif len(str(new_code))==2:
                    bw = '00'
                elif len(str(new_code))==3:
                    bw = '0'
                else:
                    bw = ''

                # 去重code
                new_code_str = f'{bw}{new_code}'
                code_data = self.api_get_enterprise(code=new_code_str,typeCode_id=typeCode_id)
                if not code_data['data']:
                    break
        else:
            new_code_str = '0001'
        enterprise.add_enterprise(name=name.strip(),en=str(en).strip().upper(),code=new_code_str,typeCode_id=typeCode_id,comment=comment,user=user)
        return self.api_response(enterprise.data)

    def api_alter_enterprise(self, ids, **kwargs):
        enterprise.alter_enterprise(ids, **kwargs)
        self.data = enterprise.data
        if 'error' not in str(self.data):
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_add_enterprise(self, **kwargs):
        enterprise.add_identity(**kwargs)
        self.data = enterprise.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_del_enterprise(self, **kwargs):
        enterprise.del_identity(**kwargs)
        self.data = enterprise.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_analysis_vi_type_id(self,vi_type_id:str)->dict:
        bt = vi_type_id[:2]
        ec = vi_type_id[2:6]
        ic = vi_type_id[6:]

        idata = {'code':ic,'identityType':'身份类型编码错误'}
        business.get_business(code=bt)
        bdata = business.data
        edata = {'code':ec,'name':'应用类型编码错误'}
        if 'error' not in bdata:
            if bdata:
                bdata = bdata[0]
                enterprise.get_enterprise(code=ec, typeCode_id=bdata['id'])
                edata = enterprise.data
                if 'error' not in edata:
                    if edata:
                        edata = edata[0]
                        identity.get_identity(code=ic)
                        idata = identity.data
                        if 'error' not in idata and idata:
                                idata = idata[0]
                        else:
                            idata = {'code':ic,'identityType':'身份类型编码错误'}
                    else:
                        edata = {'code':ec,'name':'应用类型编码错误'}
                else:
                    edata = {'code':ec,'name':'应用类型编码错误'}

            else:
                bdata = {'code':bt,'businessType':'业务类型编码错误'}

            rdata = {'idata':idata,'bdata':bdata,'edata':edata}
            self.res['data']=rdata
            self.res['code']=200
        else:
            self.res['msg'] ='业务类型编码错误'
        log.debug(self.res)
        return self.res

    def api_get_ecId(self,bcode,ecode):
        eid = ''
        self.data = business.get_business(code=bcode)
        for i in self.data:
            bid = i['id']
            edata = enterprise.get_enterprise(code=ecode,typeCode_id=bid)
            for j in edata:
                eid = j['id']
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = eid
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_get_platform(self, **kwargs):
        platform.get_net_safety_platform(**kwargs)
        self.data = platform.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_alter_platform(self, ids, **kwargs):
        platform.alter_net_safety_platform(ids, **kwargs)
        self.data = platform.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_add_platform(self, **kwargs):
        platform.add_net_safety_platform(**kwargs)
        self.data = platform.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_get_pt(self, **kwargs):
        typeCode.get_protocol_type(**kwargs)
        self.data = typeCode.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_alter_pt(self, ids, **kwargs):
        typeCode.alter_protocol_type(ids, **kwargs)
        self.data = typeCode.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_add_pt(self, **kwargs):
        typeCode.add_protocol_type(**kwargs)
        self.data = typeCode.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_get_pa(self, **kwargs):
        appCode.get_protocol_application(**kwargs)
        self.data = appCode.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_alter_pa(self, ids, **kwargs):
        appCode.alter_protocol_application(ids, **kwargs)
        self.data = appCode.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_add_pa(self, **kwargs):
        appCode.add_protocol_application(**kwargs)
        self.data = appCode.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_alter_app_ns_data(self, ids, **kwargs):
        appNs.alter_app_ns_data(ids, **kwargs)
        self.data = appNs.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_add_app_ns_data(self, **kwargs):
        appNs.add_app_ns_data(**kwargs)
        self.data = appNs.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_dpi_ns_vi(self, **kwargs):
        appNs.get_app_ns_data(**kwargs)
        self.data = appNs.data
        if 'error' not in self.data:
            self.res['code'] = 200
            self.res['data'] = self.data
        else:
            self.res['code'] = 500
            self.res['msg'] = self.data
        return self.res

    def api_get_ec_bt(self,name):
        try:
            rlist = []
            edata = enterprise.get_enterprise_by_name(name)
            for i in edata:
                typeCode_id = i['typeCode_id']
                bdata = business.get_business(id=typeCode_id)
                businessType='未找到'
                bcode='未找到'
                for b in bdata:
                    businessType=b['businessType']
                    bcode=b['code']
                i['businessType']=businessType
                i['bcode']=bcode
                rlist.append(i)
        except Exception as e:
            rlist = f'error:{e}'
        return self._res(rlist)


bm = bizM()
