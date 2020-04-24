#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
from strategy.conf.path import docking_solution, package_contains_path_dict, c_sapiloader, shell_sapiloader, \
    superd_project_path, superd_build_shell_path, out_super_conf_data, config_branch, out_dpi_conf_data, \
    out_base_path, sapiloader_c_build_shell_path, plug_domain, proxy_client_build_shell_path
from strategy.base.op_db import get_data_base,get_data_base_filter, get_data_base_order, insert_into_data, \
    get_data_base_one, exclude_data_base, create_data
from strategy.control.ap_api import ap_api
from strategy.control.support_api import sp_api
from strategy.base.tools import mkdir, get_md5_big, file_is_have, time_stamp
from strategy.control.git_tool import git_code, cp_file, executionShell
from strategy.control.git_xx import GitProcess
import logging
import time
import platform


log = logging.getLogger(__name__)


def get_all_version_data():
    """
    D_M_DB   表数据表

    device model data base

    :return:
    """
    device_model = get_data_base('D_M_DB')
    if 'error' in str(device_model):
        log.warning(f'获取型号数据失败，原因 ：{device_model}')
        device_model = {}
    data = {
        'dev_model': device_model,
        'package_contains_path': package_contains_path_dict,
        'docking_solution': docking_solution,
    }
    return data


def get_super_data(**kwargs):
    """
    D_M_DB   表数据表
    S_D_DB   表数据表
    Device Model Data Base
    SuperD Data BaseB

    :return:
    """
    superdinfo = None
    device_model = get_data_base_filter('D_M_DB', **kwargs)
    if 'error' not in str(device_model):
        superdinfo = get_data_base_filter('S_D_DB', dev_model=device_model[0]['zy_model'])
        if 'error' in str(superdinfo):
            superdinfo = None
    data = {
        'superdInfo': superdinfo,
        }

    return data

def get_super_tack_data(tn, dev_id):
    """
    S_T_V_DB   表数据表
    SuperTack Version Data Base

    :return:
    """

    if tn == c_sapiloader:
        ty = 'supertack'
    elif tn == shell_sapiloader:
        ty = 'superctl'
    else:
        return '参数错误'

    info = dict()
    data = list()
    dev_model = get_data_base_filter('D_M_DB', id=dev_id)
    if type(dev_model) != str:
        if dev_model:
            super_tack = get_data_base_filter('S_T_V_DB', supertack_type=tn, dev_model=dev_model[0]['oem_model'])
            if type(super_tack) != str:
                for i in super_tack[:5]:
                    info['id'] = i['id']
                    info['version'] = i['supertack_version']
                    info['comment'] = i['comment']
                    info['update_time'] = i['update_time']
                    info['type'] = ty
                    data.append(info)
            else:
                return super_tack
        else:
            super_tack = get_data_base_filter('S_T_V_DB', supertack_type=tn)
            if type(super_tack) != str:
                for i in super_tack[:10]:
                    info['id'] = i['id']
                    info['version'] = i['supertack_version']
                    info['comment'] = i['comment']
                    info['update_time'] = i['update_time']
                    info['type'] = ty
                    data.append(info)
            else:
                return super_tack
    return data

def get_super_d_config_data(**kwargs):
    """
    D_M_DB   表数据表
    S_D_C_F_DB   表数据表
    Device Model Data Base
    SuperD Config File Data Base

    :return:
    """

    if kwargs:
        device_model = get_data_base_filter('D_M_DB', **kwargs)
        if type(device_model) is str:
            return None
        superdcf = get_data_base_filter('S_D_C_F_DB', dev_model=device_model[0]['zy_model'])
        if type(superdcf) is str:
            return None
        return superdcf
    else:
        superdcf = get_data_base('S_D_C_F_DB')
        return superdcf

def get_dpi_config(**kwargs):
    """
    D_M_DB   表数据表
    S_D_C_F_DB   表数据表
    Device Model Data Base
    Deep Packet Inspection Config Version Data Base

    :return:
    """
    if kwargs:
        device_model = get_data_base_filter('D_M_DB', **kwargs)
        if type(device_model) is str:
            return None
        dpi_config = get_data_base_filter('dpiConfigVersion', **kwargs)
        if type(dpi_config) is str:
            return None
        return dpi_config
    else:
        dpi_config = get_data_base_filter('dpiConfigVersion')
        return dpi_config


