from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from strategy.base.tools import JsonError, JsonResponse, authentication
from strategy.base.op_val import *
from strategy.control.ap_api import ap_api
from strategy.control.support_api import sp_api
import logging
log = logging.getLogger(__name__)


@login_required(login_url='/admin/login/')
def get_oem(request):
    auth = authentication(request)
    if auth == 200:
        data = get_oem_data()
        return render(request, 'strategy/oem.html', {'data': data})
    return auth


@login_required(login_url='/admin/login/')
def get_dev_model(request):
    auth = authentication(request)
    if auth == 200:
        a = get_model_type()
        b =get_all_version_data()['dev_model']
        return render(request, 'strategy/dev_model.html', {'get': b, 'add': a})
    return auth



def set_oem(request):
    """
    新增 厂商编码信息
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth==200:
        try:
            oem_name = request.GET.get('oem_name')
            oem_code = request.GET.get('oem_code')
            comment = str(request.GET.get('comment')).strip().replace('\n', ';').replace("\t", "").replace(" ", "")
            user = request.user
            insert_into_oem(comment=comment,
                            user=str(user),
                            oem_code=oem_code,
                            oem_name=oem_name)
            rdata = sp_api.addoem(oem_name=oem_name,oem_code=oem_code,comment=comment,user=str(user))
            rapdata = ap_api.add_oem(name=oem_name, code=oem_code)

            log.debug(rdata)
            log.debug(rapdata)
            return JsonResponse('add ok')
        except Exception as e:
            log.error(e)
            return JsonError(str(e))
    return auth

def set_dev_model(request):
    """
    新增 设备信息
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        dev_model_type = request.GET.get('dev_model_type')
        zy_model = request.GET.get('zy_model')
        oem_model = request.GET.get('oem_model')
        oem_id = request.GET.get('oem_id')
        comment = str(request.GET.get('comment')).strip().replace('\n', ';').replace("\t", "").replace(" ", "")
        user = str(request.user)
        data = inset_into_dev_model(oem_id, comment, user, dev_model_type, zy_model, oem_id, oem_model)

        if type(data) == str:
            return JsonError(data)
        if not data[1]:
            return JsonError('该型号已经存在')
        return JsonResponse('insert ok')

    return auth


@csrf_exempt
def set_super_config(request):
    """
    新增 配置文件信息
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth==200:
        try:
            if request.method == "POST":
                file_obj = request.FILES.get('file')
                superdcf_version = request.POST.get('version')
                dev_model = request.POST.get('dev_model')
                cf_type = request.POST.get('cf_type')
                comment = str(request.POST.get('comment')).strip().replace('\n',';').replace("\t", "").replace(" ","")
                user = str(request.user)
                # 写入数据库
                data = inset_into_super_config(file_obj, superdcf_version, dev_model, cf_type, comment, user)
                if type(data) == str:
                    return JsonError(data)
                if not data[1]:
                    return JsonError('数据已存在')
                return JsonResponse('upload ok!')
        except Exception as e:
            return JsonError(str(e))
    return auth
