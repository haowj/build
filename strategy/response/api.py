#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
from strategy.base.tools import authentication, JsonError, JsonResponse
from strategy.control.git_tool import get_tag_list, GitProcess
from strategy.conf.path import getProjeck_path, package_contains_path_dict
from strategy.models import S_T_V_DB
from strategy.base.op_val import insert_into_super_task, get_build_log, \
    get_info_super_data_package, get_info_online_log, get_info_super_api_loader_package, get_super_task_data, \
    get_tag_info
from strategy.base.tools import executionShell
from strategy.base.super_data_build import toBuild, get_superd, toBuild_test
from strategy.base.super_api_build import SuperApi, get_log_info_super_api_loader
from strategy.base.online import Online
from strategy.base.super_data_package import PackageDB
from strategy.base.super_api_package import SuperApiPackage
from strategy.base.super_proxy_build import get_proxy_res, to_build
import logging

log = logging.getLogger(__name__)

def tag_add(request):
    """
    新增版本
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            tag = request.GET.get('tag')
            sw = request.GET.get('sw')
            comment = str(request.GET.get('comment')).strip().replace('\n', ';').replace("\t", "").replace(" ", "")
            user = request.user
            msg = '操作人:build[{}],说明:{}'.format(user, comment)
            if sw and tag and comment:
                get_data_ass = get_tag_info(project_name=sw, tag=tag, status=1)
                if get_data_ass:
                    if len(get_data_ass) > 0:
                        return JsonError(f"请勿重复添加相同的版本号:{tag}")
                path, branch = getProjeck_path(sw)
                log.debug('sw:{},pj_path:{},msg:{},tag:{}'.format(sw, path, msg, tag))
                git = GitProcess(path)
                git.init_project()
                git.createTag(tag, msg, sw, path, branch, str(user))
            else:
                return JsonError(f"参数数据缺失：tag={tag}、sw={sw}、comment={comment}")
            return JsonResponse(1)
        except Exception as e:
            log.error(e)
            return JsonError(str(e))
    return auth


def connector_add(request):
    """
    添加连接器版本
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            tag = request.GET.get('tag')
            dev_model = request.GET.get('dev_model')
            comment = request.GET.get('comment')
            connector_type = request.GET.get('connector_type')
            user = str(request.user)
            if tag and dev_model:
                data = insert_into_super_task(tag,dev_model,connector_type,comment,user)
                if type(data) is str:
                    return JsonError(data)
            return JsonResponse('upload ok!')
        except Exception as e:
            log.error(e)
            return JsonError(str(e))
    return auth


def tag_info(request):
    """
    根据Id获取版本详情
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth==200:
        try:
            tag_sw = str(request.GET.get('tag'))
            tag = tag_sw.split('_')[0]
            sw = tag_sw.split('_')[1]
            if tag:
                path, branch = getProjeck_path(sw)
                git = GitProcess(path)
                git.init_project()
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


def del_tag(request):
    """
    删除指定版本号
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            tag = request.GET.get('tag')
            project_type = request.GET.get('sw')
            project_path,branch = getProjeck_path(project_type)
            if project_path and tag:
                git = GitProcess(project_path)
                data = git.delTag(tag,project_type)
                return JsonResponse(data)
            else:
                return JsonError('param error')
        except Exception as e:
            log.error(e)
            return JsonError(str(e))
    return auth


def super_data_build(request):
    """
    构建插件版本
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth==200:
        dev_model = request.GET.get('dev_model')
        tag = request.GET.get('tag')
        reason = str(request.GET.get('reason')).strip().replace('\n',';').replace("\t", "").replace(" ","")
        try:
            data = toBuild(dev_model, tag, reason,str(request.user))
            return JsonResponse(data)
        except Exception as e:
            return JsonError(str(e))
    return auth


def super_data_build_test(request):
    """
    构建插件版本 测试版本
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth==200:
        dev_model = request.GET.get('dev_model')
        branch = request.GET.get('branch')
        reason = str(request.GET.get('reason')).strip().replace('\n',';').replace("\t", "").replace(" ","")
        try:
            data = toBuild_test(dev_model, branch, reason,str(request.user))
            return JsonResponse(data)
        except Exception as e:
            return JsonError(str(e))
    return auth


def super_data_build_result(request):
    """
    获取super data 插件构建结果
    :param request:
    :return:
    """
    auth = authentication(request)
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
                build_status = get_superd(dev_model,tag,reason,user,is_test)
                return JsonResponse(build_status)
            return JsonError('参数异常')
        except Exception as e:
            return JsonError(str(e))
    return auth


