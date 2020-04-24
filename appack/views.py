from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from appack.controller.version_control import *
log = logging.getLogger(__name__)
# Create your views here.
def authentication(request):
    authent = 400
    if request.user.is_authenticated:
        log.debug('current_user[{}] operation {} '.format(request.user,getFuncCalled()))
        current_user_set = request.user
        current_group_set = current_user_set
        if not request.user.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
        authent = 400

        if '第三方' not in str(current_group_set) or request.user.is_superuser:
            authent = 200
        log.debug('user:{},group:{},authentication:{}'.format(request.user,current_group_set,authent))
        return authent
    if authent !=200:
        log.debug('render')
        return render(request, 'appack/autherror.html', {
            'message': {'msg': '权限不足'}
        })

@login_required(login_url='/admin/login/')
def gps(request):
    log.debug('current_user[{}] operation gps '.format(request.user))
    sdata = request.GET['s_data']
    gps_dict = {'发布上线': 'release', '插件包': 'package', '策略配置': 'packageconfig', '加载器C': 'sapiloader_c',
                '正式版本': 'superd', '测试版本': 'superd_test', '设备厂商': 'oem', '设备型号': 'dev_model',
                '加载器': 'sapiloader', '配置文件': 'superdcf', '连接器': 'superctl', '连接器C': 'supertack', '后台管理': 'management'}
    if sdata:
        for k, v in gps_dict.items():
            if sdata in k:
                log.debug('sdata:{},path:{}'.format(sdata, v))
                return HttpResponseRedirect('/{}'.format(v))
    return HttpResponseRedirect('/')

@login_required(login_url='/admin/login/')
def logout(request):
    log.debug('current_user[{}] operation loginout '.format(request.user))
    return HttpResponseRedirect('/admin/logout')

@login_required(login_url='/admin/login/')
def oem_view(request):
    auth = authentication(request)
    if auth == 200:
        oo = oem_db_obj()
        data =oo.getAllData()
        return render(request, 'appack/oem.html', {'data': data})
    return auth

@login_required(login_url='/admin/login/')
def oem_add_view(request):
    auth = authentication(request)
    if auth == 200:
        oo = oem_db_obj()
        data =oo.getAllData()
        return render(request, 'appack/oem_add.html', {'data': data})
    return auth

@login_required(login_url='/admin/login/')
def dev_model_view(request):
    auth = authentication(request)
    if auth == 200:
        am = dev_model_obj()
        data =am.getAllData()
        return render(request, 'appack/dev_model.html', {'data': data})
    return auth

@login_required(login_url='/admin/login/')
def dev_model_add_view(request):
    auth = authentication(request)
    if auth == 200:
        am = dev_model_obj()
        data = am.addData()
        return render(request, 'appack/dev_model_add.html',{'data':data})
    return auth


@login_required(login_url='/admin/login/')
def sapiloader_view(request):
    auth = authentication(request)
    if auth == 200:
        sil = sapiloader()
        data = sil.getAllData()
        return render(request, 'appack/sapiloader.html', {'data': data})
    return auth

@login_required(login_url='/admin/login/')
def sapiloader_c_view(request):
    auth = authentication(request)
    if auth == 200:
        sil = sapiloaderC()
        data = sil.getAllData()
        bldata = sil.getBuildLog('sapiloader')
        data = {'sdata':data,'bldata':bldata}
        return render(request, 'appack/sapiloader_c.html', data)
    return auth


@login_required(login_url='/admin/login/')
def sapiloader_c_build_view(request):
    auth = authentication(request)
    if auth == 200:
        sil = sapiloaderC_build()
        tag_list = sil.get_tag_list('sapiloader')
        dev_model_list = sil.get_dev_model()
        data = {'tag': tag_list, 'dev_model': dev_model_list}
        return render(request, 'appack/sapiloader_c_build.html', data)
    return auth


@login_required(login_url='/admin/login/')
def sapiloader_add_view(request):
    auth = authentication(request)
    if auth == 200:
        return render(request, 'appack/sapiloaderAdd.html')
    return auth


@login_required(login_url='/admin/login/')
def superctl_view(request):
    auth = authentication(request)
    if auth == 200:
        scl = superctl()
        data = scl.getAllData()
        return render(request, 'appack/superctl.html', {'data': data})
    return auth

@login_required(login_url='/admin/login/')
def superctl_add_view(request):
    auth = authentication(request)
    if auth == 200:
        return render(request, 'appack/superctlAdd.html')
    return auth

@login_required(login_url='/admin/login/')
def superdcf_view(request):
    auth = authentication(request)
    if auth == 200:
        sdc = superdcf()
        data = sdc.getAllData()
        return render(request, 'appack/superdcf.html', {'data': data})
    return auth

@login_required(login_url='/admin/login/')
def zdpi_sig_view(request):
    auth = authentication(request)
    if auth == 200:
        sdc = zdpi_config()
        data = sdc.getDevModel()
        list_data = sdc.getAllData()
        return render(request, 'appack/dpiconfig.html', {'data': data,'list_data':list_data})
    return auth

@login_required(login_url='/admin/login/')
def superdcf_add_view(request):
    auth = authentication(request)
    if auth == 200:
        dd = superd_build()
        model = dd.get_dev_model()
        data = {'data':model,'type':superdcf_type}
        return render(request, 'appack/superdcfAdd.html',data)
    return auth

