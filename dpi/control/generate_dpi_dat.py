# coding:utf-8
import time

__author__ = 'xcma'
from dpi.pubilc.des3 import des3
import os
from dpi.pubilc.misc import delFile,get_md5_big
from .dpi_conf_db_base import dc
from dpi.conf.path import dpi_file_save_name,dpi_file_save_name_en,dpi_file_save_path
from appack.models import dpiConfigVersion
import logging
log = logging.getLogger(__name__)
class generateDpiDat:
    """
    生成dpi配置文件专用类
    """
    def __init__(self):
        self.encrypt_dpi_file_path_name = dpi_file_save_path+dpi_file_save_name_en
        self.dencrypt_dpi_file_path_name = dpi_file_save_path+dpi_file_save_name

    def selectConf(self):
        data = dc.get_dpiconf()
        return data

    def gen_file(self,tem,is_encrypt=True):
        try:
            if is_encrypt:
                dpi_file_save_name_ = dpi_file_save_name_en
                is_binary = True
            else:
                dpi_file_save_name_ = dpi_file_save_name
                is_binary = False

            if is_binary:
                write_type = 'wb+'
            else:
                write_type = 'w+'
            delFile(dpi_file_save_path+dpi_file_save_name_)
            filepath = os.path.join(dpi_file_save_path, dpi_file_save_name_)

            with open(filepath, write_type) as fp:
                if isinstance(tem,list):
                    for i in tem:
                        fp.write(i)
                else:
                    fp.write(tem)
            fp.close()
            return True
        except Exception as e:
            log.error(e)
            return False

    def read_file(self,is_encrypt=True):
        if is_encrypt:
            dpi_file_save_name_ = dpi_file_save_name_en
            is_binary = True
        else:
            dpi_file_save_name_ = dpi_file_save_name
            is_binary = False
        if is_binary:
            write_type = 'rb'
        else:
            write_type = 'r'
        filepath = os.path.join(dpi_file_save_path, dpi_file_save_name_)

        with open(filepath, write_type) as fp:
            data = fp.readlines()
        fp.close()
        return data

    def setFormart(self):
        data = self.selectConf()
        line = ''
        for i in data:
            rule_name = i['rule_name']
            rule_id = i['id']
            vi_type_id = i['vi_type_id']
            mtype_id = i['type_id']
            mtype_value = i['type_value']
            rule_data = i['rule_data']
            rule_begin_match = i['rule_begin_match']
            rule_end_match = i['rule_end_match']
            line = line + f'{rule_name} {rule_id} {vi_type_id}  {mtype_id} {mtype_value} {rule_data} {rule_begin_match} {rule_end_match}\n'
        return line

    def insertMysql(self,dev_model,dev_model_id,comment,user):
        try:
            md5 = get_md5_big(self.encrypt_dpi_file_path_name)
            dpi_data = dpiConfigVersion.objects.filter(dev_model_id=dev_model_id, md5=md5).count()
            if dpi_data == 0:
                upload = dpiConfigVersion()
                upload.zdpi_sig_version = int(time.time())
                upload.zdpi_sig_file = self.encrypt_dpi_file_path_name
                upload.dev_model_id = dev_model_id
                upload.comment = comment
                upload.dev_model = dev_model
                upload.md5 = md5
                upload.user = user
                upload.save()
            return True
        except Exception as e:
            log.error(e)
            return False


    def generateDpiFile(self,dev_model,dev_model_id,comment,user):
        data = self.setFormart()
        idata = '插入数据库失败'

        if data:
            encrypt_data = des3.encrypt(data)
            unencrypt_res = self.gen_file(data,is_encrypt=False)
            encrypt_res = self.gen_file(encrypt_data)
            # decode_data = des3.decrypt(self.read_file(is_encrypt=True)[0])
            # log.debug(decode_data)
            if unencrypt_res:
                de_data = '生成DPI未加密文件成功'
            else:
                de_data = '生成DPI未加密文件失败'
            if encrypt_res:
                en_data = '生成DPI加密文件成功'
                if self.insertMysql(dev_model,dev_model_id,comment,user):
                   idata = '插入数据库成功'

            else:
                en_data = 'error:生成DPI加密文件失败'
        else:
            en_data = 'error:未找到DPI配置信息'
            de_data = ''
        data = f'{en_data},{de_data},{idata}'
        log.debug(data)
        return data


gDpi = generateDpiDat()