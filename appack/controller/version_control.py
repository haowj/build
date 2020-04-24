# coding:utf-8
import requests

__author__ = 'xcma'
import logging

log = logging.getLogger(__name__)
from appack.models import *
from proxy.models import proxyVersion
from appack.helper.git import git_process
from appack.helper.misc import *
from django.db.models import Q
from appack.conf.path import *
from appack.conf.config import *
from appack.controller.support_api import supportApi
from appack.controller.ap_api import ap_api
sapi = supportApi()
class base:
    def get_tag_list(self,type):
        if 'superd' in type:
            project_path = superd_project_path
        elif 'connector' in type:
            project_path = connector_project_path
        elif 'sapiloader' in type:
            project_path = sapiloader_c_project_path
        else:
            project_path = ''
            log.error('type[{}] is not found'.format(type))
        git = git_process(project_path)
        tag_list = git.getTagList()[:50]
        tag_list.insert(0,'RC')
        return tag_list

    def record_build_log(self,dev_model,user,build_result,tag,reason,status,type):
        build_log.objects.update_or_create(defaults={'time_stamp':time_stamp(),'user':user,'build_result':build_result,'build_status':status,'build_reason':reason},dev_model=dev_model,build_tag=tag,type=type)

    def get_dev_model(self):
        data = dev_model_db.objects.values('zy_model')
        ldata = []
        for i in data:
            ldata.append(i['zy_model'])
        return ldata

    def get_dev_model_all(self):
        data = dev_model_db.objects.values('id','zy_model').order_by('-update_time')
        return data

    def map_devmodel(self, dev_model):
        """
        由于cbild.sh 文件写的是非标准型号，故需要做个映射进行适配,如果不需要映射则原样输出
        :return:
        """
        data = map_dev_model_db.objects.filter(dev_model=dev_model).values().order_by('-id').first()
        if data:
            map_dev_model=data['map_dev_model']
            log.debug('dev_model:{}  map_dev_model:{}'.format(dev_model,map_dev_model))
        else:
            log.warning('未找到该型号【{}】的map关系,将使用原始型号进行构建'.format(dev_model))
            map_dev_model=dev_model
        return map_dev_model

    def get_tag_code(self,path,tag,branch):
        """
        拉取指定tag的代码，
        :return:
        """
        try:
            git = git_process(path)
            git._init_directoy(branch)
            if 'RC' not in tag:
                git.reset_tag(tag)
                log.debug('拉取指定tag：{}的代码,完成'.format(tag))
                getProjectGitTag(path)
                git.active_branch()
        except Exception as e:
            log.error(e)

    def clear_path(self,build_save_path,save_path,build_shell_path_name,tag):
        try:
            taget_save_path = base_path + save_path
            cmd = 'rm -rf {}'.format(build_save_path + 'superd')
            cmd2 = 'rm -rf {}'.format(build_save_path + 'sapiloader')
            log.debug('执行清空构建输出路径:{},{}'.format(cmd,cmd2))
            cmd1 = 'rm -rf {}'.format(taget_save_path)
            log.debug('执行清空存放路径:{}'.format(cmd))

            for i in [cmd, cmd1,cmd2]:
                executionShell(i)
            chmod_file(build_shell_path_name)
            log.debug('授权文件:{}'.format(build_shell_path_name))
            if 'sapi_loader' in build_shell_path_name:
                change_version = "sed -i 's/\"v1.5\"/\"{}\"/g' config.h".format(tag)
                build_shell_path = sapiloader_c_build_shell_path
                change = 1
            else:
                change_version = "sed -i 's/\"superd_version\"/\"{}\"/g' config.h".format(tag)
                build_shell_path = superd_build_shell_path
                change = 0
            if change:
                executionShell(change_version, build_shell_path)
                # executionShell('cat config.h', build_shell_path)
                log.debug('修改config.h文件:{}'.format(change_version))
            else:
                log.debug('不修改config.h文件:{}'.format(change_version))
        except Exception as e:
            log.error(e)
            raise e

    def build(self,map_dev_model,dev_model,user,tag,reason,type):
        # map_dev_model 是映射的型号名称，即cbuild文件中的型号名称，这个型号名称有的是型号名称本身，有的是编译链简称，有的是型号名称小写
        status = 400
        try:
            cmd = './cbuild.sh {} 2>&1'.format(map_dev_model)
            if 'superd' in type:
                build_shell_path = superd_build_shell_path
            else:
                build_shell_path = sapiloader_c_build_shell_path

            log.debug('构建{}:{}，路径：{}'.format(type, cmd, build_shell_path))
            plug_name = ''
            str_sign = '1'
            if 'superd' in type:
                plug_name = 'superd'
                str_sign = 'All ok! Output:{}'.format(plug_name)
            elif 'sapiloader' in type:
                plug_name = 'sapiloader'
                str_sign = 'All ok! Output:{}'.format(plug_name)
            build_data = executionShell(cmd,build_shell_path,20)

            try:
                for data in build_data[-20:]:
                    try:
                        if str_sign in data:
                            status =200
                    except:
                        pass
                log.debug('判断是否构建成功添加：{}'.format(plug_name))
                log.debug('{}-{}-构建结果：{}'.format(type,dev_model,status))
            except Exception as e:
                log.error(e)
            finally:
                self.record_build_log(dev_model,str(user),build_data,tag,reason,status,type)
        except Exception as e:
            log.error(e)
        return status

    def _init_code(self,project_path,branch):
        git = git_process(project_path)
        git._init_directoy(branch)

    def init_project(self,project_path):
        git = git_process(project_path)
        git.init_project()

    def mv_plug(self, dev_model,user, tag, reason,type,build_save_path,save_path,build_type=None,map_dev_model=''):
        """
        找到该版本构建成功的superd文件,并移动到指定路径下
        :param dev_model:
        :return:
        """
        try:
            if 'superd' in type:
                plug_name = 'superd'
            elif 'sapiloader' in type:
                plug_name = 'sapiloader'
            elif 'proxy' in type:
                "rproxy_mr820.tar.gz"
                plug_name='rproxy_{}.tar.gz'.format(map_dev_model)
            else:
                plug_name = type
            target_save_path = base_path + save_path
            log.debug('指定型号{}:{}'.format(dev_model,type))
            # 这是去构建后指定目录中查找构建完毕的文件
            # file_path = build_save_path + map_dev_model + '/' + plug_name
            # 直接在当前构建路径获取构建结果
            file_path = build_save_path + plug_name

            log.debug('{}生成路径：{}'.format(type,file_path))
            build_status = 0
            build_result = '未找到:{}'.format(plug_name)
            save_path_name = target_save_path + plug_name
            mkdir(target_save_path)
            if file_is_have(file_path):
                cmd = 'mv {} {}'.format(file_path, target_save_path)
                log.debug('移动{}到指定路径,from:{},target:{}'.format(plug_name,file_path, target_save_path))
                executionShell(cmd)
                build_result = '失败'
                build_status = -1
                if file_is_have(save_path_name):
                    build_result = '成功'
                    build_status = 1
            log.debug('{}移动{}:{}'.format(plug_name,build_result, build_status))
            if build_status == 1:
                durl = plug_domain+save_path+plug_name
                self.record_plug_info(type,dev_model, durl,user, tag, reason,save_path_name,build_result,build_status,build_type)
            return build_status
        except Exception as e:
            log.error(e)

    def record_plug_info(self, type,dev_model,durl, user, tag, reason,save_path_name,build_result,build_status,build_type):
        log.debug('开始记录{}_info'.format(type))
        try:
            md5 = get_md5_big(save_path_name)
            if 'superd' in type:
                superdVersion.objects.update_or_create({'time_stamp':time_stamp(),'download_url':durl,'user':str(user),'superd_file':save_path_name,
                                                        'md5':md5, 'build_reason':str(reason),'build_result':build_result, 'build_status':build_status
                },dev_model=dev_model, superd_version=tag,build_type=build_type)
            elif 'spailoader' in type:
                sapiloaderCVersion.objects.update_or_create({'download_url':durl,'user':str(user),'sapiloaderC_file':save_path_name, 'md5':md5, 'build_reason':str(reason),'build_result':build_result, 'build_status':build_status},dev_model=dev_model, sapiloaderC_version=tag)
            elif 'proxy' in type:
                a=[type,dev_model,durl, user, tag, reason,save_path_name,build_result,build_status,build_type]
                log.debug(a)
                proxyVersion.objects.update_or_create({'download_url':durl,'user':str(user),'proxy_file':save_path_name, 'md5':md5, 'build_reason':str(reason),'build_result':build_result, 'build_status':build_status},dev_model=dev_model, proxy_version=tag)
            else:
                log.error('type：{},未找到该类型')
            log.debug('构建{}信息记录完成'.format(type))

        except Exception as e:
            log.error(e)

    def get_build_is_complate(self,dev_model,tag,reason,user,type):
        """
        查看指定目录中是否有type文件
        :return:
        """
        build_time_stamp = 0
        now_time_stamp = time_stamp()
        try:

            try:
                data = build_log.objects.filter(type=type,dev_model=dev_model,build_tag=tag,build_reason=reason,user=user).values('dev_model','build_tag','time_stamp','build_status').order_by('-id').first()
                log.debug('build_log:{}'.format(data))
                build_status=int(data['build_status'])
                build_time_stamp=int(data['time_stamp'])
                res = abs(now_time_stamp-build_time_stamp)
                if res>60:
                    build_status=0
                    log.debug('时间差:[{}]大于60s'.format(res))
            except:
                build_status=0

            log.debug('查找,操作人:{}，类型:{},dev_model:{},tag:{},reason:{},now_time_stamp:{},build_time_stamp:{},是否构建完成：{}'.format(user,type,dev_model,tag,reason,now_time_stamp,build_time_stamp,build_status))
            return build_status
        except Exception as e:
            log.error(e)

    def getBuildLog(self,type):
        data = build_log.objects.filter(type=type).values('id', 'dev_model', 'user', 'build_reason', 'build_tag',
                                                          'build_status', 'comment', 'update_time', 'type').order_by(
            '-update_time','-id')[:100]
        return data