def get_oem_data():
    """
    获取厂商数据
    :return:
    """
    data = get_data_base('O_E_M_DB')
    return data


def get_super_task_data():
    """
    获取 superTask 数据
    :return:
    """
    data = get_data_base('S_T_V_DB')
    if type(data) is str:
        log.warning(f'superTask 查询错误， {data}')
        return []
    return data


def get_super_api_loader_data(**kwargs):
    """
    获取sapiloder 信息
    :return:
    """
    if kwargs:
        data = get_data_base_filter('S_A_L_DB', **kwargs)
    else:
        data = get_data_base('S_A_L_DB')
    return data


def insert_into_oem(**kwargs):
    """
       插入厂商数据
       :return:
       """
    if kwargs:
        data = insert_into_data('O_E_M_DB', **kwargs)
        if 'error' not in data:
            if data:
                return 'insert ok'
            else:
                return '已经存在，将执行更新操作', 409
        else:
            return data


def get_model_type():
    """
    获取设备类型
    :return:
    """
    model_type = ['面板AP', '桌面二合一', '三合一', '四合一', '吸顶AP', 'AC路由网关', '光猫', '嗅探光猫', '嗅探2合1']
    oem_info = get_data_base('O_E_M_DB', 'id', 'oem_code', 'oem_name')
    return {'type': model_type, 'oem_info': oem_info}


def inset_into_dev_model(*args):
    """
    新增设备数据
    :param args:
    :return:
    """
    if len(args) != 7:
        return '参数错误'
    oem = get_data_base_filter('O_E_M_DB', id=int(args[0]))[0]
    log.debug(oem)
    if type(oem) == str:
        return '未找到oem数据'
    rdata = sp_api.adddev_model(type=args[3], dev_model=args[4], oem_model=args[6], old_model='',
                                oem_name=oem['oem_name'], comment=args[1], user=args[2])
    rapdata = ap_api.add_dev_model(cate_name=args[3], model_name=args[4], salscom=oem['oem_name'],
                                   oem_name=oem['oem_name'])
    log.debug(rdata)
    log.debug(rapdata)
    data = insert_into_data('D_M_DB', comment=args[1],
                     user=args[2],
                     type=args[3],
                     zy_model=args[4],
                     oem_id=args[5],
                     oem_name=oem['oem_name'],
                     oem_code=oem['oem_code'],
                     oem_model=args[6])
    log.debug(data)
    return data

def insert_into_super_task(*args):
    """
    设备链接器配置信息存储
    :param args:
    :return:
    """
    if len(args) != 5:
        return 'param error'
    git_code(args[0])
    data = cp_file(args[2])
    if not data:
        return '文件复制失败'
    if data:
        data = create_data('S_T_V_DB',
                            user=args[4],
                            supertack_version=args[0],
                            comment=args[3],
                            dev_model=args[1],
                            md5=data[1],
                            supertack_file=data[2],
                            supertack_type=args[2]
                                )
        return data
    return '目录名无效'


def inset_into_super_config(*args):
    """
        上传 superD config 文件数据
        :return:
        """
    if len(args) != 6:
        return '参数错误'
    day_time = time.strftime('%Y/%m/%d/%H/%M/%S', time.localtime(time.time()))
    save_path = './upload/' + day_time
    if 'Linux' in platform.system():
        save_path = out_base_path + out_super_conf_data + day_time

    save_path_name = save_path + '/' + args[0].name
    mkdir(save_path, False)
    # 创建文件
    with open(save_path_name, 'wb') as new_file:
        for chunk in args[0].chunks():
            new_file.write(chunk)
    # 创建文件后，计算文件md5
    md5 = get_md5_big(save_path_name)
    log.debug('file_path:{},md5:{}'.format(save_path_name, md5))

    data = insert_into_data('S_D_C_F_DB',
                            superdcf_version=args[1],
                            dev_model=args[2],
                            comment=args[4],
                            type=args[3],
                            user=args[5],
                            md5=md5,
                            superdcf_file=save_path_name)
    return data


def get_map_dev_model(dev_model):
    """
    由于cbild.sh 文件写的是非标准型号，故需要做个映射进行适配,如果不需要映射则原样输出
    :return:
    """
    data = get_data_base_filter('M_D_M_DB', dev_model=dev_model)
    if type(data) is str:
        log.warning('未找到该型号【{}】的map关系,将使用原始型号进行构建'.format(dev_model))
        map_dev_model = dev_model
    else:
        if len(data) > 0:
            map_dev_model = data[0]['map_dev_model']
            log.debug('dev_model:{}  map_dev_model:{}'.format(dev_model, map_dev_model))
        else:
            log.warning('未找到该型号【{}】的map关系,将使用原始型号进行构建'.format(dev_model))
            map_dev_model = dev_model
    return map_dev_model


