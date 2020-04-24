import copy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from checkout.base.tools import get_func_called, json_error, json_response
from dpi.control.iface import bm
from dpi.control.dpi_conf_view import miv

import logging
log = logging.getLogger(__name__)


def authentication(request):
    authent = 400
    if request.user.is_authenticated:
        log.debug('current_user[{}] operation {} '.format(request.user, get_func_called()))
        current_user_set = request.user
        current_group_set = current_user_set
        if not request.user.is_superuser:
            current_group_set = Group.objects.get(user=current_user_set)
        authent = 400

        if '第三方' not in str(current_group_set) or request.user.is_superuser:
            authent = 200
        log.debug('user:{},group:{},authentication:{}'.format(request.user,current_group_set, authent))
        return authent
    if authent != 200:
        log.debug('render')
        return render(request, 'appack/autherror.html', {
            'message': {'msg': '权限不足'}
        })

def api_auth(request):
    if request.user.is_authenticated:
        return 200
    else:
        return json_error('权限不足',400)

def api_response(data):
    # log.debug(data)
    if data['code'] == 200:
        return json_response(data['data'])
    else:
        return json_error(data['msg'])

@login_required(login_url='/admin/login/')
def show_data(request):
    auth = authentication(request)
    if auth == 200:
        data = dict()
        data['identity'] = bm.api_get_identity()['data']
        data['business'] = bm.api_get_business()['data']
        return render(request, 'dpi/showData.html', data)
    return auth


@login_required(login_url='/admin/login/')
def show_p_data(request):
    auth = authentication(request)
    if auth == 200:
        return render(request, 'dpi/showPData.html')
    return auth

@login_required(login_url='/admin/login/')
def dpi_conf(request):
    auth = authentication(request)
    if auth == 200:
        data = miv.getAll()
        return render(request, 'dpi/dpi_conf.html',{'data':data})
    return auth


def del_data(request):
    auth = authentication(request)
    if auth == 200:
        ids = request.GET.get('id')
        tm = ids.split('_')
        if tm[0] == 'identity':
            data = bm.api_del_identity(id=int(tm[1]))
            return api_response(data)
        elif tm[0] == 'business':
            data = bm.api_del_business(id=int(tm[1]))
            return api_response(data)
        elif tm[0] == 'enterprise':
            data = bm.api_del_enterprise(id=int(tm[1]))
            return api_response(data)
        else:
            data = dict()
            data['code'] = 300
            data['msg'] = '没有找到匹配的类型'
    return json_error('鉴权失败')


def api_getAllEC(request):
    auth = api_auth(request)
    if auth ==200:
        data = bm.api_get_enterprise()
        return api_response(data)


def api_searchEC(request):
    auth = api_auth(request)
    if auth ==200:
        typeCode_id = request.GET.get('typeCode_id')
        data = bm.api_get_enterprise_like(typeCode_id=typeCode_id)
        return api_response(data)


def api_analysis_vi_type_id(request):
    auth = api_auth(request)
    if auth ==200:
        vi_type_id = request.GET.get('vi_type_id')
        data = bm.api_analysis_vi_type_id(vi_type_id)
        return api_response(data)


def api_get_platform(request):
    auth = api_auth(request)
    if auth == 200:
        data = bm.api_get_platform()
        return api_response(data)


def api_get_type(request):
    auth = api_auth(request)
    if auth == 200:
        platform_id = request.Get.get('platform_id')
        if platform_id:
            data = bm.api_get_pt(platformCode_id=platform_id)
            return api_response(data)
        else:
            data = bm.api_get_pt()
            return api_response(data)


def api_get_app(request):
    auth = api_auth(request)
    if auth == 200:
        platform_id = request.Get.get('platform_id')
        type_id = request.Get.get('type_id')
        if platform_id and type_id:
            data = bm.api_get_pa(platformCode_id=platform_id, typeCode=type_id)
            return api_response(data)
        else:
            data = bm.api_get_pt()
            return api_response(data)


def api_alter_platform(request):
    auth = api_auth(request)
    if auth == 200:
        ids = request.Get.get('ids')
        if ids:
            data = bm.api_alter_platform(ids)
            return api_response(data)


def api_alter_type(request):
    auth = api_auth(request)
    if auth == 200:
        ids = request.Get.get('ids')
        if ids:
            data = bm.api_alter_pt(ids)
            return api_response(data)


def api_alter_app(request):
    auth = api_auth(request)
    if auth == 200:
        ids = request.Get.get('app_id')
        if ids:
            data = bm.api_alter_pa(ids)
            return api_response(data)

def api_updateEC(request):
    auth = api_auth(request)
    if auth ==200:
        en = request.GET.get('en')
        id = request.GET.get('id')
        user = str(request.user)
        rdata = bm.api_get_enterprise(en=en)
        if not rdata['data']:
            data = bm.api_alter_enterprise(ids=id,en=str(en).strip().upper(),user=user)
        else:
            data = {'code':400,'msg': f'当前企业英文[{en}]已经存在，请换一个'}
        return api_response(data)

def api_createEC(request):
    auth = api_auth(request)
    if auth ==200:
        en = request.GET.get('en')
        name = request.GET.get('name')
        typeCode_id = request.GET.get('typeCode_id')
        comment = request.GET.get('comment')
        user = str(request.user)
        if user in ['admin','haowj','guozh']:
            rdata = bm.api_create_enterprise(typeCode_id=typeCode_id,user=user,en=en,name=name,comment=comment)
            return api_response(rdata)
        return json_error('请找管理员进行添加')

def api_get_ns_vi_rule(request):
    auth = api_auth(request)
    if auth == 200:
        ids = request.GET.get('platformCode_id')
        if ids:
            data = bm.api_dpi_ns_vi(platformCode_id=ids)
        else:
            data = bm.api_dpi_ns_vi()
        return api_response(data)