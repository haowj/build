# coding:utf-8
import time

__author__ = 'xcma'
import copy
from django.views.decorators.csrf import csrf_exempt

from checkout.base.tools import get_func_called, json_error, json_response
from dpi.control.dpi_conf_view import dcv,dpv
from dpi.control.iface import bm
from dpi.control.dao import enterprise
import logging
log = logging.getLogger(__name__)

def api_auth(request):
    if request.user.is_authenticated:
        return 200
    else:
        return json_error('权限不足',400)
def auth_error():
    return json_error('权限不足',400)
def api_response(data):
    # log.debug(data)
    if data['code'] == 200:
        return json_response(data['data'])
    else:
        return json_error(data['msg'])


def api_getDpiConfAll(request):
    auth = api_auth(request)
    if auth == 200:
        data = dcv.view_all_dpi_conf()
        return api_response(data)
def api_getNSPAll(request):
    auth = api_auth(request)
    if auth == 200:
        data = bm.api_get_platform()
        return api_response(data)


def api_getDpiMultimodeAll(request):
    auth = api_auth(request)
    if auth == 200:
        data = dcv.view_all_dpi_multimode()
        return api_response(data)

def api_createDPIConf(request):
    auth = api_auth(request)
    if auth == 200:
        rule_name = request.GET.get('rule_name').strip()
        vi_type_id = request.GET.get('vi_type_id').strip()
        multimode_id = request.GET.get('multimode_id').strip()
        rule_data = request.GET.get('rule_data').lstrip().rstrip()
        rule_begin_match = request.GET.get('rule_begin_match').lstrip().rstrip()
        rule_end_match = request.GET.get('rule_end_match').lstrip().rstrip()
        dpipcap_id = request.GET.get('dpipcap_id').strip()
        comment = request.GET.get('comment')
        user = str(request.user)
        data = dcv.view_create_dpi_conf(rule_name=rule_name,vi_type_id=vi_type_id,multimode_id=multimode_id,
                                    rule_data=rule_data,rule_begin_match=rule_begin_match,rule_end_match=rule_end_match,
                                    user=user,comment=comment,dpipcap_id=dpipcap_id,weight=1)
        return api_response(data)

def api_generateDpi(request):
    auth = api_auth(request)
    if auth == 200:
        dev_model = request.GET.get('dev_model')
        dev_model_id = request.GET.get('dev_model_id')
        comment = request.GET.get('comment')
        user = str(request.user)
        data = dcv.view_generateDpiFile(dev_model,dev_model_id,comment,user)
        return api_response(data)

def api_getDpiPcapAll(request):
    auth = api_auth(request)
    if auth == 200:
        id = request.GET.get('id')
        if id:
            data = dpv.getAll(id=id)
        else:
            data = dpv.getAll()
        return api_response(data)

def api_delDpiConf(request):
    auth = api_auth(request)
    if auth == 200:
        id = request.GET.get('id')
        status = request.GET.get('status')
        user = str(request.user)
        data = dcv.view_upgrade_dpi_conf(id,status=status,user=user)
        return api_response(data)

def api_getDpiConf(request):
    auth = api_auth(request)
    if auth == 200:
        id = request.GET.get('id')
        data = dcv.view_get_dpi_conf(id=id)
        return api_response(data)

def api_getPlatformViType(request):
    auth = api_auth(request)
    if auth == 200:
        nsp_id = request.GET.get('id')
        # id=0 则查询智云平台全部虚拟身份
        data = dcv.view_get_nsp_conf(int(nsp_id))
        return api_response(data)