def get_build_log(**kwargs):
    """
    获取构建日志
    :return:
    """
    if kwargs:
        data = get_data_base_filter('B_T_L_DB', **kwargs)
    else:
        data = get_data_base_filter('B_T_L_DB')
    if type(data) is str:
        data = []
    return data


def insert_into_build_log(**kwargs):
    """
    构建日志数据存储
    :return:
    """
    data = insert_into_data('B_T_L_DB', **kwargs)
    if type(data) is str:
        log.warning(f'构建数据日志存入失败，原因如下： {data}')
    return data


def insert_into_super_data(**kwargs):
    """
    构建superD版本数据存储
    :return:
    """
    data = insert_into_data('S_D_DB', **kwargs)
    if type(data) is str:
        log.warning(f'构建数据日志存入失败，原因如下： {data}')
    return data


def insert_into_super_api_load(**kwargs):
    """
    构建sapiload 版本数据存储
    :param kwargs:
    :return:
    """
    data = insert_into_data('S_A_L_DB', **kwargs)
    if type(data) is str:
        log.warning(f'sapiload 构建版本数据存储失败，原因：{data}')

    return data


def insert_into_reverse_proxy(**kwargs):
    """
    构建反向代理包存储
    :param kwargs:
    :return:
    """
    data = insert_into_data('R_P_DB', **kwargs)
    if type(data) is str:
        log.warning(f'反向代理 构建版本数据存储失败，原因：{data}')

    return data


def get_super_d_all(branch='', build_type=None):
    """
    获取superD插件信息
    :param branch:
    :param build_type:
    :return:
    """
    if not branch:
        branch = config_branch['superd_branch']
    git = GitProcess(superd_project_path)
    git._init_directoy(branch)
    if build_type is 'test':
        data = get_data_base_filter('S_D_DB', build_type=build_type)
        if type(data) is str:
            return []
        return data[:100]
    else:
        data = exclude_data_base('S_D_DB', build_type='test')
        if type(data) is str:
            return []
        return data[:100]


def get_build_package_info(ids=''):
    """
    查询结果包
    :param ids:
    :return:
    """
    if ids:
        data = get_data_base_filter('B_P_R_DB', id=ids)
    else:
        data = get_data_base('B_P_R_DB')
    if type(data) is str:
        log.warning(f'pg包数据查询失败，原因{data}')
        return {}
    return data


def insert_into_super_data_package(**kwargs):
    """
    插件打包数据存储
    :param kwargs:
    :return:
    """
    if kwargs:
        data = insert_into_data('B_P_R_DB', **kwargs)
        if type(data) is str:
            log.warning(f'构建包存储信息失败，原因：{data}')
    else:
        return '参数错误！'
    return data


def insert_into_super_api_loader_package(**kwargs):
    """
    插件打包数据存储
    :param kwargs:
    :return:
    """
    if kwargs:
        data = insert_into_data('S_A_L_P_DB', **kwargs)
        if type(data) is str:
            log.warning(f'构建包存储信息失败，原因：{data}')
    else:
        return '参数错误！'
    return data


def get_info_super_api_loader_package(**kwargs):
    """
    sapiloader 打包数据存储
    :param kwargs:
    :return:
    """
    if kwargs:
        data = get_data_base_filter('S_A_L_P_DB', **kwargs)
        if type(data) is str:
            log.warning(f'查询sapiloader 包失败，原因：{data}')
            return None
    else:
        data = get_data_base_filter('S_A_L_P_DB')
        if type(data) is str:
            log.warning(f'查询sapiloader 包失败，原因：{data}')
            return None

    return data


def get_info_super_data_package(**kwargs):
    """
    获取插件打包信息
    :param kwargs:
    :return:
    """
    if kwargs:
        data = get_data_base_filter('B_P_R_DB', **kwargs)
        if type(data) is str:
            log.warning(f'插件打包信息获取失败，原因：{data}')
        else:
            return data
    else:
        data = get_data_base_filter('B_P_R_DB')
        if type(data) is str:
            log.warning(f'插件打包信息获取失败，原因：{data}')
        else:
            return data

