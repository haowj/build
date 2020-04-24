import time
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from appack.helper.misc import mkdir, get_md5_big,executionShell
from appack.models import *
from api.helper.email import *
from appack.controller.version_control import superd_build,package,sapiloaderC_build,release_obj
import platform
from api.helper.misc import *
from django.http import HttpResponseRedirect
from appack.helper.git import git_process
from appack.conf.path import  sapiloader_c_project_path,superd_project_path,package_type,package_contains_path_dict,c_sapiloader,shell_sapiloader,getProjeck_path
from appack.controller.version_control import package_conf
from api.controller.work import packageConfig
from api.controller.work import connector
log = logging.getLogger(__name__)

from api.controller.dataToJson import *
from api.helper.misc import *
from appack.controller.support_api import supportApi
from appack.controller.ap_api import apApi
__author__ = 'xcma'
sapi = supportApi()
apapi = apApi()
from build.settings import SIGN_KEY

class authentication(APIView):

    def get_str_md5(self,string):
        md5 = hashlib.md5(string.encode('utf-8')).hexdigest()
        # log.debug('字符串:{}，md5:{}'.format(string, md5))
        return md5

    def sign(self,timestamp):
        string = '{}{}'.format(SIGN_KEY,timestamp)
        sign = self.get_str_md5(string)
        return sign


    def auth(self,request):
        log.debug('api_reqest:{} ,user:{}'.format(getFuncCalled(),request.user))
        if request.user.is_authenticated:

            if request.method != 'POST':
                timestamp = request.GET.get('ts')
                sign = request.GET.get('sign')
            else:
                timestamp = request.POST.get('ts')
                sign = request.POST.get('sign')

            s_sign = self.sign(timestamp)
            # log.debug('鉴权开始：s_sign:{},c_sign:{}'.format(s_sign, sign))
            auth = 200
            if sign !=s_sign:
                log.error('鉴权失败:s_sign:{},c_sign:{}'.format(s_sign, sign))
                return JsonError('auth error')
        else:
            auth=400
            return JsonError('auth error')
        return auth