class dev_model_obj:

    def getAllData(self):
        data = dev_model_db.objects.values().order_by('-id')

        all_dev_model_info_list = []
        oem_name = oem_code = ''
        for i in data:
            all_dev_model_info = {}
            dev_model_info = {}
            oem_id = i['oem_id']
            if oem_id:
                oem_info = oem_db.objects.filter(id=oem_id).values()
                for j in oem_info:
                    oem_name = str(j['oem_name'])
                    oem_code = str(j['oem_code'])
            dev_model_info['oem_name'] = oem_name
            dev_model_info['oem_code'] = oem_code
            dev_model_info['type'] = str(i['type'])
            dev_model_info['zy_model'] = str(i['zy_model'])
            dev_model_info['oem_model'] = str(i['oem_model'])
            dev_model_info['comment'] = str(i['comment'])
            dev_model_info['user'] = str(i['user'])
            dev_model_info['update_time'] = str(i['update_time'])
            all_dev_model_info[i['id']] = dev_model_info
            all_dev_model_info_list.append(all_dev_model_info)
        return all_dev_model_info_list

    def addData(self):
        model_type = ['面板AP', '桌面二合一', '三合一', '四合一', '吸顶AP', 'AC路由网关', '光猫', '嗅探光猫', '嗅探2合1']
        oem_info = oem_db.objects.values('id', 'oem_code', 'oem_name')
        return {'type': model_type, 'oem_info': oem_info}


