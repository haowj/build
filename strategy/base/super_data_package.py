#!/usr/bin/env python3
# -*- coding: utf8 -*-
__author__ = 'wjhao'
import logging
from strategy.base.op_val import package_contains_path_dict, get_build_is_complate, get_data_base_filter, \
    insert_into_super_data_package, get_tag_info, get_pack_default_configure, insert_into_super_task
from strategy.conf.path import out_build_tmp_path, plug_domain
from strategy.base.tools import get_now_time, time, executionShell, chmod_file, cps, get_md5_big, compression, is_have_file
from strategy.base.super_data_build import toBuild
log = logging.getLogger(__name__)


class PackageDB:
    def __init__(self,
                 user,
                 dev_model,
                 adapter,
                 superd_version,
                 connector,
                 superd_conf,
                 dpi_conf,
                 pack_type,
                 docking_solution,
                 default_conf):
        """
        获取打包数据信息
        :param dev_model: 设备型号
        :param adapter: 适配器类型
        :param superd_version: superD 版本信息
        :param connector: 连接器版本信息
        :param superd_conf: superD 配置文件信息
        :param dpi_conf: DPI 配置文件ID
        """
        self.user = user
        self.model = dev_model
        self.super_data_version = superd_version
        self.adapter = adapter
        self.dpi_conf = dpi_conf
        self.connector = connector
        self.super_data_conf = superd_conf
        self.pack_type = pack_type
        self.docking_solution = docking_solution
        self.default_conf = default_conf
        self.super_data_conf_path = None
        self.dpi_conf_path = None
        self.connector_path = None
        self.super_data_path = None
        self.super_data_conf_ver = None
        self.dpi_conf_ver = None
        self.connector_ver = None
        self.super_data_tag = None
        self.connector_data_tag = None
        if self.adapter:
            self.package_contains_path = package_contains_path_dict[self.adapter]
        if not superd_version:
            tag_data = get_tag_info(status=1)
            if tag_data:
                for t_i in tag_data:
                    if 'superd' in t_i['project_name']:
                        self.super_data_tag = t_i['tag']
                        break
                for t_i in tag_data:
                    if 'connector' in t_i['project_name']:
                        self.connector_data_tag = t_i['tag']
                        break

    @property
    def pack_default_conf(self):
        if int(self.default_conf) == 0:
            data = get_pack_default_configure(dev_model=self.model)
            if not data:
                data = get_pack_default_configure(dev_model='fitall')
            if not data:
                return '没有找到打包默认配置'

            self.adapter = data[0]['pack_type']
            self.docking_solution = data[0]['docking_solution']
            self.pack_type = data[0]['compress_mode']
            self.package_contains_path = package_contains_path_dict[self.adapter]

    @property
    def super_data_conf_info(self):
        """
        根据型号获取super data config 信息
        :return:
        """
        if self.super_data_conf:
            data = get_data_base_filter('S_D_C_F_DB', id=int(self.super_data_conf))
        else:
            tall_data = get_data_base_filter('S_D_C_F_DB', dev_model='fitall', type=self.adapter)
            model_data = get_data_base_filter('S_D_C_F_DB', dev_model=self.model, type=self.adapter)
            if model_data:
                data = model_data
            else:
                data = tall_data

        if type(data) is str:
            log.warning(f'superD conf info 数据查询失败，参数dev_model{self.model}、'
                        f'superdcf_version={self.super_data_conf}、Error:{data}')
            return f'superD conf info 数据查询失败，参数dev_model{self.model}、superdcf_version={self.super_data_conf}、Error:{data}'
        elif len(data) > 0:
            self.super_data_conf_path = data[0]['superdcf_file']
            self.super_data_conf_ver = data[0]['superdcf_version']
        else:
            return 'superD config []'

    @property
    def dpi_conf_info(self):
        """
        根据版本号获取 dpi config 信息
        :return:
        """
        if self.dpi_conf:
            data = get_data_base_filter('dpiConfigVersion', id=int(self.dpi_conf))
        else:
            data = get_data_base_filter('dpiConfigVersion', dev_model_id='88888888')

        if type(data) is str:
            log.warning(f'dpi conf info 数据查询失败，参数id={self.dpi_conf}、Error:{data}')
            return f'dpi conf info 数据查询失败，参数id={self.dpi_conf}、Error:{data}'
        elif len(data) > 0:
            self.dpi_conf_path = data[0]['zdpi_sig_file']
            self.dpi_conf_ver = data[0]['zdpi_sig_version']
        else:
            return 'DPI config 数据 []'

    @property
    def connector_info(self):
        """
        获取连接器信息，根据型号，适配器类型，版本号
        如果根据版本号找到这直接使用数据， 如果未找到这创建数据。并返回对应路径
        fitall 全部类型
        :return:
        """
        if self.connector:
            tag = self.connector
        else:
            tag = self.connector_data_tag
        if not tag:
            log.warning(f'插件版本号未找到 tag:{tag}')
            return f'没有找到连接器版本号！tag:{tag}'
        data = insert_into_super_task(tag, self.model, self.adapter, '打包自动构建', self.user)
        if type(data) is str:
            return data
        self.connector_path = data.supertack_file
        self.connector_ver = data.supertack_version

    @property
    def super_data_info(self):
        """
        build_type = release
        build_result = 成功
        :return:
        """
        if self.super_data_version:
            tag = self.super_data_version
        else:
            tag = self.super_data_tag

        if not tag:
            log.warning(f'插件版本号未找到 tag:{tag}')
            return f'插件版本号未找到 tag:{tag}'

        date_time = get_now_time()
        reason = f'时间: {date_time} 打包自动构建superD插件 型号：{self.model} 版本：tag:{tag}'
        toBuild(self.model, tag, reason, self.user)
        data = 0
        for i in range(60):
            time.sleep(1)
            data = get_build_is_complate(self.model, tag, reason, self.user, 'superd')
            if type(data) is str:
                log.warning(f'super D 构建结果查询失败，原因：{data}')
                return f'super D 构建结果查询失败，原因：{data}'
            if data == 200:
                break

        if data == 200:
            data = get_data_base_filter('S_D_DB', dev_model=self.model,
                                        superd_version=tag,
                                        build_type='release',
                                        build_result='成功',
                                        build_reason=reason)
            if type(data) is str:
                log.warning(f'super data info 数据查询失败，参数dev_model={self.model}、super_version={tag}'
                            f'build_type=release,build_reason={reason} Error:{data}')
                return 'super data info 数据查询失败，参数dev_model={self.model}、super_version={tag} build_type=release,build_reason={reason} Error:{data}'
            elif len(data) > 0:
                self.super_data_path = data[0]['superd_file']
                self.super_data_version = data[0]['superd_version']
        else:
            log.warning(f'super D 构建失败 代码：{data}')
            return f'super D 构建失败 代码：{data}'

    @property
    def package_build(self):
        """
        根据信息进行打包，并存储数据信息
        :return:
        """
        if self.pack_default_conf:
            return self.pack_default_conf
        if self.super_data_conf_info:
            return self.super_data_conf_info
        if self.dpi_conf_info:
            return self.dpi_conf_info
        if self.connector_info:
            return self.connector_info
        if self.super_data_info:
            return self.super_data_info

        work_path = out_build_tmp_path + self.user + '/'
        if is_have_file(work_path):
            log.debug('删除工作目录')
            executionShell('sudo rm -rf *', work_path)
        ex_path = work_path + self.package_contains_path
        pack_content = f'superd_path:{self.super_data_path},' \
                       f'superdcf_path:{self.super_data_conf_path},' \
                       f'connector:{self.connector_path},' \
                       f'package_contains_path:{self.package_contains_path}, ' \
                       f'dpi_config_path:{self.dpi_conf_path}'

        # pack_data = get_info_super_data_package(zdpi_sig_version=self.dpi_conf_ver,
        #                             pack_content=pack_content,
        #                             dev_model = self.model,
        #                             superd_version = self.super_data_version,
        #                             connector_version = self.connector_ver,
        #                             superdcf_version = self.super_data_conf_ver,
        #                             pack_type = self.pack_type,
        #                             docking_solution = self.docking_solution,
        #                             package_contains_path = self.package_contains_path,
        #                             package_contains_path_type = self.adapter)
        # if pack_data:
        #     if type(pack_data) is str:
        #         log.warning(f'构建插件包数据查询失败， 原因：{pack_data}')
        #     else:
        #         return '已经存在包,请勿重复构建！'

        for i in [self.connector_path, self.dpi_conf_path, self.super_data_path, self.super_data_conf_path]:
            cfres = chmod_file(i)
            cpres = cps(i, ex_path)
            if not cfres and not cpres:
                log.error('授权结果：{}，复制结果：{}'.format(cfres, cpres))
                return f'{i}文件复制或授权失败'
        else:
            is_ok, tarname, package_path, package_save_path_name = compression(self.pack_type,
                                                                               self.model,
                                                                               self.super_data_version,
                                                                               self.package_contains_path,
                                                                               'superd',
                                                                               work_path)
            if is_ok:
                md5 = get_md5_big(package_save_path_name)
                obj, created = insert_into_super_data_package(download_url=plug_domain + package_path + tarname,
                                                              pack_name=tarname,
                                                              md5=md5,
                                                              user=self.user,
                                                              zdpi_sig_version=self.dpi_conf_ver,
                                                              pack_content=pack_content,
                                                              package=package_save_path_name,
                                                              dev_model=self.model,
                                                              superd_version=self.super_data_version,
                                                              connector_version=self.connector_ver,
                                                              superdcf_version=self.super_data_conf_ver,
                                                              pack_type=self.pack_type,
                                                              docking_solution=self.docking_solution,
                                                              package_contains_path=self.package_contains_path,
                                                              package_contains_path_type=self.adapter)
                log.debug('pack_db-obj:{},create:{}'.format(obj, created))
                if created is not True:
                    return '已经存在包信息，更新'
            else:
                return '构建压缩文件失败'