def build_log_info(request):
    """
    获取super data 构建日志数据
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            ids = int(request.GET.get('id'))
            if ids:
                data = get_build_log(id=ids)[0]
                try:
                    build_result = eval(data['build_result'])
                except:
                    build_result = data['build_result']
                return JsonResponse(build_result)
        except Exception as e:
            log.error(e)
            return JsonError(str(e))
    return auth


def get_filter_package_info(request):
    """
    打包
        根据设备型号查找打包结果
    :param request:
    :return:
    """

    auth = authentication(request)

    if auth == 200:
        try:
            t = request.GET.get('t')
            dev_model = request.GET.get('dev_model')

            if t=='pg':
                package_contains_path_type = request.GET.get('package_contains_path_type')
                package_contains_path = package_contains_path_dict[package_contains_path_type]
                data = get_info_super_data_package(dev_model=dev_model,
                                                    package_contains_path_type=package_contains_path_type,
                                                    package_contains_path=package_contains_path)[:100]
            elif t=='sapiloader':
                data = get_info_super_data_package(dev_model=dev_model)[:100]
            else:
                data = {}
            return JsonResponse(data)
        except Exception as e:
            log.error(e)
            return JsonError(str(e))
    return auth


def get_package_one_info(request):
    """
    打包：
        根据ID查询打包结果
        查询插件打包结果
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            ids = request.GET.get('id')
            types = request.GET.get('type')
            if ids:
                if types=='pg':
                    data = get_info_super_data_package(id=ids)
                elif types=='sapiloader':
                    data = get_info_super_api_loader_package(id=ids)
                else:
                    data =[0]
                return JsonResponse(data)
        except Exception as e:
            log.error(e)
            return JsonError(str(e))
    return auth


def set_online_log(request):
    """
    插入上线日志数据
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            t = request.GET.get('t')
            user = str(request.user)
            rel = Online()

            if t == 'pg':
                pack_id = request.GET.get('id')

                save_target_path = request.GET.get('save_target_path')
                if save_target_path == 'slave':
                    save_target_path = '/sapi/slave'
                else:
                    save_target_path = '/sapi/master'
                run_cmd = request.GET.get('run_cmd')
                unpack_cmd = request.GET.get('unpack_cmd')
                monitor_time = request.GET.get('monitor_time')
                reconnect_time = request.GET.get('reconnect_time')
                rom_version = request.GET.get('rom_version')
                comment = request.GET.get('comment')
                data = rel.do_release(pack_id, user,
                                      comment=comment,
                                      save_target_path=save_target_path,
                                      run_cmd=run_cmd,
                                      unpack_cmd=unpack_cmd,
                                      monitor_time=monitor_time,
                                      reconnect_time=reconnect_time,
                                      rom_version=rom_version)
            else:
                s_pack_id = request.GET.get('id')
                area = request.GET.get('area')
                comment_api = request.GET.get('commentApi')
                data = rel.release_super_api_loader(s_pack_id, area, comment_api, user)
            return JsonResponse(data)
        except Exception as e:
            log.error(f'数据上线失败，原因：{e}')
            return JsonResponse({'code': 500, 'err': str(e)})
    return auth

def get_online_log(request):
    """
    根据Id获取上线日志
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        try:
            id = request.GET.get('id')
            sid = str(id).split('_')[0]
            t = str(id).split('_')[1]
            if sid and t:
                data = get_info_online_log(id=sid, rtype=t)
                return JsonResponse(data)
            else:
                msg = '参数异常'
                raise msg
        except Exception as e:
            log.error(e)
            return JsonError(str(e))
    return auth


def get_info_super_api_loader(request):
    """
    获取sapiloader 构建日志
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth==200:
        try:
            dev_model = request.GET.get('dev_model')
            tag = request.GET.get('tag')
            reason = str(request.GET.get('reason')).strip().replace('\n', ';').replace("\t", "").replace(" ", "")

            user = str(request.user)
            if dev_model:
                build_status = get_log_info_super_api_loader(dev_model,tag,reason,user)
                return JsonResponse(build_status)
            return JsonError('参数异常')
        except Exception as e:
            return JsonError(str(e))
    return auth


def super_api_loader_build(request):
    """
    构建super loader 加载器
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth==200:
        dev_model = request.GET.get('dev_model')
        tag = request.GET.get('tag')
        reason = str(request.GET.get('reason')).strip().replace('\n',';').replace("\t", "").replace(" ","")
        try:
            sbl = SuperApi()
            data = sbl.to_build(dev_model, tag, reason,request.user)
            return JsonResponse(data)
        except Exception as e:
            return JsonError(str(e))
    return auth


