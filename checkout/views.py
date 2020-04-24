from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from checkout.control.processManage import processManage
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from checkout.base.tools import json_response,json_error,get_func_called
import logging
import hashlib,json
from build.settings import SIGN_KEY

from checkout.control.bizManage import bm
log = logging.getLogger(__name__)

def getSign(param):
    """md5($mobile.$mac.'pythonapi')"""
    ps = ''
    log.debug('参与计算的参数:{}'.format(param))
    pdict = sorted(param.items(), key=lambda param: param[0], reverse=False)
    for i in pdict:
        ps += '{}={}'.format(i[0].lower(), i[1])
    cmd = 'pythonapi{}'.format(ps).replace('\"','\'')
    log.debug('str:{}'.format(cmd))
    sign = hashlib.md5(cmd.encode('utf-8')).hexdigest()
    log.debug(sign)
    return sign

def check_sign(request,type):
    para_dict = {}
    para_sign=''
    para = request.GET if type=='get' else request.POST
    for k, v in para.items():
        if k != 'sign':
            para_dict[k] = v
        else:
            para_sign = v
    sign = getSign(para_dict)
    if sign == para_sign:
        log.debug('鉴权成功')
        return True
    log.debug('鉴权失败：{}={}?{}'.format(sign, para_sign, sign == para_sign))
    return False

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
    auth = 400
    if request.user.is_authenticated:
        auth = 200
    return auth

def api_response(data):
    log.debug(data)
    if data['code'] == 200:
        return json_response(data['data'])
    else:
        return json_error(data['msg'])


class checkout_api:
    # api
    @csrf_exempt
    def get_task(self, request):
        if request.method == 'POST':
            sign = request.POST.get('sign')
            if sign == SIGN_KEY:
                kwargs = request.POST.get('data')
                return HttpResponse(processManage(kwargs))
            return HttpResponse("无效参数")
        return json_error('鉴权失败')

    def getBasicsInfo_v(self, request):
        if api_auth(request) == 200:
            data = bm.api_getBasicsInfoList('basicsInfo')
            return api_response(data)
        return json_error('鉴权失败')

    def addBasicsInfo_v(self, request):
        if api_auth(request) == 200:
            k = request.GET.get('keys')
            v = request.GET.get('values')
            data = bm.api_setBasicsInfoList('basicsInfo', k, v)
            return api_response(data)
        return json_error('鉴权失败')

    def delBasicsInfo_v(self, request):
        if api_auth(request) == 200:
            k = request.GET.get('keys')
            data = bm.api_delBasicsInfoList('basicsInfo', k)
            return api_response(data)
        return json_error('鉴权失败')

    def add_case(self, request):
        if api_auth(request) == 200:
            try:
                if request.POST:
                    dev_model = request.GET.get('dev_model')
                    set_name = request.GET.get('set_name')
                    user = request.user
                    return json_response('add ok')
            except Exception as e:
                log.error(e)
                return json_error(str(e))
        return json_error('鉴权失败')

    def getDevModelList_v(self, request):
        if api_auth(request) == 200:
            oem_name = request.GET.get('oem_name')
            data = bm.api_getDevModelList(oem_name)
            return api_response(data)
        return json_error('鉴权失败')

    def getTestCaseList_v(self, request):
        if api_auth(request) == 200:
            oem_name = request.GET.get('oem_name')
            data = bm.api_getDevModelList(oem_name)
            return api_response(data)
        return json_error('鉴权失败')

    def delTestAP_v(self, request):
        if api_auth(request) == 200:
            ids = request.GET.get('id')
            data = bm.api_delTestAP(ids)
            return api_response(data)
        return json_error('鉴权失败')

    def delTestAPSetList_v(self, request):
        if api_auth(request) == 200:
            ids = request.GET.get('id')
            data = bm.api_delTestAPSetList(ids)
            return api_response(data)
        return json_error('鉴权失败')

    def getTestAPSetListInfo_v(self, request):
        if api_auth(request) == 200:
            ids = request.GET.get('id')
            data = bm.api_getTestAPSetListInfo(ids)
            return api_response(data)
        return json_error('鉴权失败')

    def getTestSetListInfo_v(self, request):
        if api_auth(request) == 200:
            ids = request.GET.get('id')
            data = bm.api_getTestSetListInfo(ids)
            return api_response(data)
        return json_error('鉴权失败')


    def delTestCase_v(self, request):
        if api_auth(request) == 200:
            ids = request.GET.get('id')
            data = bm.api_delTestCase(ids)
            return api_response(data)
        return json_error('鉴权失败')

    def delTestSet_v(self, request):
        if api_auth(request) == 200:
            ids = request.GET.get('id')
            data = bm.api_delTestSet(ids)
            return api_response(data)
        return json_error('鉴权失败')


    def addTestCase_v(self, request):
        if api_auth(request) == 200:
            args_remark = request.GET.get('args_remark')
            args_command = request.GET.get('args_command')
            args_name = request.GET.get('args_name')
            args_vales = request.GET.get('args_vales')
            data = bm.api_addTestCase(args_remark=args_remark, args_command=args_command, args_name=args_name,
                                    args_vales=args_vales, args_operator=str(request.user))
            return api_response(data)
        return json_error('鉴权失败')

    def addTestSet_v(self, request):
        if api_auth(request) == 200:
            case_name = request.GET.get('set_name')
            case_action = request.GET.get('case_action')
            data = bm.api_addTestSet(case_name=case_name,case_action=case_action,operator=str(request.user))
            return api_response(data)
        return json_error('鉴权失败')


    def addTestApSet_v(self,request):
        if api_auth(request) == 200:
            dev_model_id = request.GET.get('dev_model_id')
            caseId = request.GET.get('testSetId')
            data = bm.api_addTestApSet(deviceID_id=dev_model_id,caseID=caseId,operator=str(request.user))
            return api_response(data)
        return json_error('鉴权失败')

    def upTestAP_v(self, request):
        if api_auth(request) == 200:
            ids = request.GET.get('ids')
            ip = request.GET.get('ip')
            port = request.GET.get('port')
            dev_user = request.GET.get('user')
            dev_pwd = request.GET.get('pwd')
            comment = request.GET.get('remark')
            data = bm.api_upTestAP(ids, dev_ip=ip, dev_port=port, dev_user=dev_user, dev_password=dev_pwd,
                                   operator=str(request.user), remark=comment)
            return api_response(data)
        return json_error('鉴权失败')

    def upTestCase_v(self, request):
        if api_auth(request) == 200:
            ids = request.GET.get('ids')
            args_remark = request.GET.get('args_remark')
            args_command = request.GET.get('args_command')
            args_name = request.GET.get('args_name')
            args_vales = request.GET.get('args_vales')
            data = bm.api_upTestCase(ids, args_remark=args_remark, args_command=args_command, args_name=args_name,
                                     args_vales=args_vales, args_operator=str(request.user))
            return api_response(data)
        return json_error('鉴权失败')

    def addTestAP_v(self, request):
        if api_auth(request) == 200:
            oem_name = request.GET.get('oem_name')
            sn = request.GET.get('sn')
            ip = request.GET.get('ip')
            port = request.GET.get('port')
            dev_model = request.GET.get('dev_model')
            dev_user = request.GET.get('user')
            dev_pwd = request.GET.get('pwd')
            comment = request.GET.get('comment')
            data = bm.api_addTestAP(oem_name=oem_name, dev_sn=sn, dev_ip=ip, dev_port=port, dev_model=dev_model,
                                    dev_user=dev_user, dev_password=dev_pwd, operator=str(request.user), remark=comment)
            return api_response(data)
        return json_error('鉴权失败')

    def getTestAPInfo_v(self, request):
        if api_auth(request) == 200:
            id = request.GET.get('id')
            data = bm.getTestAPInfo(id)
            return api_response(data)
        return json_error('鉴权失败')

    def runTestAP_v(self, request):
        if api_auth(request) == 200:
            caseSetIdList = request.GET.get('caseSetIdList')
            dev_model_id = request.GET.get('dev_model_id')
            user = request.user
            data = bm.runTestAP(caseSetIdList, dev_model_id, user)
            return api_response(data)
        return json_error('鉴权失败')

    def getTestSet_v(self, request):
        if api_auth(request) == 200:
            id = request.GET.get('id')
            data = bm.getTestSet(id)
            return api_response(data)
        return json_error('鉴权失败')

    def getTestCase_v(self, request):
        if api_auth(request) == 200:
            id = request.GET.get('id')
            data = bm.get_test_case(id)
            return api_response(data)
        return json_error('鉴权失败')

    def getCaseResult_v(self, request):
        if api_auth(request) == 200:
            ids = request.GET.get('case_result')
            data = bm.get_case_result(ids)
            return api_response(data)
        return json_error('鉴权失败')

    def getRecord_v(self, request):
        if api_auth(request) == 200:
            ids = request.GET.get('case_result')
            data = bm.get_strategy_data(ids)
            return api_response(data)
        return json_error('鉴权失败')