class oem_db_obj:

    def getAllData(self):
        data = oem_db.objects.values().order_by('-id')
        return data

    def addData(self):
        model_type = ['面板AP', '桌面二合一', '三合一', '四合一', '吸顶AP', 'AC路由网关', '光猫', '嗅探光猫', '嗅探2合1']
        oem_info = oem_db.objects.values('id', 'oem_code', 'oem_name')
        return {'type': model_type, 'oem_info': oem_info}

class package_conf:
    """处理主要配置表工作"""

    def getAllData(self,dev_model_id='',id=''):
        """返回全部数据"""
        try:
            info_list = []
            if id:
                sw =1
            elif dev_model_id:
                sw=2
            else:
                sw=0

            if sw==1:
                data = version_contorl.objects.filter(id=id).values()
            elif sw==2:
                data = version_contorl.objects.filter(dev_model_id=dev_model_id).values().order_by('-update_time')
            else:
                data = version_contorl.objects.values().order_by('-update_time')
            if data:
                for i in data:
                    info = {}
                    # log.debug(i)
                    for k, v in i.items():
                        # log.debug('{}-{}'.format(k,v))
                        if k == 'dev_model_id':
                            k = 'dev_model'
                            try:
                                info['oem_name'] = dev_model_db.objects.get(id=v).oem_name
                                v = dev_model_db.objects.get(id=v).zy_model
                            except:
                                pass

                        elif k == 'supertack_version_id' and v:
                            k = 'connector_version'
                            try:
                                if v == '0':
                                    v= '默认最新'
                                else:
                                    v = supertackVersion.objects.get(id=v).supertack_version
                            except:
                                pass
                        elif k == 'superctl_version_id' and v:
                            k = 'connector_version'
                            try:
                                if v == '0':
                                    v= '默认最新'
                                else:
                                    v = superctlVersion.objects.get(id=v).superctl_version
                            except:

                                pass
                        elif k == 'superdcf_version_id' and v:
                            k = 'superdcf_version'
                            try:
                                if v == '0':
                                    v= '默认最新'
                                else:
                                    v = superdcfVersion.objects.get(id=v).superdcf_version
                            except:
                                pass
                        elif k == 'superd_version_id' and v:
                            k = 'superd_version'
                            try:
                                if v == '0':
                                    v= '默认最新'
                                else:
                                    v = superdVersion.objects.get(id=v).superd_version
                            except:
                                pass
                        elif k == 'zdpi_sig_version_id' and v:
                            k = 'zdpi_sig_version'
                            try:
                                if v == '0':
                                    v= '默认最新'
                                else:
                                    v = dpiConfigVersion.objects.get(id=v).zdpi_sig_version
                            except:
                                pass

                        info[k] = v
                    info_list.append(info)
            # log.debug(info_list)
            return info_list
        except Exception as e:
            log.error(e)

    def getIdAp_model(self):
        data = dev_model_db.objects.values('id', 'zy_model').order_by('-id')
        return data

    def add(self, **kwargs):
        res = version_contorl.objects.create(kwargs)
        return res

    def getallVersionData(self):
        sc = superdcf()
        sl = sapiloader()
        slc = sapiloaderC()
        st = superctl()
        stack = supertack()
        sd = superd()
        data = {
            'dev_model': self.getIdAp_model(),
            # 'superctl': st.getIdVersion(),
            # 'supertack': stack.getIdVersion(),
            # 'sapiloader': sl.getIdVersion(),
            # 'sapiloaderC': slc.getIdVersion(),
            # 'superdcf': sc.getIdVersion(),
            # 'superd': sd.getIdVersion(),
            'package_contains_path': package_contains_path_dict,
            'docking_solution': docking_solution,
        }
        return data

class superctl:
    """处理superctl配置工作"""

    def getAllData(self):
        data = superctlVersion.objects.values().order_by('-id')
        return data

    def getIdVersion(self):
        data = superctlVersion.objects.values('id', 'superctl_version', 'comment').order_by('-id')
        return data

    def add(self, **kwargs):
        res = superctlVersion.objects.create(kwargs)
        return res

