import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dataplatform.models import PhoneApplicationsUser, PhoneNumber
from dpi.models import EnterpriseCoding, IdentityTypeCoding
from .tools import authentication, json_error, json_response

log = logging.getLogger(__file__)
@login_required(login_url='/admin/login/')
def get_phone_number_info(request):
    auth = authentication(request)
    if auth == 200:
        p_data = PhoneNumber.objects.filter(status=1).values().order_by('-update_time')
        data_one = list()
        for i in p_data:
            tme = PhoneApplicationsUser.objects.filter(status=1, phoneNumber=i['phoneNumber'])
            i.update({'applicationsNumber': len(tme)})
            data_one.append(i)
        return render(request, 'dataplatform/home.html', {'data': data_one})
    return auth


def get_app_info(request):
    """
    根据手机号码查询，应用详情信息
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            ids = request.GET.get('ids')
            data = PhoneApplicationsUser.objects.filter(status=1, phoneNumber=ids).values().order_by('-update_time')
            data_data = list()
            for i in data:
                i.update({'applicationsType': IdentityTypeCoding.objects.get(id=i['applicationsType']).identityType})
                i.update({'applicationsName': EnterpriseCoding.objects.get(id=i['applicationsName']).name})
                data_data.append(i)
            return json_response(data_data)
        except Exception as e:
            log.error(f'手机号详细信息查询：{str(e)}')
            return json_error(str(e))
    return auth


def set_phone_number_info(request):
    """
    添加手机号信息
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            phone_number = request.GET.get('phoneNumber')
            phone_type = request.GET.get('phoneType')
            utilize_user = request.GET.get('utilizeUser')
            user = request.user
            tem = PhoneNumber.objects.update_or_create(phoneNumber=phone_number, status=1)
            if not tem[1]:
                return json_error('手机号已存在，请勿重复添加！')
            PhoneNumber.objects.filter(phoneNumber=phone_number, status=1).update(status=1,
                                                                                  user = str(user),
                                                                                  phoneType = phone_type,
                                                                                  utilizeUser=utilize_user)
            return json_response("Added Successfully！")
        except Exception as e:
            log.error(f'新增手机号失败，原因：{str(e)}')
            return json_error(str(e))
    return auth


def del_phone_number_info(request):
    """
    删除手机号码
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            ids = request.GET.get('ids')
            PhoneNumber.objects.filter(id=ids).update(status=0)
            return json_response('del Successfully!')
        except Exception as e:
            log.error(f'删除手机号失败，原因：{str(e)}')
            return json_error(str(e))
    return auth


def del_applications_info(request):
    """
    删除手机应用账户
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            ids = request.GET.get('ids')
            PhoneApplicationsUser.objects.filter(id=ids).update(status=0)
            return json_response('delete Successfully!')
        except Exception as e:
            log.error(f'删除应用账号失败, 原因：{str(e)}')
            return json_error(str(e))
    return auth


def alter_phone_number_info(request):
    """
    更新手机号信息
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            ids = request.GET.get('ids')
            phoneNumber = request.GET.get('phoneNumber')
            phoneType = request.GET.get('phoneType')
            utilizeUser = request.GET.get('utilizeUser')
            PhoneNumber.objects.filter(id=ids).update(phoneNumber=phoneNumber,
                                                      phoneType=phoneType,
                                                      utilizeUser=utilizeUser)
            return json_response('alter Successfully!')
        except Exception as e:
            log.error(f'更新手机号信息失败, 原因：{str(e)}')
            return json_error(str(e))
    return auth

def get_app_name(request):
    """
    查询智云平台app应用
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            app_name = EnterpriseCoding.objects.values('id', 'name').order_by('-update_time')
            app_type = IdentityTypeCoding.objects.values('id', 'identityType').order_by('-update_time')
            return json_response({'app_name':app_name, 'app_type': app_type})
        except Exception as e:
            log.error(f'智云平台APP应用数据查询失败,原因：{str(e)}')
            return json_error(f'智云平台APP应用数据查询失败,原因：{str(e)}')
    return auth


def set_phone_app_info(request):
    """
    提交手机应用信息到数据库
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            phone_number = request.GET.get('phone_number')
            app_type = request.GET.get('app_type')
            phone_app_info = request.GET.get('phone_app_info')
            app_user = request.GET.get('app_user')
            app_pass = request.GET.get('app_pass')
            tem = PhoneApplicationsUser.objects.update_or_create(applicationsType=app_type,
                                                                 applicationsName=phone_app_info,
                                                                 phoneNumber=phone_number)
            if not tem[1]:
                return json_error('手机号已存在，请勿重复添加！')
            PhoneApplicationsUser.objects.filter(applicationsType=app_type,
                                                 applicationsName=phone_app_info,
                                                 phoneNumber=phone_number).update(user=str(request.user),
                                                                                  applicationsUser=app_user,
                                                                                  applicationsPass=app_pass)
            return json_response("Added Successfully！")
        except Exception as e:
            log.error(f'手机应用数据插入数据库失败,原因：{str(e)}')
            return json_error(f'手机应用数据插入失败,原因：{str(e)}')
    return auth


def get_phone_application_info(request):
    """
    查询手机号下的指定应用名称
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            res = dict()
            ids = request.GET.get('ids')
            data = PhoneApplicationsUser.objects.filter(id=ids, status=1).values('id',
                                                                                 'phoneNumber',
                                                                                 'applicationsType',
                                                                                 'applicationsName',
                                                                                 'applicationsUser',
                                                                                 'applicationsPass'
                                                                                 )
            user_type = IdentityTypeCoding.objects.all().values('id', 'identityType')
            user_app = EnterpriseCoding.objects.all().values('id', 'name')
            res['data'] = data[0]
            res['ut'] = user_type
            res['ua'] = user_app
            return json_response(res)
        except Exception as e:
            log.error(f'查询手机号下的应用数据失败,原因：{str(e)}')
            return f'查询手机号下的应用数据失败,原因：{str(e)}'
    return auth

def alter_phone_application_info(request):
    """
    更新手机app应用
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            ids = request.GET.get('ids')
            phone_app_type = request.GET.get('alter_phone_app_type')
            phone_app_name = request.GET.get('alter_phone_app_info')
            phone_app_user = request.GET.get('alter_app_user')
            phone_app_passw = request.GET.get('alter_app_passwd')
            PhoneApplicationsUser.objects.filter(id=ids, status=1).update(
                applicationsType=phone_app_type,
                applicationsName=phone_app_name,
                applicationsUser=phone_app_user,
                applicationsPass=phone_app_passw
            )
            return json_response('alter Successfully!')
        except Exception as e:
            log.error(f'手机app数据跟新失败,原因：{str(e)}')
            return f'手机app数据跟新失败,原因：{str(e)}'
    return auth