@login_required(login_url='/admin/login/')
def packageconfig_view(request):
    auth = authentication(request)
    if auth == 200:
        pc = package_conf()
        data = pc.getAllData()
        return render(request, 'appack/packageconfig.html', {'data': data})
    return auth

@login_required(login_url='/admin/login/')
def packageconfig_add_view(request):
    auth = authentication(request)
    if auth == 200:
        pc = package_conf()
        data = pc.getallVersionData()
        return render(request, 'appack/packageconfigAdd.html', {'data': data})
    return auth

@login_required(login_url='/admin/login/')
def superd_view(request):
    auth = authentication(request)
    if auth == 200:
        sc = superd()
        data = sc.getAllData(build_type='superd')
        bldata = sc.getBuildLog('superd')
        data = {'sdata':data,'bldata':bldata}
        return render(request, 'appack/superd.html',data)
    return auth

@login_required(login_url='/admin/login/')
def superd_build_view(request):
    auth = authentication(request)
    if auth == 200:
        sb = superd_build()
        tag_list = sb.get_tag_list('superd')
        dev_model_list = sb.get_dev_model()
        data = {'tag':tag_list,'dev_model':dev_model_list}
        return render(request, 'appack/superd_build.html',data)
    return auth

@login_required(login_url='/admin/login/')
def superd_test_view(request):
    auth = authentication(request)
    if auth == 200:
        sc = superd()
        build_type = 'test'
        data = sc.getAllData(build_type=build_type)
        bldata = sc.getBuildLog('superd_test')
        data = {'sdata':data,'bldata':bldata}
        return render(request, 'appack/superd_test.html',data)
    return auth

@login_required(login_url='/admin/login/')
def superd_build_test_view(request):
    auth = authentication(request)
    if auth == 200:
        sb = superd_build()

        dev_model_list = sb.get_dev_model()
        data = {'tag':superd_build_test_branch_list,'dev_model':dev_model_list}
        return render(request, 'appack/superd_build_test.html',data)
    return auth

@login_required(login_url='/admin/login/')
def supertack_add_view(request):
    auth = authentication(request)
    if auth == 200:
        sc = supertack()
        data = sc.getAllData()
        return render(request, 'appack/supertackAdd.html', {'data': data})
    return auth

@login_required(login_url='/admin/login/')
def package_view(request):
    auth = authentication(request)
    if auth == 200:
        sc = package()
        sb = superd_build()
        dev_model_list = sb.get_dev_model_all()
        data = sc.getAllData()
        sldata = sc.getSapiloaderData()
        proxydata = sc.getproxyData()

        rdata = {'pack_list':data,'dev_model':dev_model_list,'tag_list':sb.get_tag_list('sapiloader'),'sapiloader_pack_list':sldata,'proxydata':proxydata}
        return render(request, 'appack/package.html', {'data': rdata})
    return auth

@login_required(login_url='/admin/login/')
def release_view(request):
    auth = authentication(request)
    if auth == 200:
        ro = release_obj()
        sb = superd_build()
        dev_model_list = sb.get_dev_model()
        rdata = ro.getAllData()
        data = {'release_log': rdata,'package_contains_path':package_contains_path_dict,'save_path':save_path,'dev_model_list':dev_model_list}
        return render(request, 'appack/release.html', data)
    return auth

@login_required(login_url='/admin/login/')
def management(request):
    if request.user.is_superuser :
        return HttpResponseRedirect('/admin/')
    return render(request, 'appack/autherror.html', {
        'message': {'msg': '权限不足'}
    })

@login_required(login_url='/admin/login/')
def tag_add_view(request):
    auth = authentication(request)
    if auth == 200:
        sb = superd_build()
        superd_tag_list = sb.get_tag_list('superd')
        sapiloader_tag_list = sb.get_tag_list('sapiloader')
        vdata = {'superd':'插件版本','sapiloader':'加载器版本','connector':'连接器版本',}
        data = {'vdata':vdata,'superd_tag_list':superd_tag_list,'sapiloader_tag_list':sapiloader_tag_list}
        return render(request, 'appack/tag_add.html', data)
    return auth

@login_required(login_url='/admin/login/')
def advertising_view(request):
    auth = authentication(request)
    if auth == 200:
        adv_data = advertising.objects.values().order_by('-id')
        data = {'adv_data':adv_data,'type':advertising_type,'location':advertising_location}
        return render(request, 'appack/advertising.html', data)
    return auth

@login_required(login_url='/admin/login/')
def connector_view(request):
    auth = authentication(request)
    if auth == 200:
        sc = supertack()
        history_data = sc.getAllData()
        dev_model_list = sc.get_dev_model()
        dev_model_list.insert(0, 'fitall')
        tag_list = sc.get_tag_list('connector')
        data = {'dev_model': dev_model_list, 'tag': tag_list, 'connector_type': connector_type, 'history': history_data}
        return render(request, 'appack/connector.html', data)
    return auth

@login_required(login_url='/admin/login/')
def auth_view(request):
    auth = authentication(request)
    if auth == 200:
        sc = supertack()
        dev_model_list = sc.get_dev_model()
        data = {'dev_model': dev_model_list}
        return render(request, 'appack/registerauthadd.html', data)
    return auth