class sapiloader:
    """处理sapiloader配置工作"""

    def getAllData(self):
        data = sapiloaderVersion.objects.values().order_by('-update_time','-id')
        return data

    def getIdVersion(self):
        data = sapiloaderVersion.objects.values('id', 'sapiloader_version', 'comment').order_by('-id')
        return data

    def add(self, **kwargs):
        res = sapiloaderVersion.objects.create(kwargs)
        return res

class sapiloaderC(base):
    """处理sapiloader配置工作"""

    def getAllData(self):
        self._init_code(sapiloader_c_project_path,'master')
        data = sapiloaderCVersion.objects.values().order_by('-id')[:10]
        return data

    def getIdVersion(self):
        data = sapiloaderCVersion.objects.values('id', 'sapiloaderC_version','dev_model').order_by('-id')
        return data

    def add(self, **kwargs):
        res = sapiloaderCVersion.objects.create(kwargs)
        return res

class sapiloaderC_build(base):

    def __init__(self):
        self.type = 'sapiloader'
        self.branch = config_branch['sapiloader_branch']
    def Build(self, dev_model, tag, reason, user):

        self.package_path = 'upload/sapiloaderc/{}'.format(get_path_day_time())
        type = self.type
        map_dev_model = self.map_devmodel(dev_model)
        self.get_tag_code(sapiloader_c_project_path, tag,self.branch)
        self.clear_path( sapiloader_c_build_shell_path, self.package_path, sapiloader_c_build_shell_path_name,
                        tag)
        self.build(map_dev_model, dev_model, user, tag, reason, type)
        # 这里的dev_model 必须使用原始的，因为需要入库展示使用。
        build_status = self.mv_plug( dev_model, user, tag, reason, type, sapiloader_c_build_shell_path,
                                     self.package_path)
        self._init_code(sapiloader_c_project_path,self.branch)
        return build_status

    def toBuild(self, dev_model, tag, reason, user):
        import threading
        t1 = threading.Thread(target=self.Build, args=(dev_model, tag, reason, str(user)))
        t1.start()
        return 1

    def get_sapiloader(self, dev_model, tag, reason, user):
        type = self.type
        return self.get_build_is_complate(dev_model, tag, reason, user, type)

class superd(base):
    def getAllData(self,branch='',build_type=None):
        if not branch:
            branch = config_branch['superd_branch']
        git = git_process(superd_project_path)
        git._init_directoy(branch)
        if build_type=='test':
            data = superdVersion.objects.filter(build_type=build_type).values().order_by('-update_time','-id')[:100]
        else:
            data = superdVersion.objects.exclude(build_type='test').values().order_by('-update_time','-id')[:100]
        return data

    def getIdVersion(self):
        data = superdVersion.objects.values('id', 'dev_model', 'superd_version').order_by('-id')
        return data

    def add(self, **kwargs):
        res = superdVersion.objects.create(kwargs)
        return res

class superd_build(base):

    def __init__(self):
        self.type = 'superd'
        self.branch = config_branch['superd_branch']
        self.build_type = 'release'

    def Build(self, dev_model, tag, reason, user,branch=None):
        # 构建完成后，包存放的路径
        package_path = 'upload/superd/{}'.format(get_path_day_time())

        log.debug('start_build:{},tag:{},reason:{},user:{}'.format(dev_model,tag,reason,user))
        type = self.type
        map_dev_model = self.map_devmodel(dev_model)
        if branch:
            self.branch = branch
            type='superd_test'
            self.build_type = 'test'
        self.get_tag_code(superd_project_path, tag,self.branch)
        self.clear_path(superd_build_save_path, package_path, superd_build_shell_path_name,
                        tag)
        self.build(map_dev_model, dev_model, user, tag, reason, type)
        # 这里的dev_model 必须使用原始的，就是设备的正常型号而不是cbuild中写的，因为需要入库展示使用。
        build_status = self.mv_plug(dev_model,user, tag, reason, type, superd_build_shell_path,
                                    package_path,self.build_type)
        self._init_code(superd_project_path,self.branch)

        return build_status

    def toBuild(self, dev_model, tag, reason, user):
        import threading
        t1 = threading.Thread(target=self.Build, args=(dev_model, tag, reason, str(user)))
        t1.start()
        return 1

    def toBuild_test(self, dev_model, branch, reason, user,tag='RC'):
        import threading
        t1 = threading.Thread(target=self.Build, args=(dev_model, tag, reason, str(user),branch))
        t1.start()
        return 1

    def get_superd(self, dev_model, tag, reason, user,is_test=None):
        type = self.type
        if is_test:
            type='superd_test'
        return self.get_build_is_complate(dev_model, tag, reason, user, type)

class superdcf:
    """处理superdcf配置工作"""

    def getAllData(self):
        data = superdcfVersion.objects.values().order_by('-update_time')
        return data

    def getIdVersion(self):
        data = superdcfVersion.objects.values('id', 'superdcf_version', 'comment').order_by('-id')
        return data

    def add(self, **kwargs):
        res = superdcfVersion.objects.create(kwargs)
        return res
class zdpi_config:

    def getDevModel(self):
        data = dev_model_db.objects.values()
        return data

    def getAllData(self):
        data = dpiConfigVersion.objects.values()
        return data

