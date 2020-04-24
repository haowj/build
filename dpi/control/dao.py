#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
from django.db import connection
from dpi.models import *
import logging
log = logging.getLogger(__name__)


class ITC:
    def __init__(self):
        self.data = None

    def get_identity(self, **kwargs):
        try:
            if kwargs:
                self.data = IdentityTypeCoding.objects.filter(**kwargs).values()
                self.data = [i for i in self.data]
            else:
                self.data = IdentityTypeCoding.objects.values()
                self.data = [i for i in self.data]
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def alter_identity(self, ids, **kwargs):
        try:
            if kwargs:
                self.data = IdentityTypeCoding.objects.filter(id=ids).update(**kwargs)
            else:
                self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def add_identity(self, **kwargs):
        try:
            IdentityTypeCoding.objects.create(**kwargs)
            self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def del_identity(self, **kwargs):
        try:
            if kwargs:
                data = IdentityTypeCoding.objects.filter(**kwargs).delete()
                self.data = data[0]
            else:
                self.data = 0

        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)


class BT:
    def __init__(self):
        self.data = None

    def get_business(self, **kwargs):
        try:
            if kwargs:
                self.data = BusinessType.objects.filter(**kwargs).values()
                self.data = [i for i in self.data]
            else:
                self.data = BusinessType.objects.values()
                self.data = [i for i in self.data]
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)
        return self.data

    def alter_business(self, ids, **kwargs):
        try:
            if kwargs:
                self.data = BusinessType.objects.filter(id=ids).update(**kwargs)
            else:
                self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def add_business(self, **kwargs):
        try:
            BusinessType.objects.create(**kwargs)
            self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def del_business(self, **kwargs):
        try:
            if kwargs:
                data = BusinessType.objects.filter(**kwargs).delete()
                self.data = data[0]
            else:
                self.data = 0
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)


class EC:
    def __init__(self):
        self.data = None

    def get_enterprise(self, **kwargs):
        try:
            rlist = []

            if kwargs:
                data = EnterpriseCoding.objects.filter(**kwargs).values()
                for i in data:
                    typeCode_id = i['typeCode_id']
                    bdata = business.get_business(id=typeCode_id)
                    businessType= f'未找到:{typeCode_id}'
                    for b in bdata:
                        businessType = b['businessType']
                    i['businessType']=businessType
                    rlist.append(i)
                self.data = rlist
            else:
                data = EnterpriseCoding.objects.values()
                for i in data:
                    typeCode_id = i['typeCode_id']
                    bdata = business.get_business(id=typeCode_id)
                    businessType= f'未找到:{typeCode_id}'
                    for b in bdata:
                        businessType = b['businessType']
                    i['businessType']=businessType
                    rlist.append(i)
                self.data = rlist
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)
        return self.data

    def get_enterprise_by_name(self,name):
        try:
            self.data = EnterpriseCoding.objects.filter(name__contains=name).values()
            if not self.data:
                self.data = EnterpriseCoding.objects.filter(en__contains=name.upper()).values()
            if not self.data:
                self.data = EnterpriseCoding.objects.filter(code__contains=name).values()

        except Exception as e:
            log.error(e)
            self.data = f'error :{e}'
        return self.data

    def get_enterprise_last(self,**kwargs):
        try:
            self.data = EnterpriseCoding.objects.filter(**kwargs).values().order_by('-id')[:1]
            self.data = [i for i in self.data]
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def alter_enterprise(self, ids, **kwargs):
        try:
            if kwargs:
                self.data = EnterpriseCoding.objects.filter(id=ids).update(**kwargs)
            else:
                self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def add_enterprise(self, **kwargs):
        try:
            EnterpriseCoding.objects.create(**kwargs)
            self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def del_enterprise(self, **kwargs):
        try:
            if kwargs:
                data = EnterpriseCoding.objects.filter(**kwargs).delete()
                self.data = data[0]
            else:
                self.data = 0
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def get_enterprise_like_ByenterpriseType(self,typeCode_id):
        try:
            self.data = EnterpriseCoding.objects.filter(typeCode_id=typeCode_id).values()
            self.data = [i for i in self.data]
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)