at = authentication()
class version_contorl_view(APIView):
    save_path_name = ''
    def getPath(self, file_obj):
        day_time = time.strftime('%Y/%m/%d/%H/%M/%S', time.localtime(time.time()))
        self.save_path = './upload/' + day_time
        if 'Linux' in platform.system():
            self.save_path = '/home/build/upload/' + day_time

        self.save_path_name = self.save_path + '/' + file_obj.name
        mkdir(self.save_path, False)
        # 创建文件
        with open(self.save_path_name, 'wb') as new_file:
            for chunk in file_obj.chunks():
                new_file.write(chunk)
        # 创建文件后，计算文件md5
        self.md5 = get_md5_big(self.save_path_name)
        log.debug('file_path:{},md5:{}'.format(self.save_path_name, self.md5))

    @csrf_exempt
    def sapiloaderAdd(self, request):
        auth = at.auth(request)
        if auth==200:
            try:
                if request.method == "POST":
                    file_obj = request.FILES.get('file')
                    if file_obj:  # 处理附件上传到方法
                        self.getPath(file_obj)

                    sapiloader_version = request.POST.get('sapiloader_version')
                    comment = str(request.POST.get('comment')).strip().replace('\n',';').replace("\t", "").replace(" ","")

                    # 写入数据库
                    upload = sapiloaderVersion()
                    upload.sapiloader_version = sapiloader_version
                    upload.sapiloader_file = self.save_path_name
                    upload.md5 = self.md5
                    upload.comment = comment
                    upload.user = request.user
                    upload.save()
                    return JsonResponse('upload ok!')
            except Exception as e:
                return JsonError(str(e))
        return auth

    @csrf_exempt
    def superdcfAdd(self, request):
        auth = at.auth(request)
        if auth==200:
            try:
                if request.method == "POST":
                    file_obj = request.FILES.get('file')
                    if file_obj:  # 处理附件上传到方法
                        self.getPath(file_obj)
                    superdcf_version = request.POST.get('version')
                    dev_model = request.POST.get('dev_model')
                    cf_type = request.POST.get('cf_type')
                    comment = str(request.POST.get('comment')).strip().replace('\n',';').replace("\t", "").replace(" ","")
                    # 写入数据库
                    upload = superdcfVersion()
                    upload.superdcf_version = superdcf_version
                    upload.superdcf_file = self.save_path_name
                    upload.comment = comment
                    upload.dev_model = dev_model
                    upload.md5 = self.md5
                    upload.type = cf_type

                    upload.user = request.user
                    upload.save()
                    return JsonResponse('upload ok!')
            except Exception as e:
                return JsonError(str(e))
        return auth
    @csrf_exempt
    def zdpi_sig_add(self, request):
        auth = at.auth(request)
        if auth==200:
            try:
                if request.method == "POST":
                    file_obj = request.FILES.get('file')
                    if file_obj:  # 处理附件上传到方法
                        self.getPath(file_obj)
                    zdpi_sig_version = request.POST.get('version')
                    dev_model = request.POST.get('dev_model')
                    dev_model_id = request.POST.get('dev_model_id')
                    comment = str(request.POST.get('comment')).strip().replace('\n',';').replace("\t", "").replace(" ","")
                    # 写入数据库
                    dpi_data = dpiConfigVersion.objects.filter(dev_model_id=dev_model_id,md5=self.md5).count()
                    if dpi_data==0:
                        upload = dpiConfigVersion()
                        upload.zdpi_sig_version = zdpi_sig_version
                        upload.zdpi_sig_file = self.save_path_name
                        upload.dev_model_id = dev_model_id
                        upload.comment = comment
                        upload.dev_model = dev_model
                        upload.md5 = self.md5
                        upload.user = str(request.user)
                        upload.save()
                        return JsonResponse('upload ok!')
                    return JsonResponse('已经存在，不再新增！')
            except Exception as e:
                return JsonError(str(e))
        return auth

    @csrf_exempt
    def superctlAdd(self, request):
        auth = at.auth(request)
        if auth==200:
            try:
                if request.method == "POST":
                    file_obj = request.FILES.get('file')
                    if file_obj:  # 处理附件上传到方法
                        self.getPath(file_obj)
                    superctl_version = request.POST.get('version')
                    comment = str(request.POST.get('comment')).strip().replace('\n',';').replace("\t", "").replace(" ","")

                    # 写入数据库
                    upload = superctlVersion()
                    upload.superctl_version = superctl_version
                    upload.superctl_file = self.save_path_name
                    upload.comment = comment
                    upload.md5 = self.md5

                    upload.user = request.user
                    upload.save()
                    return JsonResponse('upload ok!')
            except Exception as e:
                return JsonError(str(e))
        return auth
    @csrf_exempt
    def supertackAdd(self, request):
        auth = at.auth(request)
        if auth==200:
            try:
                if request.method == "POST":
                    file_obj = request.FILES.get('file')
                    if file_obj:  # 处理附件上传到方法
                        self.getPath(file_obj)
                    supertack_version = request.POST.get('version')
                    comment = str(request.POST.get('comment')).strip().replace('\n',';').replace("\t", "").replace(" ","")
                    # 写入数据库
                    upload = supertackVersion()
                    upload.supertack_version = supertack_version
                    upload.supertack_file = self.save_path_name
                    upload.comment = comment
                    upload.md5 = self.md5

                    upload.user = request.user
                    upload.save()
                    return JsonResponse('upload ok!')
            except Exception as e:
                return JsonError(str(e))
        return auth
    def superd_build(self, request):
        auth = at.auth(request)
        if auth==200:
            dev_model = request.GET.get('dev_model')
            tag = request.GET.get('tag')
            reason = str(request.GET.get('reason')).strip().replace('\n',';').replace("\t", "").replace(" ","")
            try:
                sbl = superd_build()
                data = sbl.toBuild(dev_model, tag, reason,str(request.user))
                return JsonResponse(data)
            except Exception as e:
                return JsonError(str(e))
        return auth

    def superd_build_test(self, request):
        auth = at.auth(request)
        if auth==200:
            dev_model = request.GET.get('dev_model')
            branch = request.GET.get('branch')
            reason = str(request.GET.get('reason')).strip().replace('\n',';').replace("\t", "").replace(" ","")
            try:
                sbl = superd_build()
                data = sbl.toBuild_test(dev_model,branch,reason,str(request.user))
                return JsonResponse(data)
            except Exception as e:
                return JsonError(str(e))
        return auth

    def superd_build_result(self, request):
        auth = at.auth(request)
        if auth==200:
            try:
                dev_model = request.GET.get('dev_model')
                tag = request.GET.get('tag')
                reason = str(request.GET.get('reason')).strip().replace('\n', ';').replace("\t", "").replace(" ", "")
                user = str(request.user)
                is_test = None
                if tag =='RC':
                    is_test = True
                if dev_model:
                    sbl = superd_build()
                    build_status = sbl.get_superd(dev_model,tag,reason,user,is_test)
                    return JsonResponse(build_status)
                return JsonError('参数异常')
            except Exception as e:
                return JsonError(str(e))
        return auth

    def sapiloader_c_build(self, request):
        auth = at.auth(request)
        if auth==200:
            dev_model = request.GET.get('dev_model')
            tag = request.GET.get('tag')
            reason = str(request.GET.get('reason')).strip().replace('\n',';').replace("\t", "").replace(" ","")

            try:
                sbl = sapiloaderC_build()
                data = sbl.toBuild(dev_model, tag, reason,request.user)
                return JsonResponse(data)
            except Exception as e:
                return JsonError(str(e))
        return auth

    def sapiloader_c_build_result(self, request):
        auth = at.auth(request)
        if auth==200:
            try:
                dev_model = request.GET.get('dev_model')
                tag = request.GET.get('tag')
                reason = str(request.GET.get('reason')).strip().replace('\n', ';').replace("\t", "").replace(" ", "")

                user = str(request.user)
                if dev_model:
                    sbl = sapiloaderC_build()
                    build_status = sbl.get_sapiloader(dev_model,tag,reason,user)
                    return JsonResponse(build_status)
                return JsonError('参数异常')
            except Exception as e:
                return JsonError(str(e))
        return auth

    def packageconfigAdd(self, request):
        auth = at.auth(request)
        if auth==200:
            dev_model_id = request.GET.get('dev_model_id')
            sapiloader_id = request.GET.get('sapiloader_id')
            sapiloaderC_id = request.GET.get('sapiloaderC_id')
            superdcf_id = request.GET.get('superdcf_id')
            zdpi_sig_id = request.GET.get('zdpi_sig_id')
            connector = request.GET.get('connector')
            superd_id = request.GET.get('superd_id')
            pack_type = request.GET.get('pack_type')
            package_contains_path_type = str(request.GET.get('package_contains_path_type'))
            package_contains_path_in = package_contains_path_dict[package_contains_path_type]
            rom_version = request.GET.get('rom_version')
            docking_solution = request.GET.get('docking_solution')
            comment = str(request.GET.get('comment')).strip().replace('\n', ';').replace("\t", "").replace(" ", "")
            user = str(request.user)
            connector_list = str(connector).split('_')
            if 'supertack' in connector_list[1]:
                supertack_id =connector_list[0]
            else:
                supertack_id = ''
            if 'superctl' in connector_list[1]:
                superctl_id=connector_list[0]
            else:
                superctl_id=''

            try:
                obj, created = version_contorl.objects.update_or_create(defaults={'sapiloaderC_version_id':sapiloaderC_id,'sapiloader_version_id':sapiloader_id,
                                                                'comment':comment,'user':user},
                                                     dev_model_id=dev_model_id,
                                                     pack_type=pack_type,
                                                     superdcf_version_id=superdcf_id,
                                                     superctl_version_id=superctl_id,
                                                     supertack_version_id=supertack_id,
                                                     superd_version_id=superd_id,zdpi_sig_version_id=zdpi_sig_id,
                                                     rom_version=rom_version,
                                                     docking_solution=docking_solution,
                                                     package_contains_path=package_contains_path_in,
                                                     package_contains_path_type=package_contains_path_type,
                                                     )
                if created:
                    return JsonResponse('insert ok')
                else:
                    return JsonError('已经存在，将执行更新操作',409)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def oem_add(self,request):
        auth = at.auth(request)
        if auth==200:
            try:
                oem_name = request.GET.get('oem_name')
                oem_code = request.GET.get('oem_code')
                comment = str(request.GET.get('comment')).strip().replace('\n', ';').replace("\t", "").replace(" ", "")
                user = request.user
                oem_db.objects.update_or_create(defaults={'comment':comment,'user':str(user)},oem_code=oem_code,oem_name=oem_name)
                rdata = sapi.addoem(oem_name=oem_name,oem_code=oem_code,comment=comment,user=str(user))
                rapdata = apapi.add_oem(name=oem_name,code=oem_code)
                log.debug(rdata)
                log.debug(rapdata)
                return JsonResponse('add ok')
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def dev_model_add(self, request):
        auth = at.auth(request)
        if auth==200:
            dev_model_type = request.GET.get('dev_model_type')
            zy_model = request.GET.get('zy_model')
            oem_model = request.GET.get('oem_model')
            oem_id = request.GET.get('oem_id')
            comment = str(request.GET.get('comment')).strip().replace('\n', ';').replace("\t", "").replace(" ", "")
            user = str(request.user)
            try:
                oem_data = oem_db.objects.filter(id=oem_id).values('oem_name','oem_code').get()
                oem_name = oem_data['oem_name']
                oem_code = oem_data['oem_code']
                res=''
                try:
                    res = dev_model_db.objects.update_or_create(defaults={'comment':comment,'user':user},type=dev_model_type,
                                                      zy_model=zy_model,
                                                      oem_id=oem_id,
                                                    oem_name=oem_name,
                                                    oem_code=oem_code,
                                                oem_model=oem_model,
                                                )
                except Exception as e:
                    log.error(e)
                rdata = sapi.adddev_model(type=dev_model_type,dev_model=zy_model,oem_model=oem_model,old_model='',oem_name=oem_name,comment=comment,user=str(user))
                rapdata = apapi.add_dev_model(cate_name=dev_model_type,model_name=zy_model,salscom=oem_name,oem_name=oem_name)
                log.debug(rdata)
                log.debug(rapdata)
                if '1062' in str(res):
                    return JsonError('该型号已经存在')
                return JsonResponse('insert ok')
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def package(self,request):
        auth = at.auth(request)
        if auth==200:
            try:
                pack_conf_id = request.GET.get('id')
                ver = request.GET.get('ver')
                pack = package()
                reason = 'auto build'
                if not ver:
                    data = pack.dopack(pack_conf_id,reason,request.user)
                else:
                    data = pack.sapiloaderpack(pack_conf_id, ver, reason, request.user)
                return JsonResponse(data)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def getConnector(self,request):
        "获取连接器"
        auth = at.auth(request)
        if auth==200:
            try:
                cinfo = {}
                list = []
                package_contains_path_type = request.GET.get('package_contains_path_type')
                dev_model_id = request.GET.get('dev_model_id')
                if c_sapiloader in package_contains_path_type:
                    data = supertackVersion.objects.values().order_by('-update_time','-id')
                    for i in data:
                        info = {}
                        id = i['id']
                        version = i['supertack_version']
                        comment = i['comment']
                        update_time = i['update_time']
                        info['id']=id
                        info['version'] = version
                        info['comment'] = comment
                        info['update_time'] = update_time
                        info['type'] = 'supertack'
                        list.append(info)
                    type=c_sapiloader
                elif shell_sapiloader == package_contains_path_type:
                    data = superctlVersion.objects.values().order_by('-update_time','-id')
                    for i in data:
                        info = {}
                        id = i['id']
                        version = i['superctl_version']
                        comment = i['comment']
                        update_time = i['update_time']
                        info['id']=id
                        info['version'] = version
                        info['comment'] = comment
                        info['update_time'] = update_time
                        info['type'] = 'superctl'
                        list.append(info)
                    type=shell_sapiloader
                else:
                    return JsonError('参数错误',400)

                cinfo['connector']=list

                try:
                    dev_model = dev_model_db.objects.filter(id=dev_model_id).values('zy_model').get()['zy_model']
                    data = superdcfVersion.objects.filter(type=type,dev_model=dev_model).values()
                except:
                    data={}
                cinfo['superdcf']=data

                try:
                    zdpiInfo = dpiConfigVersion.objects.filter(dev_model_id=dev_model_id).values()
                except:
                    zdpiInfo=[]
                try:
                    # 型号id为：88888888 标识全部型号全部适用，属于通用版本。
                    gzdpiInfo = dpiConfigVersion.objects.filter(dev_model_id='88888888').values()
                except:
                    gzdpiInfo=[]

                cinfo['zdpiInfo']=zdpiInfo
                cinfo['gzdpiInfo']=gzdpiInfo
                cinfo['pack_type']=package_type[type]
                return JsonResponse(cinfo)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def release(self,request):
        auth = at.auth(request)
        if auth==200:
            try:
                t = request.GET.get('t')
                rel = release_obj()

                if t=='pg':
                    pack_id = request.GET.get('id')
                    user = str(request.user)
                    save_target_path = request.GET.get('save_target_path')
                    if save_target_path =='slave':
                        save_target_path='/sapi/slave'
                    else:
                        save_target_path='/sapi/master'
                    run_cmd = request.GET.get('run_cmd')
                    unpack_cmd = request.GET.get('unpack_cmd')
                    monitor_time = request.GET.get('monitor_time')
                    reconnect_time = request.GET.get('reconnect_time')
                    rom_version = request.GET.get('rom_version')
                    comment = request.GET.get('comment')
                    data = rel.dorelease(pack_id,user,comment=comment,save_target_path=save_target_path,run_cmd=run_cmd,
                                         unpack_cmd=unpack_cmd,monitor_time=monitor_time,reconnect_time=reconnect_time,rom_version=rom_version,
                                         )
                else:
                    s_pack_id = request.GET.get('id')
                    area = request.GET.get('area')
                    data = rel.release_sapiloader(s_pack_id,area)
                return JsonResponse(data)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth


    def tag_add(self,request):
        auth = at.auth(request)
        if auth==200:
            try:
                tag = request.GET.get('tag')
                sw = request.GET.get('sw')
                comment = str(request.GET.get('comment')).strip().replace('\n', ';').replace("\t", "").replace(" ", "")
                user = request.user
                msg = '操作人:build[{}],说明:{}'.format(user,comment)
                if sw and tag and comment:
                    path,branch = getProjeck_path(sw)
                    log.debug('sw:{},pj_path:{},msg:{},tag:{}'.format(sw,path,msg,tag))
                    git = git_process(path)
                    git.createTag(tag,msg,sw,path,branch,str(user))
                return JsonResponse(1)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth
    def tag_info(self,request):
        auth = at.auth(request)
        if auth==200:
            try:
                tag_sw = str(request.GET.get('tag'))
                tag = tag_sw.split('_')[0]
                sw = tag_sw.split('_')[1]
                if tag:

                    path,branch = getProjeck_path(sw)
                    log.debug('sw:{},pj_path:{},tag:{}'.format(sw,path,tag))
                    if tag=='RC':
                        cmd = 'git log -n1'
                    else:
                        cmd = "git show {}".format(tag)
                    data = executionShell(cmd,path)
                    adata = []
                    for i in data:
                        if len(i)>1:
                            i = str(i).replace('<','').replace('>','')
                            adata.append(i)
                    return JsonResponse(adata)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def build_info(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                id = str(request.GET.get('id'))
                if id:
                    data = build_log.objects.filter(id=id).values('build_result').get()
                    try:
                        build_result = eval(data['build_result'])
                    except:
                        build_result = data['build_result']
                    return JsonResponse(build_result)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def getSuperdInfo(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                dev_model_id = str(request.GET.get('id'))
                if dev_model_id:
                    dev_model = dev_model_db.objects.filter(id=dev_model_id).values('zy_model').get()['zy_model']
                    superdInfo = superdVersion.objects.filter(dev_model=dev_model).values().order_by('-id')[:10]
                    superdcf = superdcfVersion.objects.filter(dev_model=dev_model).values().order_by('-id')[:10]
                    data ={'superdInfo':superdInfo,'superdcfInfo':superdcf}
                    return JsonResponse(data)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def getPackageConfigList(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                dev_model_id = request.GET.get('dev_model_id')
                id = request.GET.get('id')
                pc = package_conf()
                PackageConfigList = pc.getAllData(dev_model_id,id)
                return JsonResponse(PackageConfigList)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def getPackageConfigInfo(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                id = request.GET.get('id')
                if id:
                    pc = packageConfig()
                    data = pc.getPackageConfigInfo(id)
                    return JsonResponse(data)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def getadvertising(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                type = request.GET.get('type')
                location = request.GET.get('location')
                if type:
                    data = getadvertising(type,location)
                    return JsonResponse(data)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def getReleaseInfo(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                id = request.GET.get('id')
                sid = str(id).split('_')[0]
                t = str(id).split('_')[1]
                if sid and t:
                    data = release_plug_log.objects.filter(id=sid,rtype=t).values()
                    return JsonResponse(data)
                else:
                    msg='参数异常'
                    raise msg
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def advertisingAdd(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                type = request.GET.get('type')
                user = str(request.user)
                location = request.GET.get('location')
                title = request.GET.get('title')
                content = request.GET.get('content')
                if type:
                    obj, created = advertising.objects.update_or_create({'type':type,'title':title,'location':location,'user':user},content=content)
                    return JsonResponse(created)
                return JsonError('param error')
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def getAdvertisingContent(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                id = request.GET.get('id')
                if type:
                    data = advertising.objects.filter(id=id).values().get()
                    return JsonResponse(data)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def getPackageInfo(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                t = request.GET.get('t')
                dev_model = request.GET.get('dev_model')

                if t=='pg':
                    package_contains_path_type = request.GET.get('package_contains_path_type')
                    package_contains_path = package_contains_path_dict[package_contains_path_type]
                    data = pack_list_contorl.objects.filter(dev_model=dev_model,package_contains_path_type=package_contains_path_type,package_contains_path=package_contains_path).values().order_by('-id')[:10]
                elif t=='sapiloader':
                    data = sapiloader_pack.objects.filter(dev_model=dev_model).values().order_by('-id')[:100]
                else:
                    data = {}
                return JsonResponse(data)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def getPackageIDInfo(self,request):
            auth = at.auth(request)
            if auth == 200:
                try:
                    id = request.GET.get('id')
                    if id:
                        data = pack_list_contorl.objects.filter(id=int(id)).get().pack_type
                        return JsonResponse(data)
                except Exception as e:
                    log.error(e)
                    return JsonError(str(e))
            return auth

    def getPackageInfo_detail(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                id = request.GET.get('id')
                type = request.GET.get('type')
                if id:
                    if type=='pg':
                        data = pack_list_contorl.objects.filter(id=id).values()
                    elif type=='sapiloader':
                        data = sapiloader_pack.objects.filter(id=id).values()
                    else:
                        data =[0]
                    return JsonResponse(data)
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth


    def deltag(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                tag = request.GET.get('tag')
                project_type = request.GET.get('sw')
                project_path,branch = getProjeck_path(project_type)
                if project_path and tag:
                    git = git_process(project_path)
                    data = git.delTag(tag,project_type)
                    return JsonResponse(data)
                else:
                    return JsonError('param error')
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth

    def gitInit(self, request, project_path):
        auth = at.auth(request)
        if auth == 200:
            try:
                git = git_process(project_path)
                git.init_project()
            except Exception as e:
                log.error(e)
                return JsonError(e)
        return auth

    def connector_add(self,request):
        auth = at.auth(request)
        if auth == 200:
            try:
                tag = request.GET.get('tag')
                connector_trype = request.GET.get('connector_type')
                dev_model = request.GET.get('dev_model')
                comment = request.GET.get('comment')
                user = str(request.user)
                if tag and dev_model:
                    cc= connector()
                    data = cc.connector_add(tag,dev_model,connector_trype,comment,user)
                    if data:
                        return JsonResponse(data)
                    else:
                        return  JsonError(data)
                return JsonError('param error')
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth
    def authadd(self,request):
        from api.controller.work import register_auth
        auth = at.auth(request)
        if auth == 200:
            try:
                sn = request.GET.get('sn')
                dev_model = request.GET.get('dev_model')
                result = request.GET.get('result')
                user = str(request.user)
                log.debug(user)
                if dev_model and sn and result:
                    cc= register_auth()
                    data = cc.setAuth(sn,dev_model,result)
                    if data['code']==200:
                        return JsonResponse(data)
                    else:
                        return  JsonError(data['data'])
                return JsonError('param error')
            except Exception as e:
                log.error(e)
                return JsonError(str(e))
        return auth


    def restart(self,request):
        try:
            c_key = request.GET.get('token')
            cmd = request.GET.get('cmd')
            if '32d8358abcdc9be57a267a9b1bb45ad0' == c_key:
                if not cmd:
                    cmd='restart'
                cmd = 'sh restart.sh {}'.format(cmd)
                cwd = '/home/zjzy/build/'
                log.debug('cmd:{},cwd:{}'.format(cmd,cwd))
                executionShell(cmd,cwd)
                HttpResponseRedirect('/public')
                return JsonResponse(1)
            return JsonError('auth error')
        except Exception as e:
            return JsonError(str(e))


