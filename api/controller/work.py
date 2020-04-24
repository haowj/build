# coding:utf-8
__author__ = 'xcma'
from appack.models import *
from appack.helper.git import *
from appack.helper.misc import *
import logging
import requests
import pymysql
from appack.conf.path import get_path_day_time, base_save_file_path, connector_project_path, supertack_file_path_name, \
    superctl_file_path_name, workplace_path

log = logging.getLogger(__name__)


class packageConfig:

    def getVersionContorl(self, id):
        data = version_contorl.objects.filter(id=id).values().get()
        self.id = data['id']
        self.dev_model_id = data['dev_model_id']
        self.superctl_version_id = data['superctl_version_id']
        self.supertack_version_id = data['supertack_version_id']
        self.superd_version_id = data['superd_version_id']
        self.superdcf_version_id = data['superdcf_version_id']
        self.rom_version = data['rom_version']
        self.docking_solution = data['docking_solution']
        self.pack_type = data['pack_type']
        self.package_contains_path = data['package_contains_path']
        self.package_contains_path_type = data['package_contains_path_type']
        self.user = data['user']
        self.comment = data['comment']
        self.create_time = data['create_time']
        self.update_time = data['update_time']
        self.dev_model = self.getDevModeInfo()['zy_model']
        return data

    def getDevModeInfo(self):
        data = ''
        if self.dev_model_id:
            data = dev_model_db.objects.filter(id=self.dev_model_id).values().get()
        return data

    def getSuperctlInfo(self):
        try:
            if self.superctl_version_id != '0':
                data = superctlVersion.objects.filter(id=self.superctl_version_id).values().get()
            else:
                ddata = superctlVersion.objects.filter(dev_model=self.dev_model).values().order_by(
                    'update_time').first()
                fdata = superctlVersion.objects.filter(dev_model='fitall').values().order_by('update_time').first()
                if ddata and fdata:
                    did = int(ddata['id'])
                    fid = int(fdata['id'])
                    if did > fid:
                        data = ddata
                    else:
                        data = fdata
                elif ddata:
                    data = ddata
                else:
                    data = fdata
            return data
        except Exception as e:
            log.error(e)

    def getSupertackInfo(self):
        try:
            if self.supertack_version_id != '0':
                data = supertackVersion.objects.filter(id=self.supertack_version_id).values().get()
            else:
                ddata = supertackVersion.objects.filter(dev_model=self.dev_model).values().order_by(
                    'update_time').first()
                fdata = supertackVersion.objects.filter(dev_model='fitall').values().order_by('update_time').first()
                if ddata and fdata:
                    did = int(ddata['id'])
                    fid = int(fdata['id'])
                    if did > fid:
                        data = ddata
                    else:
                        data = fdata
                elif ddata:
                    data = ddata
                else:
                    data = fdata
            return data
        except Exception as e:
            log.error(e)

    def getSuperdInfo(self):

        try:
            if self.superd_version_id != '0':
                data = superdVersion.objects.filter(id=self.superd_version_id).values().get()
            else:
                data = superdVersion.objects.filter(dev_model=self.dev_model).values().order_by('update_time').first()
            return data
        except Exception as e:
            log.error(e)

    def getSuperdcfInfo(self):

        try:
            if self.superdcf_version_id != '0':
                data = superdcfVersion.objects.filter(id=self.superdcf_version_id).values().get()
            else:
                data = superdcfVersion.objects.filter(dev_model=self.dev_model,
                                                      type=self.package_contains_path_type).values().order_by(
                    'update_time').first()
            return data
        except Exception as e:
            log.error(e)

    def getconnectorInfo(self):
        if self.package_contains_path_type == 'c_sapiloader':
            data = self.getSupertackInfo()
        else:
            data = self.getSuperctlInfo()
        return data

    def getPackageConfigInfo(self, id):
        try:
            self.getVersionContorl(id)
            info = {}
            info['id'] = self.id
            info['dev_model_info'] = self.getDevModeInfo()
            info['superd_info'] = self.getSuperdInfo()
            info['superdcf_info'] = self.getSuperdcfInfo()
            info['connector_info'] = self.getconnectorInfo()
            info['user'] = self.user
            info['comment'] = self.comment
            info['create_time'] = self.create_time
            info['update_time'] = self.update_time
            info['rom_version'] = self.rom_version
            info['docking_solution'] = self.docking_solution
            info['pack_type'] = self.pack_type
            info['package_contains_path'] = self.package_contains_path
            info['package_contains_path_type'] = self.package_contains_path_type
            return info
        except Exception as e:
            log.error(e)