def get_info_online_log(**kwargs):
    """
    获取上线日志
    :param kwargs:
    :return:
    """
    if kwargs:
        data = get_data_base_filter('R_O_P_L_DB', **kwargs)
        if type(data) is str:
            log.warning(f'插件打包信息获取失败，原因：{data}')
        else:
            return data
    else:
        data = get_data_base_filter('R_O_P_L_DB')
        if type(data) is str:
            log.warning(f'插件打包信息获取失败，原因：{data}')
        else:
            return data


def insert_into_online_log(**kwargs):
    """
    存储上线日志数据
    :param kwargs:
    :return:
    """
    if kwargs:
        data = insert_into_data('R_O_P_L_DB', **kwargs)
        if type(data) is str:
            log.warning(f'发布上线数据失败，原因：{data}')
    else:
        return '参数错误！'
    return data



def build(map_dev_model,dev_model,user,tag,reason, types):
    """
     map_dev_model 是映射的型号名称，即cbuild文件中的型号名称，
     这个型号名称有的是型号名称本身，有的是编译链简称，
     有的是型号名称小写

    构建数据包，并存储构建日志
    :param map_dev_model:
    :param dev_model:
    :param user:
    :param tag:
    :param reason:
    :param type:
    :return:
    """

    status = 400
    log.debug(map_dev_model)
    try:
        cmd = './cbuild.sh {} 2>&1'.format(map_dev_model)
        if 'superd' in types:
            build_shell_path = superd_build_shell_path
        else:
            build_shell_path = sapiloader_c_build_shell_path

        log.debug('构建{}:{}，路径：{}'.format(types, cmd, build_shell_path))

        if 'superd' in types:
            plug_name = 'superd'
            str_sign = 'All ok! Output:{}'.format(plug_name)
        else:
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
            log.debug('{}-{}-构建结果：{}'.format(types,dev_model,status))
        except Exception as e:
            log.error(e)
        finally:
            insert_into_build_log(time_stamp=time_stamp(),
                                  dev_model=dev_model,
                                  user=str(user),
                                  build_result=build_data,
                                  build_tag=tag,
                                  build_reason=reason,
                                  build_status=status,
                                  type=types)
    except Exception as e:
        log.error(e)
    return status


def record_plug_info(types, dev_model, durl, user,  tag, reason,
                     save_path_name, build_result, build_status, build_type):
    """
    构建信息存储

    :param types:
    :param dev_model:
    :param durl:
    :param user:
    :param tag:
    :param reason:
    :param save_path_name:
    :param build_result:
    :param build_status:
    :param build_type:
    :return:
    """
    log.debug('开始记录{}_info'.format(types))
    try:
        md5 = get_md5_big(save_path_name)
        if 'superd' in types:
            insert_into_super_data(
                                    time_stamp=time_stamp(),
                                    download_url=durl,
                                    user=str(user),
                                    superd_file=save_path_name,
                                    md5=md5,
                                    build_reason=str(reason),
                                    build_result=build_result,
                                    build_status=build_status,
                                    dev_model=dev_model,
                                    superd_version=tag,
                                    build_type=build_type)
        elif 'sapiloader' in types:
            insert_into_super_api_load(download_url=durl,
                                       user=str(user),
                                       sapiloaderC_file=save_path_name,
                                       md5=md5,
                                       build_reason=str(reason),
                                       build_result=build_result,
                                       build_status=build_status,
                                       dev_model=dev_model,
                                       sapiloaderC_version=tag)
        elif 'proxy' in types:
            insert_into_reverse_proxy(download_url=durl,
                                      user=str(user),
                                      proxy_file=save_path_name,
                                      md5=md5,
                                      build_reason=str(reason),
                                      build_result=build_result,
                                      build_status=build_status,
                                      dev_model=dev_model,
                                      proxy_version=tag)
        else:
            log.error('type：{},未找到该类型')
        log.debug('构建{}信息记录完成'.format(types))

    except Exception as e:
        log.error(e)