class supertack(base):
    """处理supertack配置工作"""

    def getAllData(self):
        data = supertackVersion.objects.values().order_by('-update_time')
        return data

    def getIdVersion(self):
        supertackVersion.objects.filter(id >= 2).count('')
        data = supertackVersion.objects.values('id', 'supertack_version', 'comment').order_by('-id')
        return data

    def add(self, **kwargs):
        res = supertackVersion.objects.create(kwargs)
        return res
class package(base):
    def getAllData(self):
        data = pack_list_contorl.objects.values('id','dev_model','download_url','superd_version','package_contains_path','pack_type','user','update_time').order_by('-update_time')[:10]
        return data
    def getSapiloaderData(self):
        data = sapiloader_pack.objects.values().order_by('-update_time')[:10]
        return data
    def getproxyData(self):
        from proxy.models import proxyVersion
        data = proxyVersion.objects.values().order_by('-update_time')[:10]
        return data

    def add(self, **kwargs):
        res = pack_list_contorl.objects.create(kwargs)
        return res

    def getAllPackConf(self):
        pc = package_conf()
        self.pack_conf_data = pc.getAllData()
        return self.pack_conf_data

    def getConfigInfo(self, pack_conf_id,reason,user):
        try:
            superdcf_version = ''
            connector_version = ''
            superdcf_path = ''
            connector_path = ''
            pack_conf = version_contorl.objects.filter(id=pack_conf_id)
            for i in pack_conf:
                zy_model = dev_model_db.objects.filter(id=i.dev_model_id).get().zy_model
                if i.superd_version_id != '0':
                    superd_data = superdVersion.objects.filter(id=i.superd_version_id).get()
                    superd_path = superd_data.superd_file
                    superd_version = superd_data.superd_version
                else:
                    superd_version = ''
                    superd_path = ''
                status = self.pack_superd_build(zy_model,reason,user,superd_version)
                # status = 200
                log.debug('superd_version_id:{},superdcf_version_id:{},zy_model:{}'.format(i.superd_version_id,i.superdcf_version_id,zy_model))
                if status==200:
                    try:
                        log.debug('开始匹配插件')
                        if i.superd_version_id == '0':
                            # 如果id=0，此时取最新插件值
                            superd_data=superdVersion.objects.filter(dev_model=zy_model).values().order_by('-update_time').first()
                            superd_path = superd_data['superd_file']
                            superd_version = superd_data['superd_version']
                        # else:
                        #     superd_data = superdVersion.objects.filter(id=i.superd_version_id).get()
                        #     superd_path = superd_data.superd_file
                        #     superd_version = superd_data.superd_version
                    except Exception as e:
                        log.error(e)
                        raise e

                    log.debug('开始匹配连接器')
                    superctl = i.superctl_version_id
                    supertack = i.supertack_version_id
                    c_sapiloader = 'c_sapiloader'
                    shell_sapiloader = 'shell_sapiloader'
                    try:
                        log.debug('superctl:{};supertack:{}'.format(superctl,supertack))
                        if superctl=='0':
                            connector_type= shell_sapiloader
                            try:
                                ddata = superctlVersion.objects.filter(dev_model=zy_model).values().order_by('-update_time').first()
                                fdata = superctlVersion.objects.filter(dev_model='fitall').values().order_by('-update_time').first()
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
                                connector_path = data['superctl_file']
                                connector_version = data['superctl_version']
                            except Exception as e:
                                log.error(e)
                        elif superctl:
                            connector_type= shell_sapiloader
                            connector_data = superctlVersion.objects.filter(id=superctl).get()
                            connector_path = connector_data.superctl_file
                            connector_version = connector_data.superctl_version
                        elif supertack=='0':
                            connector_type= c_sapiloader

                            try:
                                ddata = supertackVersion.objects.filter(dev_model=zy_model).values().order_by('-update_time').first()
                                fdata = supertackVersion.objects.filter(dev_model='fitall').values().order_by('-update_time').first()
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
                                connector_path = data['supertack_file']
                                connector_version = data['supertack_version']
                            except Exception as e:
                                log.error(e)
                        elif supertack:
                            connector_type= c_sapiloader

                            connector_data = supertackVersion.objects.filter(id=supertack).get()
                            connector_path = connector_data.supertack_file
                            connector_version = connector_data.supertack_version

                        else:
                            connector_type= 'None'
                            connector_data = 'connector not found'
                            log.error(connector_data)
                            raise connector_data
                        try:
                            log.debug(f'开始匹配插件配置文件:{zy_model}-{connector_type}')
                            if i.superdcf_version_id == '0':
                                try:
                                    sddata = superdcfVersion.objects.filter(dev_model=zy_model,type=connector_type).values().order_by(
                                        '-update_time').first()
                                    log.debug(sddata)
                                    sfdata = superdcfVersion.objects.filter(dev_model='fitall',type=connector_type).values().order_by(
                                        '-update_time').first()
                                    # 如果该型号存在配置文件，则优先取配置的，否则取默认的
                                    if sddata:
                                        superdcf_data = sddata
                                    else:
                                        superdcf_data = sfdata
                                    superdcf_path = superdcf_data['superdcf_file']
                                    superdcf_version = superdcf_data['superdcf_version']
                                except Exception as e:
                                    log.error(e)
                                    log.error('未找到该【{}】型号的配置文件'.format(zy_model))
                            else:
                                superdcf_data = superdcfVersion.objects.filter(id=i.superdcf_version_id).get()
                                superdcf_path = superdcf_data.superdcf_file
                                superdcf_version = superdcf_data.superdcf_version
                        except Exception as e:
                            log.error(e)
                            raise e
                    except Exception as e:
                        log.error(e)
                        raise e
                    log.debug('开始匹配DPI配置文件')
                    zdpi_sig_version_id = i.zdpi_sig_version_id

                    try:
                        if zdpi_sig_version_id=='0':
                            try:
                                log.debug('取型号【{}】最新的DPI配置'.format(zy_model))
                                if dpiConfigVersion.objects.filter(dev_model=zy_model).count()>0:
                                    zdpi_data = dpiConfigVersion.objects.filter(dev_model=zy_model).values().order_by('-update_time').first()
                                else:
                                    log.debug('取最新的通用DPI配置')
                                    zdpi_data = dpiConfigVersion.objects.filter(
                                        dev_model_id='88888888').values().order_by('-update_time').first()
                            except:
                                log.debug('取通用的DPI配置')
                                zdpi_data = dpiConfigVersion.objects.filter(dev_model_id='88888888').values().first()
                        else:
                            log.debug('取型号【{}】特定的的DPI配置'.format(zy_model))
                            zdpi_data = dpiConfigVersion.objects.filter(id=zdpi_sig_version_id).values().first()
                        log.debug('DPI配置:{}'.format(zdpi_data))
                        zdpi_sig_version = zdpi_data['zdpi_sig_version']
                        zdpi_sig_file_path = zdpi_data['zdpi_sig_file']
                    except Exception as e:
                        log.error(e)
                        raise e
                    info = {
                        'superd_build_status': status,
                        'superd_version': superd_version,
                        'superdcf_version': superdcf_version,
                        'zdpi_sig_version': zdpi_sig_version,
                        'zdpi_sig_file_path': zdpi_sig_file_path,

                        'connector_version': connector_version,
                        'zy_model': zy_model,
                        'superd_path': superd_path,
                        'superdcf_path': superdcf_path,
                        'connector': connector_path,
                        'pack_type': i.pack_type,
                        'package_contains_path': i.package_contains_path,
                        'package_contains_path_type': i.package_contains_path_type,
                        'docking_solution': i.docking_solution
                    }
                    log.debug('配置策略详情：\n{}'.format(info))
                    log.debug('开始复制配置项中文件到工作路径：{}'.format(workplace_path+i.package_contains_path))
                    for j in [superd_path, superdcf_path, connector_path,zdpi_sig_file_path]:
                        cfres = chmod_file(j)
                        cpres = cp(j, workplace_path + i.package_contains_path)
                        if not cfres or not cpres:
                            log.error('授权结果：{}，复制结果：{}'.format(cfres,cpres))
                            info=0
                    return info
                else:
                    msg = '构建插件失败'
                    raise msg
        except Exception as e:
            log.error(e)
            return 0

    def compression(self, pack_type, dev_model, superd_version,package_contains_path,sw,source_save_path=''):
        '打包并且压缩，移动到包存放路径'
        tarname=''
        package_save_path_name = ''
        day_time_for_name = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        package_path = 'upload/package/{}'.format(get_path_day_time())
        save_package_path = base_path + package_path
        dir_name = package_contains_path
        is_ok=False
        try:
            if pack_type == 'gzip':
                if sw=='superd':
                    # 如果是shell版本加载器，则需要将版本号中的横线替换成下划线，因为shell脚本不识别横线。
                    if 'sapi' not in str(dir_name):
                        superd_version = superd_version.replace('-','.')
                    tarname = 'pgpack.{}.{}_{}.tar.gz'.format(dev_model, day_time_for_name, superd_version)
                else:
                    tarname = 'sapiloaderpack.{}.{}_{}.tar.gz'.format(dev_model, day_time_for_name, superd_version)
                cmd = 'tar zcvf {} {}'.format(tarname, dir_name)
            elif pack_type == 'lzma':
                if sw == 'superd':
                    tarname = 'pgpack.{}.{}_{}.tar'.format(dev_model, day_time_for_name, superd_version)
                else:
                    tarname = 'sapiloaderpack.{}.{}_{}.tar'.format(dev_model, day_time_for_name, superd_version)

                cmd = 'tar -cvf {0} {1} && lzma -e {0}'.format(tarname, dir_name)
                tarname = tarname + '.lzma'
            else:
                cmd = ''
                tarname = ''

            log.debug('开始打包:{},name:{}'.format(cmd, tarname))
            if sw=='superd':
                executionShell(cmd, workplace_path)
                source_path_name = workplace_path + tarname
            else:
                executionShell(cmd, source_save_path)
                source_path_name = source_save_path + tarname
            log.debug('开始移动包到保存路径：{}，{}'.format(source_path_name, save_package_path))
            if is_have_file(source_path_name):
                try:
                    mv(source_path_name, save_package_path)
                    if sw=='superd':
                        del_file(workplace_path)
                        log.debug('清理工作路径')
                    log.debug('包名称：{}'.format(tarname))
                    is_ok=True
                except Exception as e:
                    is_ok = False
                    log.error(e)
            else:
                is_ok=False
                log.error(source_path_name)

            package_save_path_name = save_package_path + tarname
            return is_ok,tarname,package_path,package_save_path_name
        except Exception as e:
            log.error(e)
            return is_ok,tarname,package_path,package_save_path_name

    def pack_superd_build(self,dev_model,reason,user,superd_version=''):
        """
        1.构建superd
        2.轮询10s查询superd是否构建完成
        :param dev_model:
        :param reason:
        :param user:
        :param superd_version:指定的superd——version

        :return:
        """
        status = 0
        sb = superd_build()
        if superd_version:
            tag = superd_version
        else:
            tag_list = sb.get_tag_list('superd')
            tag = tag_list[1]
        sb.toBuild(dev_model,tag,reason,user)
        for i in range(0,10):
            time.sleep(1)
            status = sb.get_superd(dev_model,tag,reason,user)
            if status==200:
                break
        return status

    def dopack(self, pack_conf_id, reason,user):
        """
        1.拿到配置详情
        2.拿到物料：superd、配置文件、连接器，并移动到指定路径下。
        3.根据指定打包方式，进行打包
        4.将结果存放在路径下。返回结果
        :param pack_conf_id:
        :param user:
        :return:
        """
        try:

            info = self.getConfigInfo(pack_conf_id,reason,user)
            res = -1
            if info:
                pack_type = info['pack_type']
                superd_version = info['superd_version']
                zy_model = info['zy_model']
                docking_solution = info['docking_solution']
                superd_path = info['superd_path']
                superdcf_path = info['superdcf_path']
                connector = info['connector']
                package_contains_path = info['package_contains_path']
                package_contains_path_type = info['package_contains_path_type']
                connector_version = info['connector_version']
                superdcf_version = info['superdcf_version']
                superd_build_status = info['superd_build_status']
                if int(superd_build_status)==200:
                    res = 0
                    is_ok,tarname,package_path,package_save_path_name = self.compression(pack_type, zy_model, superd_version,package_contains_path,'superd')
                    md5 = get_md5_big(package_save_path_name)
                    log.debug('包存放路径：{}'.format(package_save_path_name))
                    if is_ok:
                        pack_content = 'superd_path:{},superdcf_path:{},connector:{},package_contains_path:{}'.format(
                            superd_path, superdcf_path, connector, info['package_contains_path'])
                        download_url = plug_domain + package_path + tarname
                        obj, created=pack_list_contorl.objects.update_or_create(defaults={'pack_name':tarname,'md5':md5,'user':str(user), 'pack_content':pack_content,
                                                                 'package':package_save_path_name,
                                                                 'download_url':download_url}
                                                                 ,dev_model=zy_model, superd_version=superd_version,connector_version=connector_version,superdcf_version=superdcf_version,
                                                                 pack_type=pack_type,docking_solution=docking_solution,package_contains_path=package_contains_path,package_contains_path_type=package_contains_path_type)
                        log.debug('pack_db-obj:{},create:{}'.format(obj,created))
                        res = 1
                        if created != True:
                            res = 2
                else:
                    res = 3

            if info==0:
                res=3
                msg='插件构建失败'
            elif res == -1:
                msg = '取配置文件异常'
            elif res == 0:
                msg = '打包异常'
            elif res ==2:
                msg = '已经存在包信息，更新'
            elif res ==3:
                msg = '插件构建失败'
            else:
                msg = '打包完成'
            log.debug(msg)
            return {'code':res,'msg':msg}
        except Exception as e:
            log.error(e)


    def sapiloaderpack(self, dev_model, version,reason,user):
        # 1. 构建sapiloader
        if version=='88888':
            version = self.get_tag_list('sapiloader')[1]
        scb = sapiloaderC_build()
        is_complete = scb.Build(dev_model,version,reason,user)
        res = 400
        if is_complete==1:
            sapiloader_save_path = base_path+scb.package_path
            is_ok, tarname, package_path, package_save_path_name = self.compression('gzip',dev_model,version,'.','sapiloader',sapiloader_save_path)
            md5 = get_md5_big(package_save_path_name)
            download_url = plug_domain + package_path + tarname

            if is_ok:
                res=200
                obj, created =sapiloader_pack.objects.update_or_create(defaults={'md5':str(md5),'pack_save_path':package_save_path_name,'url':download_url,'user':str(user),'pack_name':tarname,'reason':reason},dev_model=dev_model,version=version)
                if created != True:
                    msg = '已经存在包信息，更新'
                else:
                    msg = '新增包记录成功'
            else:
                msg='加载器打包失败'
        else:
            msg = '构建sapiloader失败'
        log.debug(msg)
        return {'code': res, 'msg': msg}