# view
@login_required(login_url='/admin/login/')
def show_case(request):
    auth = authentication(request)
    if auth == 200:
        scl = bm.getTestCase()
        return render(request, 'checkout/showCase.html', {'data': scl})
    return auth


@login_required(login_url='/admin/login/')
def data_case(request):
    auth = authentication(request)
    if auth == 200:
        return render(request, 'checkout/addCase.html')
    return auth


@login_required(login_url='/admin/login/')
def testApList(request):
    auth = authentication(request)
    if auth == 200:
        data = bm.view_gettestApListData()
        return render(request, 'checkout/testApList.html', {'data': data})
    return auth


@login_required(login_url='/admin/login/')
def testApSetList(request):
    auth = authentication(request)
    if auth == 200:
        data = bm.view_getApSetList()
        return render(request, 'checkout/testApSetList.html', {'data': data})
    return auth


@login_required(login_url='/admin/login/')
def testSetList(request):
    auth = authentication(request)
    if auth == 200:
        data = bm.view_getSetList()
        tdata = bm.view_getTestCase()
        return render(request, 'checkout/testSetList.html', {'data': data, 'tdata': tdata})
    return auth


@login_required(login_url='/admin/login/')
def testCaseList(request):
    auth = authentication(request)
    if auth == 200:
        data = bm.view_getTestCase()
        return render(request, 'checkout/testCaseList.html', {'data': data})
    return auth


@login_required(login_url='/admin/login/')
def testRecordList(request):
    auth = authentication(request)
    if auth == 200:
        data = bm.view_getRecordList()
        return render(request, 'checkout/testRecordList.html', {'data': data})
    return auth


@login_required(login_url='/admin/login/')
def del_case(request):
    auth = authentication(request)
    if auth == 200:
        pass