def get_build_is_complate(dev_model,tag,reason,user,types):
    """
    查看指定目录中是否有type文件
    :return:
    """
    build_time_stamp = 0
    now_time_stamp = time_stamp()

    try:
        data = get_build_log(type=types,
                             dev_model=dev_model,
                             build_tag=tag,
                             build_reason=reason,
                             user=user)
        log.debug('build_log:{}'.format(data))
        if type(data) is not str and len(data) > 0:
            data = data[0]
            build_status=int(data['build_status'])
            build_time_stamp=int(data['time_stamp'])
            res = abs(now_time_stamp-build_time_stamp)
            if res>60:
                build_status=0
                log.debug('时间差:[{}]大于60s'.format(res))
        else:
            build_status = 0
    except Exception as e:
        log.warning(e)
        build_status=0

    log.debug(f'查找,操作人:{user}，'
              f'类型:{types},'
              f'dev_model:{dev_model},'
              f'tag:{tag},'
              f'reason:{reason},'
              f'now_time_stamp:{now_time_stamp},'
              f'build_time_stamp:{build_time_stamp},'
              f'是否构建完成：{build_status}')
    return build_status


def mv_plug(dev_model, user, tag, reason, types, build_save_path,
            save_path, build_type=None, map_dev_model=''):
    """
    找到该版本构建成功的superd文件,并移动到指定路径下
    :param dev_model:
    :return:
    """
    save_plug_name = ""
    try:
        if 'superd' in types:
            plug_name = 'superd'
        elif 'sapiloader' in types:
            plug_name = 'sapiloader'
        elif 'proxy' in types:
            "rproxy_mr820.tar.gz"
            plug_name = 'rproxy_{}.tar.gz'.format(map_dev_model)
            save_plug_name = 'rproxy_{}.tar.gz'.format(map_dev_model.replace('-', '_'))
        else:
            log.warning(f'根据typees 参数：{types}, 未找到指定的文件名称。中断当前操作，返回失败结果-1')
            return -1

        log.debug('指定型号{}:{}'.format(dev_model,types))
        # 这是去构建后指定目录中查找构建完毕的文件
        # file_path = build_save_path + map_dev_model + '/' + plug_name
        # 直接在当前构建路径获取构建结果
        file_path = build_save_path + plug_name

        log.debug('{}生成路径：{}'.format(types,file_path))
        build_status = 0
        build_result = '未找到:{}'.format(plug_name)
        if save_plug_name:
            save_path_name = save_path + save_plug_name
        else:
            save_path_name = save_path + plug_name
        mkdir(save_path)
        if file_is_have(file_path):
            cmd = 'mv {} {}'.format(file_path, save_path_name)
            log.debug('移动{}到指定路径,from:{},target:{}'.format(plug_name,file_path, save_path))
            executionShell(cmd)
            build_result = '失败'
            build_status = -1
            if file_is_have(save_path_name):
                build_result = '成功'
                build_status = 1
        log.debug('{}移动{}:{}'.format(plug_name,build_result, build_status))
        if build_status == 1:
            durl = plug_domain+save_path_name.replace(out_base_path, '')
            record_plug_info(types,dev_model, durl,user, tag, reason,save_path_name,build_result,build_status,build_type)
        return build_status
    except Exception as e:
        log.error(e)


def get_dpi_config_all(**kwargs):
    """
    D_M_DB   表数据表
    S_D_C_F_DB   表数据表
    Device Model Data Base
    Deep Packet Inspection Config Version Data Base

    :return:
    """
    if kwargs:
        dpi_config = get_data_base_filter('dpiConfigVersion', **kwargs)
    else:
        dpi_config = get_data_base_filter('dpiConfigVersion')
    if type(dpi_config) is str:
        return None
    return dpi_config


def get_proxy_version_info(**kwargs):
    """
    获取反向代理信息  proxyVersion
    :param kwargs:
    :return:
    """
    if kwargs:
        proxy_ver = get_data_base_filter('R_P_DB', **kwargs)
    else:
        proxy_ver = get_data_base_filter('R_P_DB')

    if type(proxy_ver) is str:
        return None
    return proxy_ver


def get_pack_default_configure(**kwargs):
    """
    获取默认打包配置数据
    :param kwargs:
    :return:
    """
    if kwargs:
        proxy_ver = get_data_base_filter('PackDefaultConfigure', **kwargs)
    else:
        proxy_ver = get_data_base_filter('PackDefaultConfigure')

    if type(proxy_ver) is str:
        return None
    return proxy_ver


def get_tag_info(**kwargs):
    """
    获取代码版本
    :return:
    """
    if kwargs:
        data = get_data_base_filter('S_O_T_DB', **kwargs)
    else:
        data = get_data_base_filter('S_O_T_DB')

    if type(data) is str:
        return None
    return data