class NSP:
    def __init__(self):
        self.data = None

    def get_net_safety_platform(self, **kwargs):
        try:
            if kwargs:
                self.data = NetSafetyPlatform.objects.filter(status=0, **kwargs).values()
                self.data = [i for i in self.data]
            else:
                self.data = NetSafetyPlatform.objects.filter(status=0).values()
                self.data = [i for i in self.data]
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def alter_net_safety_platform(self, ids, **kwargs):
        try:
            if kwargs:
                self.data = NetSafetyPlatform.objects.filter(id=ids).update(**kwargs)
            else:
                self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def add_net_safety_platform(self, **kwargs):
        try:
            NetSafetyPlatform.objects.create(**kwargs)
            self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)


class PT:
    def __init__(self):
        self.data = None

    def get_protocol_type(self, **kwargs):
        try:
            if kwargs:
                self.data = ProtocolType.objects.filter(status=0, **kwargs).values()
                self.data = [i for i in self.data]
            else:
                self.data = ProtocolType.objects.filter(status=0).values()
                self.data = [i for i in self.data]
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def alter_protocol_type(self, ids, **kwargs):
        try:
            if kwargs:
                self.data = ProtocolType.objects.filter(id=ids).update(**kwargs)
            else:
                self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def add_protocol_type(self, **kwargs):
        try:
            ProtocolType.objects.create(**kwargs)
            self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)


class PA:
    def __init__(self):
        self.data = None

    def get_protocol_application(self, **kwargs):
        try:
            if kwargs:
                self.data = ProtocolApplication.objects.filter(status=0, **kwargs).values()
                self.data = [i for i in self.data]
            else:
                self.data = ProtocolApplication.objects.filter(status=0).values()
                self.data = [i for i in self.data]
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def alter_protocol_application(self, ids, **kwargs):
        try:
            if kwargs:
                self.data = ProtocolApplication.objects.filter(id=ids).update(**kwargs)
            else:
                self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)

    def add_protocol_application(self, **kwargs):
        try:
            ProtocolApplication.objects.create(**kwargs)
            self.data = 1
        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)


class APP:
    def __init__(self):
        self.data = None

    def get_app_ns_data(self, **kwargs):
        cursor = connection.cursor()
        sql = """select a.a2, a.a3, a.a4, a.a5, a.a6, a.a7 from (select count(distinct e.id) as a1, e.platformCode_id as a2, e.ns_appname as a3, e.ns_code as a4, 
b.vi_type_id as a5, b.`comment` as a6, b.id as a7 from dpi_dpiconf b LEFT JOIN 
 dpi_businesstype c  on  c.`code` = left(b.vi_type_id, 2)  
left join dpi_enterprisecoding a on a.typeCode_id = c.id and a.`code` = substring(b.vi_type_id, 3, 4)
 LEFT JOIN dpi_appprocode e on e.vi_ec_id = a.id where e.ns_appname <> ''"""
        try:
            if kwargs:
                d = ''
                for k, v in kwargs.items():
                    d += ' and e.' + k + '=' + str(v) + ') a'

                cursor.execute(sql + d)
                rows = cursor.fetchall()
                self.data = [[a, b, c, d, e, f] for a, b, c, d, e, f in rows]

            else:
                cursor.execute(sql + ') a')
                rows = cursor.fetchall()
                self.data = [[a, b, c, d, e, f] for a, b, c, d, e, f in rows]


        except Exception as e:
            log.error(e)
            self.data = 'error:{}'.format(e)
    def get_data(self,**kwargs):
        try:
            if kwargs:
                self.data = AppProCode.objects.filter(**kwargs).values()
            else:
                self.data = AppProCode.objects.values()
        except Exception as e:
            self.data = f'error:{e}'
        return self.data

enterprise = EC()
identity = ITC()
business = BT()
platform = NSP()
typeCode = PT()
appCode = PA()
appNs = APP()