class connector:

    def __init__(self):
        self.package_path = base_save_file_path + 'connector/{}'.format(get_path_day_time())

    def gitCode(self, tag, branch='master'):
        try:
            git = git_process(connector_project_path)
            if 'RC' == tag:
                git.pull()
            else:
                git._init_directoy(branch)
                git.reset_tag(tag)
        except Exception as e:
            log.error(e)

    def cp_file(self, connector_type):
        try:
            if connector_type == 'c_sapiloader':
                connector_file_path_name = supertack_file_path_name
            elif connector_type == 'shell_sapiloader':
                connector_file_path_name = superctl_file_path_name
            else:
                connector_file_path_name = ''
            self.md5 = getMd5(connector_file_path_name)
            res = cp(connector_file_path_name, self.package_path)
            return res
        except Exception as e:
            log.error(e)
            return False

    def record_connector(self, dev_model, connector_type, tag, user, comment, md5):
        try:
            log.debug(
                'dev_model:{},connector_type:{},tag:{},user:{},comment:{},md5:{}'.format(dev_model, connector_type, tag,
                                                                                         user, comment, md5))
            if connector_type == 'c_sapiloader':
                file_name = self.package_path + 'supertack'

                obj, created = supertackVersion.objects.update_or_create(
                    defaults={'dev_model': dev_model, 'user': user, 'comment': comment, 'supertack_version': tag,
                              'supertack_file': file_name}, md5=md5)
                log.debug('{},{}'.format(obj, created))
            elif connector_type == 'shell_sapiloader':
                file_name = self.package_path + 'superctl'
                obj, created = superctlVersion.objects.update_or_create(
                    defaults={'dev_model': dev_model, 'user': user, 'comment': comment, 'superctl_version': tag,
                              'superctl_file': file_name}, md5=md5)
            else:
                created = 'record_connector'
                log.error('record_connector error  connector_type:{}'.format(connector_type))
            if created:
                log.debug('新增')
            else:
                log.debug('更新')
            return True
        except Exception as e:
            log.error(e)
            return False

    def connector_add(self, tag, dev_model, connector_type, comment, user):
        try:
            connector_type = 'c_sapiloader'
            self.gitCode(tag)
            self.cp_file(connector_type)
            res = self.record_connector(dev_model, connector_type, tag, user, comment, self.md5)
            return res
        except Exception as e:
            log.error(e)
            return False


class register_auth:
    from api.controller.pymysql import Mysql
    ms = Mysql()
    def getRid(self,dev_model,sn):
        try:
            sql = 'select * from zjzy_ap where sn="{}"'.format(sn)
            data = self.ms.getquery(sql)[0]
            if data:
                model_id = data['model_id']
                sql = 'select * from zjzy_ap_model where id="{}"'.format(model_id)
                mdata = self.ms.getquery(sql)[0]
                dev_model_sn=mdata['name']
                log.debug(data)
                if dev_model==dev_model_sn:
                    return data['rid']
                else:
                    return 0
            else:
                return 400
        except Exception as e:
            log.error(e)

    def setAuth(self,sn,dev_model,result):
        """
        "http://172.16.65.126:5003/pre-filter/update" -H "Content-Type: text/json" -d
        '{"TYPE":"PRE-FILTER_UPDATE", "DATA":[{"SN":"0010099900E08200SY0K18D2252FC217", "MODEL":"MR820","RID":32266,"ACCESS":true}]}'
        :return:
        """
        log.debug('sn:{},dev_model:{},result:{}'.format(sn,dev_model,result))
        try:
            rid = self.getRid(dev_model,sn)
            log.debug('rid:{}'.format(rid))
            if rid:
                url = 'http://47.96.16.60:5003/pre-filter/update'
                params={"TYPE":"PRE-FILTER_UPDATE", "DATA":[{"SN":str(sn), "MODEL":str(dev_model),"RID":rid,"ACCESS":bool(result)},]}
                log.debug(params)
                headers={"Content-Type": "text/json"}
                data = requests.request('POST',url,json=params,headers=headers,timeout=10)
                log.debug(data)
                try:
                    data=data.json()
                    code=200
                except:
                    data=data.text
                    code=500
            elif rid==0:
                data='SN与设备型号不匹配'
                code=501
            else:
                data = 'SN为找打'
                code = 502
        except Exception as e:
            code=503
            data = e
            log.error(e)
        data = {'data':str(data),'code':code}
        log.debug('data:{}'.format(data))
        return data

