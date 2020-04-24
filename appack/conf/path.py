# coding:utf-8
import platform

__author__ = 'xcma'
import time
from appack.conf.config import *

plug_domain = 'http://plug.superhcloud.com/'
release_domain = 'http://ap.superhcloud.com/'
"""
C版本PG包上线接口
ap.superhcloud.com/apmodel/loader-plug?t={$t}&url={$url}&sign={$sign}&modelname={$modelname}&filename={$filename}&name={$name}&run_cmd={$run_cmd}&unpack_cmd={$unpack_cmd}&save_plug_name={$save_plug_name}&
monitor_time={$monitor_time}&reconnect_time={$reconnect_time}&rom_version={$rom_version}&save_target_path={$save_target_path}

shell版PG包上线接口
ap.superhcloud.com/apmodel/plugin?

"""
base_path = '/home/build/'
workplace = 'workplace/'

superd_project_name = 'device_side_2.0/'
superd_output = 'src/output/'
superd_shell_path = 'src/super2d/'
connector = 'connector/'
# package_contains_path = 'sapi/run/'    # C加载器打包需要的路径
# package_contains_path_shell = 'run/'  # shell版本加载器打包需要的路径

sapiloader_c_project_name='sapi_bootstrap/'
sapiloader_shell_path = 'src/sapi_loader/'
sapiloader_c_output = 'src/output/'
sapiloader_c_project_path = base_path+sapiloader_c_project_name
sapiloader_c_build_shell_path = sapiloader_c_project_path+sapiloader_shell_path
sapiloader_c_build_save_path = sapiloader_c_project_path+sapiloader_c_output
sapiloader_c_build_shell_path_name = sapiloader_c_build_shell_path+'cbuild.sh'

superd_project_path = base_path+superd_project_name
# /home/build/device_side_2.0/src/super2d
superd_build_shell_path = superd_project_path+superd_shell_path
workplace_path = base_path+workplace
superd_project_path = base_path+superd_project_name
superd_build_save_path = superd_project_path+superd_output
superd_build_shell_path_name = superd_build_shell_path+'cbuild.sh'

connector_project_path = base_path+connector
supertack_file_path_name = connector_project_path+'supertack/supertack'
superctl_file_path_name = connector_project_path+'superctl/superctl'

proxy_client_build_shell_path="{}reverse_proxy".format(base_path)
proxy_client_project_path="{}reverse_proxy".format(base_path)
# 构建完成后，生成存储目录
proxy_client_build_save_path="{}reverse_proxy/install/".format(base_path)

def get_path_day_time():
    day_time = time.strftime('%Y/%m/%d/%H/%M/%S/', time.localtime(time.time()))
    return day_time

if 'Linux' not in platform.system():
    base_path = './'
    workplace = 'workplace/'
    upload = 'upload/{}'.format(get_path_day_time())
    code_path = '/Users/xuechao.ma/work/'
    superd_project_path = '/Users/xuechao.ma/work/device_side_2.0/'
    superd_build_save_path = '/Users/xuechao.ma/work/device_side_2/src/output/'
    superd_build_shell_path = '{}src/super2d/'.format(superd_project_path)
    workplace_path = base_path+workplace

    proxy_client_build_shell_path = "{}reverse_proxy".format(code_path)

    sapiloader_c_project_name = 'sapi_bootstrap/'
    sapiloader_c_project_path = '/Users/xuechao.ma/work/sapi_bootstrap/'
    sapiloader_c_build_shell_path = sapiloader_c_project_path+sapiloader_shell_path

    connector_project_path = code_path+connector



superd_build_test_branch_list = ['master','zjsuperd','test']  # 构建测试插件时使用
docking_solution = ['2.5', '2.0', '1.5', '1.0']
c_sapiloader = 'c_sapiloader'
shell_sapiloader = 'shell_sapiloader'

package_contains_path_dict = {
    c_sapiloader:'sapi/run',
    shell_sapiloader:'run'
}

advertising_type = ['全局','一级','二级']
advertising_location = ['全局','构建','打包']
superdcf_type = [c_sapiloader,shell_sapiloader]
connector_type = [c_sapiloader,shell_sapiloader]
save_path = {
    'master':'/sapi/master',
    'slave':'/sapi/slave'
}
package_type = {
    c_sapiloader:['lzma','gzip'],
    shell_sapiloader:['lzma','gzip'],

}



# save file path
base_save_file_path = base_path+'upload/'

def getProjeck_path(sw):
    if sw == 'superd':
        path = superd_project_path
        branch = config_branch['superd_branch']
    elif sw == 'sapiloader':
        path = sapiloader_c_project_path
        branch = config_branch['sapiloader_branch']
    elif sw == 'connector':
        path = connector_project_path
        branch = config_branch['connector_branch']
    else:
        path = 'not found'
        branch = config_branch['superd_branch']
    return path,branch