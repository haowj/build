# coding:utf-8
__author__ = 'xcma'

import platform

dpi_file_save_name_en = 'zdpi-sig.dat'
dpi_file_save_name = 'enzdpi-sig.dat'
if 'Linux' in platform.system():
    dpi_file_save_path = '/home/zjzy/build_output/dpi_conf/'
elif 'Windows' in platform.system():
    dpi_file_save_path = '/home/log/'
else:
    dpi_file_save_path = '/Users/xuechao.ma/Downloads/'