class release_obj:
    """
    apmodel/loader-plug?t={$t}&url={$url}&sign={$sign}&modelname={$modelname}&filename={$filename}&name={$name}&run_cmd={$run_cmd}&unpack_cmd={$unpack_cmd}&save_plug_name={$save_plug_name}&
monitor_time={$monitor_time}&reconnect_time={$reconnect_time}&rom_version={$rom_version}&save_target_path={$save_target_path}
    """
    def __init__(self):
        self.apipath = 'apmodel/loader-plug'
        self.ts = str(time_stamp())

    def getPackInfo(self,id):
        data = pack_list_contorl.objects.filter(id=id).values().get()
        log.debug('packInfo:{}'.format(data))
        return data

    def getAllData(self):
        data = release_plug_log.objects.values().order_by('-update_time')[:10]
        return data
    def sign(self,md5):
        from appack.helper.sign import getSign
        md5_stamp = str(md5)+self.ts+'pythonapi'
        sign = hashlib.md5(md5_stamp.encode('utf-8')).hexdigest()
        return sign

    def record_release_log(self,**kwargs):
        try:
            obj = release_plug_log.objects.create(**kwargs)
            return obj
        except Exception as e:
            log.error(e)

    def getShellUrl(self,downurl,dev_model,file_name,superd_version,router,comment_in,md5):
        '针对shell版本加载器的PG包上线操作'
        sign = self.sign(md5)
        comment='build push \n'
        comment +=comment_in
        url = "{}apmodel/plugin?url={}&modelname={}&filename={}&version=ZJPG-{}&router={}&comment={}&sign={}&t={}".format(release_domain,downurl,dev_model,file_name,superd_version,router,comment,sign,self.ts)
        return url

    def ReleasePG(self,durl,modelname,md5,salscom,name,filename,**kwargs):
        para_dict = {
            'url': durl,
            'md5': md5,
            'modelname': modelname,
            'filename': filename,
            'name': name,
            'salscom': salscom,
            'run_cmd': kwargs['run_cmd'],
            'unpack_cmd': kwargs['unpack_cmd'],
            'save_plug_name': filename,
            'monitor_time': kwargs['monitor_time'],
            'reconnect_time': kwargs['reconnect_time'],
            'rom_version': kwargs['rom_version'],
            'save_target_path': kwargs['save_target_path'],
        }
        data = ap_api.release_pg(para_dict)
        return data
    def ReleaseShellPG(self,downurl,dev_model,file_name,superd_version,router,comment_in,md5):
        comment = 'build push \n'
        comment += comment_in
        para = {
            'url':downurl,
            'modelname':dev_model,
            'filename':file_name,
            'version':superd_version,
            'router':router,
            'comment':comment,
            'md5':md5,
        }
        data = ap_api.release_shell_pg(para)
        return data

    def dorelease(self,id,user,**kwargs):
        try:
            code = 0
            data={}
            err= ''
            packInfo = self.getPackInfo(id)
            durl = packInfo['download_url']
            md5 = packInfo['md5']
            modelname = packInfo['dev_model']
            filename = packInfo['pack_name']
            superd_version = packInfo['superd_version']
            superdcf_version = packInfo['superdcf_version']
            connector_version = packInfo['connector_version']
            package_contains_path_type = packInfo['package_contains_path_type']
            comment = kwargs['comment']
            if 'CMCC' in modelname:
                salscom = '中国移动'
                modelname=str(modelname).replace('CMCC-','')
            else:
                salscom=''
            if 'c_sapiloader' == package_contains_path_type:
                name = '{}[id]_{}_{}[superd]_{}[connector]_{}[conf]_{}'.format(id,modelname,superd_version,connector_version,superdcf_version,getNowTime())
                data = self.ReleasePG(durl,modelname,md5,salscom,name,filename,**kwargs)
                cmd_content = 'run_cmd:{},unpack_cmd:{},save_plug_name={},monitor_time={},reconnect_time={},rom_version={},save_target_path={}'.format(
                    kwargs['run_cmd'], kwargs['unpack_cmd'], filename, kwargs['monitor_time'], kwargs['reconnect_time'],
                    kwargs['rom_version'], kwargs['save_target_path'])

            elif 'shell_sapiloader' == package_contains_path_type:
                url = self.getShellUrl(durl,modelname,filename,superd_version,25,comment,md5)
                name=modelname
                cmd_content = url
                data = self.ReleaseShellPG(durl,modelname,filename,superd_version,25,comment,md5)
            else:
                cmd_content=''
                name=modelname
                code = 500
                err = '包内路径类型错误'
                data['err']=err

            if code!=500:
                code=400
                err = data['err']
                if data['succ']:
                    code=200
                    try:
                        self.record_release_log(dev_model=modelname,user=user,plug_title_name=name,plug_name=filename,plug_md5=md5,version=superd_version,cmd_content=cmd_content,
                                            comment=comment,rtype='pg')
                    except:
                        pass
            resdata = {'code':code,'err':err}
            return resdata
        except Exception as e:
            log.error(e)

    def release_sapiloader(self,id,area):
        log.debug('加载器上线开始')
        data = sapiloader_pack.objects.filter(id=id).values().get()
        dev_model = data['dev_model']
        user = data['user']
        pack_name = data['pack_name']
        md5 = data['md5']
        version = data['version']
        comment = data['reason']
        res = self.record_release_log(dev_model=dev_model,user=user,plug_title_name='',plug_name=pack_name,plug_md5=md5,version=version,cmd_content='',
                                        comment=comment,rtype='sapiloader')
        res = sapi.addNewSVersionInfo(area=area,dev_model=dev_model,status='1.准备中',docking_solution='2.5',vsapiloader=version,sapiloader_type='c版本',start_time=getNowTime(1))

        log.debug('加载器上线结果：{}'.format(res))
        return res