def api_get_ec(request):
    auth = api_auth(request)
    if auth == 200:
        rlist = []
        name = request.GET.get('name')
        data = bm.api_get_ec_bt(name)
        if data['code'] ==200 :
            ebdata = data['data']
            for eb in ebdata:
                rdict = {}
                code = eb['code']
                eid = eb['id']
                typeCode_id = eb['typeCode_id']
                en = eb['en']
                bcode = eb['bcode']
                businessType = eb['businessType']
                name = eb['name']
                if not en:
                    en = '未找到英文名'
                    code = 'error'
                rdict['id'] = f'{bcode}-{code}-{eid}-{typeCode_id}'
                rdict['text']= f'{businessType}|{name}|{en}'
                rlist.append(copy.deepcopy(rdict))
        if rlist:
            return json_response(rlist)
        else:
            return json_error(rlist)

def api_set_weight(request):
    auth = api_auth(request)
    if auth == 200:
        order_id_str = request.GET.get('order')
        if order_id_str:
            order_id_list = str(order_id_str).split(',') if ',' in order_id_str else list(order_id_str)
            weight = 10
            cdata = []
            data = {'code':400,'msg':'更新失败'}
            try:
                dcv.view_update_dpiconf_init_weight()
                for cid in order_id_list:
                    data = dcv.view_upgrade_dpi_conf(cid,weight=weight,user='auto')
                    weight +=1
                    rstr = f'{cid}:{weight}'
                    cdata.append(str(rstr))
            except Exception as e:
                cdata.append(e)
            return api_response(data)
        return json_error('参数异常',400)
    return auth_error()

@csrf_exempt
def api_createDpiPcap(request):
    auth = api_auth(request)
    if auth==200:
        if request.method == "POST":
            user = str(request.user)
            file_obj = request.FILES.get('file')
            if file_obj:  # 处理附件上传到方法
                dpv.getPath(file_obj)
            vi_type_id = request.POST.get('pacp_vi_type_id').strip()
            taget_account = request.POST.get('taget_account').strip()
            mobileinfo_id = request.POST.get('mobileinfo_id').lstrip().rstrip()
            app_type = request.POST.get('app_type').lstrip().rstrip()
            app_version = request.POST.get('app_version').lstrip().rstrip()
            comment = str(request.POST.get('pcap_comment')).strip().replace('\n',';').replace("\t", "").replace(" ","")
            data = dpv.createPcap(vi_type_id=vi_type_id,taget_account=taget_account,mobileinfo_id=mobileinfo_id,
            app_type=app_type,app_version=app_version,comment=comment,user=user)
            return api_response(data)


def api_get_net_safety_platform(request):
    """查询网安平台"""
    try:
        from dpi.models import NetSafetyPlatform
        data = NetSafetyPlatform.objects.all().values('id', 'wname')
    except Exception as e:
        return json_error(str(e))
    return json_response(data)


def api_get__app_pro_code(request):
    """查询中间<==>网安平台"""
    try:
        from dpi.models import AppProCode, EnterpriseCoding
        import os
        import xlsxwriter


        vi_id = request.GET.get('vid')
        tem = AppProCode.objects.filter(platformCode_id=vi_id)
        wname = tem[0].platformCode.wname
        if os.path.exists(os.path.join('/home/zjzy/output/excel/', '虚拟身份.xlsx')):
            os.remove(os.path.join('/home/zjzy/output/excel/', '虚拟身份.xlsx'))
        save_book = xlsxwriter.Workbook(os.path.join('/home/zjzy/output/excel/', '虚拟身份.xlsx'))
        save_sheet = save_book.add_worksheet('虚拟身份对照表')
        save_sheet.write(0, 0, '中建平台')
        save_sheet.write(0, 1, f'{wname}平台')
        cols = 1
        for i in tem:
            t_data = EnterpriseCoding.objects.filter(id=i.vi_ec_id)
            if len(t_data) > 0:
                t_data = t_data[0]
                save_sheet.write(cols, 0, t_data.typeCode.code + t_data.code + '?')
                save_sheet.write(cols, 1, i.ns_code)
                cols += 1
        save_book.close()
    except Exception as e:
        return json_error(str(e))
    return json_response(f'http://test.plug.superhcloud.com/excel/虚拟身份.xlsx')