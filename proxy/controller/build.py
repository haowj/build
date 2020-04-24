# coding:utf-8
import time

__author__ = 'xcma'
from appack.controller.version_control import base
from appack.conf.path import proxy_client_project_path,proxy_client_build_save_path,get_path_day_time,proxy_client_build_shell_path
from proxy.models import proxyVersion
from strategy.models import R_P_DB
from appack.helper.misc import monitorLog,executionShell
import logging
import threading

log = logging.getLogger(__name__)
class proxy_build_class(base):

    def is_ok(self,dev_model):
        num = 0
        status = 400
        while True:
            log_name = '{}_out.log'.format(dev_model)
            str_sign = './ngrok'
            data = monitorLog('grep -w "{}" {}/{}'.format(str_sign, proxy_client_project_path, log_name), 10)
            if './ngrok' in str(data) and len(str(data))<8:
                status=200
                log.debug('判断是否构建成功添加：{}'.format('proxy_client'))
                log.debug('{}-构建结果：{}'.format( dev_model, status))
                break
            else:
                log.debug('proxy_client 未构建完成等待2s。。。【已等待：{}s】'.format(num*2))
                time.sleep(2)
                num += 1
            if num > 100:
                # 最长等待5分钟
                break
        return status

    def build(self, map_dev_model, dev_model, user, tag, reason, type):
        # map_dev_model 是映射的型号名称，即cbuild文件中的型号名称，这个型号名称有的是型号名称本身，有的是编译链简称，有的是型号名称小写
        status = 400
        try:
            cmd = './cbuild.sh {}>{}_out.log 2>&1'.format(map_dev_model, dev_model)
            build_shell_path = proxy_client_build_shell_path

            log.debug('构建{}:{}，路径：{}'.format(type, cmd, build_shell_path))
            build_data = executionShell(cmd, build_shell_path, 1)
            # status = self.is_ok(dev_model)
            # if not build_data:
            #     build_data ='400'
            self.record_build_log(dev_model, str(user), build_data, tag, reason, status, type)
        except Exception as e:
            log.error(e)
        return status

    def proxy_build(self,dev_model,user):
        """
        1.更新项目库代码
        2.构建
        3.移动构建完成的包
        4.记录 型号 反向代理包 下载地址
        :param dev_model:
        :param user:
        :return:
        """
        tag = '1.0'
        reason = 'auto'
        type ='proxy'
        target_package_path = 'upload/superd/{}'.format(get_path_day_time())
        self.init_project(proxy_client_project_path)
        map_dev_model = self.map_devmodel(dev_model)
        self.build(map_dev_model,dev_model,user,tag,reason,type)
        num = 1
        while True:
            status = self.mv_plug(dev_model,user, tag, reason,type,proxy_client_build_save_path,target_package_path,map_dev_model=map_dev_model)
            if status==1:
                break
            else:
                time.sleep(1)
                num+=1
            if num==200:
                break

    def dobuid(self,dev_model,user):
        t1 = threading.Thread(target=self.proxy_build, args=(dev_model, str(user)))
        t1.start()
        return 1

    def get_proxy(self, dev_model, user):
        type ='proxy'
        tag='1.0'
        reason='auto'
        return self.get_build_is_complate(dev_model, tag, reason, user, type)

    def get_dev_model_proxy(self,dev_model):
        log.debug('dev_model:{}'.format(dev_model))
        data = R_P_DB.objects.filter(dev_model=dev_model).values().order_by('-id').first()
        return data