#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
import logging
import hashlib
from strategy.base.op_val import get_build_package_info, insert_into_online_log, get_info_super_api_loader_package
from strategy.conf.path import release_domain
from strategy.base.tools import get_now_time, time_stamp
from strategy.control.ap_api import ap_api
from strategy.control.support_api import sp_api


log = logging.getLogger(__name__)

class Online:
    def __init__(self):
        self.data = None
        self.shell_url = None

    def get_shell_url(self, downurl, dev_model, file_name, superd_version, router, comment_in, md5):
        """
        针对shell版本加载器的PG包上线操作
        :param downurl:
        :param dev_model:
        :param file_name:
        :param superd_version:
        :param router:
        :param comment_in:
        :param md5:
        :return:
        """
        md5_stamp = str(md5) + str(time_stamp()) + 'pythonapi'
        sign = hashlib.md5(md5_stamp.encode('utf-8')).hexdigest()
        comment='build push \n'
        comment += comment_in
        self.shell_url = f"{release_domain}apmodel/plugin?url={downurl}" \
                         f"&modelname={dev_model}&filename={file_name}" \
                         f"&version=ZJPG-{superd_version}&router={router}" \
                         f"&comment={comment}&sign={sign}&t={str(time_stamp())}"

    def release_shell(self,downurl,dev_model,file_name,superd_version,router,comment_in,md5):
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
        self.data = ap_api.release_shell_pg(para)

    def release(self, durl, modelname, md5, salscom, name, filename, **kwargs):
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
        log.debug(f"上线接口提交数据：{para_dict}")
        self.data = ap_api.release_pg(para_dict)

    def do_release(self, ids, user, **kwargs):
        try:
            code = 0
            err = ''
            packInfo = get_build_package_info(ids)[0]
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
                modelname = str(modelname).replace('CMCC-', '')
            else:
                salscom = ''
            if 'c_sapiloader' == package_contains_path_type:
                name = '{}[id]_{}_{}[superd]_{}[connector]_{}[conf]_{}'.format(ids, modelname,
                                                                               superd_version,
                                                                               connector_version,
                                                                               superdcf_version,
                                                                               get_now_time())

                self.release(durl, modelname, md5, salscom, name, filename, **kwargs)
                cmd_content = 'run_cmd:{},unpack_cmd:{},' \
                              'save_plug_name={},' \
                              'monitor_time={},reconnect_time={},' \
                              'rom_version={},save_target_path={}'.format(kwargs['run_cmd'],
                                                                          kwargs['unpack_cmd'],
                                                                          filename,
                                                                          kwargs['monitor_time'],
                                                                          kwargs['reconnect_time'],
                                                                          kwargs['rom_version'],
                                                                          kwargs['save_target_path'])

            elif 'shell_sapiloader' == package_contains_path_type:
                self.get_shell_url(durl, modelname, filename, superd_version, 25, comment, md5)
                name = modelname
                cmd_content = self.shell_url
                self.release_shell(durl, modelname, filename, superd_version, 25, comment, md5)
            else:
                cmd_content = ''
                name = modelname
                code = 500
                err = '包内路径类型错误'
                self.data['err'] = err

            if code != 500:
                code = 400
                err = self.data['err']
                if self.data['succ']:
                    code = 200
                    log.debug(f'上线配置名称{name}')
                    args = insert_into_online_log(dev_model=modelname,
                                                  user=user,
                                                  plug_title_name=name,
                                                  plug_name=filename,
                                                  plug_md5=md5,
                                                  version=superd_version,
                                                  cmd_content=cmd_content,
                                                  comment=comment,
                                                  rtype='pg')
                    if type(args) is str:
                        err = args
                        code = 400
            return {'code': code, 'err': err}
        except Exception as e:
            log.error(e)
            return {'code': 500, 'err': e}

    def release_super_api_loader(self, ids, area, sor, user):
        log.debug('加载器上线开始')
        data = get_info_super_api_loader_package(id=ids)
        if not data and type(data) is str:
            log.warning(f'未找到上线数据包  加载器查询参数 {ids}')
            return {'code': 400, 'err': '未找到上线数据包'}
        else:
            data = data[0]
        dev_model = data['dev_model']
        pack_name = data['pack_name']
        md5 = data['md5']
        version = data['version']
        res = insert_into_online_log(dev_model=dev_model,
                                     user=user,
                                     plug_title_name='',
                                     plug_name=pack_name,
                                     plug_md5=md5,
                                     version=version,
                                     cmd_content='',
                                     comment=sor,
                                     rtype='sapiloader')
        if type(res) is str:
            log.warning(f'{dev_model}, {pack_name}上线日志数据插入失败，原因{res}')
            return {'code': 400, 'err': res}

        res = sp_api.addNewSVersionInfo(area=area,
                                      dev_model=dev_model,
                                      status='1.准备中',
                                      docking_solution='2.5',
                                      vsapiloader=version,
                                      sapiloader_type='c版本',
                                      start_time=get_now_time(1))

        log.debug('加载器上线结果：{}'.format(res))
        return res