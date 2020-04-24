#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
import logging
from strategy.control.git_tool import get_tag_list
from strategy.base.tools import  get_now_time, time, is_have_file, executionShell, get_md5_big, chmod_file, cps, compression
from strategy.base.op_val import get_super_api_loader_data, get_build_is_complate, get_data_base_filter, \
    insert_into_super_api_loader_package
from strategy.conf.path import plug_domain, out_build_tmp_path, out_super_api_loader
from strategy.base.super_api_build import SuperApi

log = logging.getLogger(__name__)

class SuperApiPackage:
    def __init__(self, dev_model, super_api_loader, user):
        self.model = dev_model
        self.superA = super_api_loader
        self.user = user
        self.super_api_path = None
        self.super_api_version = None
        self.reason = None

    @property
    def get_super_api_loader(self):
        if self.superA:
            tag = self.superA
        else:
            tag = get_tag_list('sapiloader')
            if len(tag) > 0:
                tag = tag[1]
            else:
                log.warning(f'加载器版本号未找到 tag:{tag}')
                return False
        data = get_super_api_loader_data(dev_model=self.model, sapiloaderC_version=tag)
        if type(data) is str:
            log.warning(f'加载器查询失败{data}')
            return False
        elif len(data) > 0:
            self.super_api_path = data[0]['sapiloaderC_file']
            self.super_api_version = data[0]['sapiloaderC_version']
            self.reason = data[0]['build_reason']
            return data[0]['sapiloaderC_file']
        else:
            date_time = get_now_time()
            self.reason = f'datetime{date_time} sapiloder Autoloading the latest version device model {self.model} tag:{tag}'
            slr = SuperApi()
            slr.to_build(self.model, tag, self.reason, self.user)
            data = 0
            for i in range(30):
                time.sleep(1)
                data = get_build_is_complate(self.model, tag, self.reason, self.user, 'sapiloader')
                if type(data) is str:
                    log.warning(f'super Api loader 构建结果查询失败，原因：{data}')
                    return False
                if data == 200:
                    break

            if data == 200:
                data = get_data_base_filter('S_A_L_DB', dev_model=self.model,
                                            sapiloaderC_version=tag,
                                            build_result='成功',
                                            build_reason=self.reason)
                if type(data) is str:
                    log.warning("sapiloadeer 数据查询失败，参数dev_model={},"
                                "super_version={}、build_reason={} Error:{}".format(self.model, tag, self.reason, data))

                    return False
                elif len(data) > 0:
                    self.super_api_path = data[0]['sapiloaderC_file']
                    self.super_api_version = data[0]['sapiloaderC_version']
                    return data[0]['sapiloaderC_file']
            else:
                log.warning(f'super Api Loader 构建失败 代码：{data}')
                return False

    @property
    def package_build(self):
        """
        根据信息进行打包，并存储数据信息
        :return:
        """
        if not self.get_super_api_loader:
            return 'super Api loader 获取失败，详情请分析日志'

        work_path = out_build_tmp_path + self.user + '/'
        if is_have_file(work_path):
            log.debug('删除工作目录')
            executionShell('sudo rm -rf *', work_path)
        ex_path = work_path + out_super_api_loader
        cfres = chmod_file(self.super_api_path)
        cpres = cps(self.super_api_path, ex_path)
        if not cfres and not cpres:
            log.error('授权结果：{}，复制结果：{}'.format(cfres, cpres))
            return f'{self.super_api_path}文件复制或授权失败'
        else:
            is_ok, tarname, package_path, package_save_path_name = compression('gzip',
                                                                               self.model,
                                                                               self.super_api_version,
                                                                               './',
                                                                               'sapiloader',
                                                                               ex_path)
            if is_ok:
                md5 = get_md5_big(package_save_path_name)
                obj, created = insert_into_super_api_loader_package(url=plug_domain + package_path + tarname,
                                                                    pack_name=tarname,
                                                                    md5=md5,
                                                                    user=self.user,
                                                                    pack_save_path=package_save_path_name,
                                                                    dev_model=self.model,
                                                                    version=self.super_api_version,
                                                                    reason=self.reason)


                log.debug('pack_db-obj:{},create:{}'.format(obj, created))
                if created is not True:
                    return '已经存在包信息，更新'
            else:
                return '构建压缩文件失败'