def get_super_api_loader_package(request):
    """
    根据设备型号获取sapiloader包
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        dev_model = request.GET.get('dev_model')
        data = get_info_super_api_loader_package(dev_model=dev_model)
        if type(data) is str:
            return JsonError(data)
        else:
            return JsonResponse(data)
    return auth

def get_tag_list_info(request):
    """
    获取tag 列表
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        dev_model = str(request.GET.get('dev_model'))
        package_contains_path = str(request.GET.get('package_contains_path'))

        tag_data = get_tag_info(status=1)
        super_data = ['RC']
        super_api_load = ['RC']
        connector = ['RC']
        if tag_data:
            for t_i in tag_data:
                if 'superd' in t_i['project_name']:
                    super_data.append(t_i['tag'])
                elif 'sapiloader' in t_i['project_name']:
                    super_api_load.append(t_i['tag'])
                elif 'connector' in t_i['project_name']:
                    connector.append(t_i['tag'])
        try:
            # connector tag data
            if package_contains_path != "None":
                if 'shell_sapiloader' == package_contains_path:
                    connector_tag = S_T_V_DB.objects.filter(supertack_type=package_contains_path).values().order_by('-update_time')
                    connector_tag_list = ['RC']
                    cont = 0
                    cons = 0
                    for i in connector_tag:
                        if cont < 5:
                            if 'fitall' in i['dev_model']:
                                connector_tag_list.append(i)
                                cont += 1
                            elif cons < 5:
                                if dev_model in i['dev_model']:
                                    connector_tag_list.append(i)
                                    cons += 1
                        elif len(connector_tag_list) < 10:
                            if dev_model in i['dev_model']:
                                connector_tag_list.append(i)
                        else:
                            break
                    connector_tag = connector_tag_list
                else:
                    connector_tag = [{'dev_model': dev_model, 'supertack_version': i} for i in connector]
                    if len(connector) > 0:
                        connector_tag = [{'dev_model': dev_model, 'supertack_version': i} for i in connector[:10]]
                return JsonResponse(connector_tag)

            # super data tag data
            if len(super_data) > 10:
                super_data = super_data[:10]

            # super api loader tag data
            if len(super_api_load) > 10:
                super_api_load = super_api_load[:10]

            data = {'superD': super_data, 'superApi': super_api_load}
            return JsonResponse(data)
        except Exception as e:
            log.warning(f'获取版本信息失败{e}')
            return JsonError(e)
    return auth

def set_strategy(request):
    """
    根据型号进行打包 superD
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth==200:
        user = str(request.user)
        dev_model = str(request.GET.get('dev_model_id'))
        package_contains_path = str(request.GET.get('package_contains_path'))
        default_conf = request.GET.get('package_contains_type')
        superdcf_id = request.GET.get('superdcf_id')
        zdpi_sig_id = request.GET.get('zdpi_sig_id')
        superd_id = request.GET.get('superd_id')
        pack_type = request.GET.get('pack_type')
        docking_solution = request.GET.get('docking_solution')
        connector = request.GET.get('connector')
        pac_info = PackageDB(user,
                             dev_model,
                             package_contains_path,
                             superd_id,
                             connector,
                             superdcf_id,
                             zdpi_sig_id,
                             pack_type,
                             docking_solution,
                             default_conf)
        data = pac_info.package_build
        if data:
            return JsonError(data)
        else:
            return JsonResponse('成功')
    return auth


def set_sapiloder_package(request):
    """
    根据型号进行打包 spailoder
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth==200:
        user = str(request.user)
        dev_model = request.GET.get('id')
        spailoader_edi = request.GET.get('ver')

        pac_info = SuperApiPackage(dev_model,
                                   spailoader_edi,
                                   user
                                   )
        data = pac_info.package_build
        if data:
            return JsonError(data)
        else:
            return JsonResponse('成功')
    return auth

def set_proxy_package(request):
    """
    新增反向代理包
    :param request:
    :return:
    """
    auth = authentication(request)
    if auth == 200:
        user = str(request.user)
        dev_model = request.GET.get('dev_model')
        try:
            data = to_build(dev_model, user)
            return JsonResponse(data)
        except Exception as e:
            return JsonError(str(e))
    return auth


def get_proxy_down_url(request):
    """
    获取反向代理下载路径
    :param request:
    :return:
    """
    from strategy.base.tools import check_sign
    from strategy.models import R_P_DB
    if check_sign(request):
        try:
            dev_model = request.GET.get('dev_model')
            data = R_P_DB.objects.filter(dev_model=dev_model).values().order_by('-id').first()
            return JsonResponse(data)
        except Exception as e:
            log.error(f'获取反向代理包下载信息失败,原因：{str(e)}')
            return JsonError(f'获取反向代理包下载信息失败,原因：{str(e)}')
    return JsonError('鉴权失败')