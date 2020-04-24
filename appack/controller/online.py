# coding:utf-8
__author__ = 'xcma'

import hashlib
import os
import platform
import subprocess
import time
import requests
import logging
from appack import models
log = logging.getLogger(__name__)

class sendOnline:
    """
    版本控制。
    """
    def getDname(self,sw):
        '获取路径下文件夹名称'
        path = '.'
        if sw == 'ttools':
            path = '/home/zjzy/tools/ttools/'
        if sw == 'plug':
            path = '/home/zjzy/tools/plug/'
        if sw == 'plug_20_release':
            path = '/home/zjzy/tools/plug/20/release/'
        if sw == 'plug_20_rc':
            path = '/home/zjzy/tools/plug/20/rc/'
        if sw == 'plug_25_release':
            path = '/home/zjzy/tools/plug/25/release/'
        if sw == 'plug_25_rc':
            path = '/home/zjzy/tools/plug/25/rc/'
        if sw == 'plug_30_rc':
            path = '/home/zjzy/tools/plug/30/rc'
        if sw == 'plug_30_release':
            path = '/home/zjzy/tools/plug/30/release/'
        if sw == 'test_plug':
            path = '/home/zjzy/tools/test_plug/'
        if sw == 'test_ttools':
            path = '/home/zjzy/tools/test_ttools/'
        # path = '/Users/xuechao.ma/Downloads/work_path/test_plug/'
        dir_list = []
        for dir in os.listdir(path):
            if os.path.isdir(path+dir):
                dir_list.append(dir)
        # log.debug('dir:{}-path:{}'.format(dir_list,path))
        return dir_list,path

    def getFilename(self,path):
        '拿插件/测试工具名称'
        name_list = os.listdir(path)
        for file_name in name_list:
            if not os.path.isdir(path+file_name):
                # log.debug('name_list:{}-path:{},filename:{}'.format(name_list, path,file_name))
                return file_name

    def urlFindVersion(self,url):
        "从url中拿到版本号：http://test.plug.superhcloud.com/plug/C2DT-M362/sapipack_v2.0.620.tar.lzma"
        version = ''
        if '_' in url:
            versionF = url.split('_')[1]
            version = versionF[:versionF.find('tar')-1]
            return version
        return version

    def gettimedifference(self,bigdate,now):
        now-bigdate
    def getDownloadPath(self):
        host = 'http://test.plug.superhcloud.com/'
        ap_model = {}
        url_total = {}
        for upath in ['ttools','plug_20_rc','plug_20_release','plug_25_rc','plug_25_release','plug_30_release','plug_30_rc','test_plug','test_ttools']:
            dname_list,dpath = self.getDname(upath)
            url_dict = {}
            for name in dname_list:
                file_path = dpath + name
                if 'plug_' in upath :
                    if 'plug_20_release'==upath:
                        url = "{}plug/20/release/{}/{}".format(host, name, self.getFilename(file_path))
                    elif 'plug_20_rc'==upath:
                        url = "{}plug/20/rc/{}/{}".format(host, name, self.getFilename(file_path))
                    elif 'plug_25_release'==upath:
                        url = "{}plug/25/release/{}/{}".format(host, name, self.getFilename(file_path))
                    elif 'plug_25_rc'==upath:
                        url = "{}plug/25/rc/{}/{}".format(host, name, self.getFilename(file_path))
                    else:
                        url = "{}plug/{}/{}/{}".format(host, upath, name, self.getFilename(file_path))
                    build_log=models.build_log.objects.filter(ap_model=name).values('user','build_reason','build_tag','build_status','up_time').order_by('-id').first()
                    release_plug_log = models.release_plug_log.objects.filter(ap_model=name).values('version').order_by('-id').first()
                    release_ver='暂无'
                    if release_plug_log:
                        release_ver = release_plug_log['version']

                    user=build_reason=version=build_status=up_time=''
                    if build_log:
                        user = build_log['user']
                        build_reason = build_log['build_reason']
                        version = build_log['build_tag']
                        build_status = build_log['build_status']
                        up_time = build_log['up_time']
                        file_version = self.urlFindVersion(url)
                        # if version not in file_version :
                            # url = '构建中'
                            # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            # up_time_format = up_time.strftime("%Y-%m-%d %H:%M:%S")
                            # if not compare_time(up_time_format,now):
                            #     url = '构建失败，请重新构建。'
                    url_dict[name] = {'url': url, 'user': user, 'build_reason': build_reason,
                                      'version': version,'release_ver':release_ver, 'build_status': build_status, 'up_time': up_time}
                else:
                    url = "{}{}/{}/{}".format(host, upath, name, self.getFilename(file_path))
                    url_dict[name] = {'url': url}

            url_total[upath] = url_dict
            ap_model[upath]=dname_list

        data = {
            'url':url_total,
            'ap_model':ap_model

        }
        log.debug(data)
        return data

    def sendtoRose(self,downurl,sign,t,modelname,filename,user,comment,version,plug_md5):
        # murl = 'http://test.rose.superhcloud.com/apmodel/plugin'
        murl = 'http://ap.superhcloud.com/apmodel/plugin'
        if '2.5.' in version:
            router=25
        elif '2.0.' in version:
            router =20
        else:
            router=0

        if 'LCS-' in modelname:
            # 简单名字是为了跟线上版本保持一致，全名是为了入库，跟jenkins中job名称一致
            sign_modelname=modelname.replace('LCS-','')
        else:
            sign_modelname = ''
        param = {
            'url':downurl,
            'sign':sign,
            't':t,
            'modelname':sign_modelname,
            # 'salscom':salscom,
            'filename':filename,
            'comment':comment,
            'version':version,
            'router':router
        }
        log.debug('release_send_info:url={},param={}'.format(murl,param))
        s_data = ''
        try:
            resp = requests.request('GET', murl, params=param)
            log.debug('api_response:{}'.format(resp.text))
            try:
                data = resp.json()
                log.error('data_json:{}'.format(data))
            except:
                data = resp.text
                log.error('php api respone not json:{}'.format(data))
            data['status'] = 0
            if data['succ']:
                try:
                    s_data = models.release_plug_log.objects.filter(plug_name=filename, ap_model__contains=modelname,plug_md5=plug_md5)
                    log.debug('s_data={}'.format(s_data))
                except Exception as e :
                    log.error(e)
                if not s_data:
                    log.debug('not found ap_model creat')
                    models.release_plug_log.objects.create(ap_model=modelname, user=user, plug_name=filename,plug_md5=plug_md5,version=version,comment=comment)
                else:
                    up_time = s_data.get().up_time
                    # =2 标识重复操作，提醒已经上线过相同的插件包。
                    data['status'] = 2
                    data['err']='型号：{}，插件：{}，已经在【{}】操作过上线了,请勿重复操作！'.format(modelname,filename,str(up_time)[:19])
            else:
                data['status'] = 1
        except:
            data = {
                'status':400,
                'err':'server error'
            }
        log.debug(data)
        return data

    def release_plug(self,ap_model,user,plug_url,comment,version):
        log.debug('ap_model:{},user:{},plug_url:{},comment:{},version:{}'.format(ap_model,user,plug_url,comment,version))
        if 'LCS-' in ap_model:
            plug_path = '/home/zjzy/tools/plug/25/release/{}/'.format(ap_model)
        else:
            plug_path = '/home/zjzy/tools/plug/{}/'.format(ap_model)
        # plug_path = '/Users/xuechao.ma/code/autotest/sts_webserver/'
        # md2 = "(b'4f7ff5736286604c44b2b52aa5203033  /home/zjzy/tools/plug/RG020ET-CA/sapipack_v1.0.16.tar.lzma\n', b'')"
        file_name = self.getFilename(plug_path)
        file_path_name = '{}{}'.format(plug_path,file_name)
        # url = '{}plug/{}/{}'.format(host,ap_model,file_name)
        if platform.system()=='Linux':
            cmd = 'md5sum {}'.format(file_path_name)
        else:
            cmd = 'md5 {}'.format(file_path_name)
        s = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        out = s.communicate()
        # log.debug('md5num:{}'.format(out))
        stamp = int(time.time())
        md5_s = str(out[0]).split('/')[0].replace("'",'').strip()[1:]
        # log.debug(md5_s)
        md5_stamp = md5_s+str(stamp)+'pythonapi'
        # log.debug(md5_stamp)
        sign = hashlib.md5(md5_stamp.encode('utf-8')).hexdigest()
        # log.debug(sign)
        data = self.sendtoRose(plug_url,sign,stamp,ap_model,file_name,user,comment,version,md5_s)
        return data