import os
import pathlib
import shlex
import subprocess

unpack_cmd_tar = 'tar xf '
unpack_cmd_tar_tgz = 'tar zxvf '
unpack_cmd_tar_bz2 = 'tar -xjf '
unpack_cmd_unzip = 'unzip -o '
work_path = '/opt/build_tools/'
mr820 = 'fenghuo_MR820/'
jcbyl_mr820 = '/data/nextcloud/rom/files/FIBH\|烽火/重庆烽火/三合一\|MR820/交叉编译链/'
name_mr820 = 'mr820.tar.gz'
build_jcbyl_path_mr820 = 'rsdk-1.5.8-4281-EB-2.6.30-0.9.30.3-m32ub-120907/bin'

RG020ET_CA = 'beier_RG020ET-CA/'
jcbyl_RG020ET_CA = '/data/nextcloud/rom/files/BELL\|上海贝尔/三合一\|RG020ET-CA/交叉编译链/'
name_RG020ET_CA = 'beier_RG020ET-CA.tar.gz'
build_jcbyl_path_RG020ET_CA = 'rsdk-1.5.8-4281-EB-2.6.30-0.9.30.3-m32ub-120907/bin'

HG510E = 'youhua_HG510E/'
jcbyl_HG510E = '/data/nextcloud/rom/files/YHTX\|友华/三合一\|HG510E/交叉编译链/中国电信版本\|交叉编译链/'
name_HG510E = 'HG510E.tar.gzip'
build_jcbyl_path_HG510E = 'buildroot-gcc463/usr/lib'

HG510PG = 'youhua_HG510PG/'
jcbyl_HG510PG = '/data/nextcloud/rom/files/YHTX\|友华/四合一\|HG510PG/交叉编译链/'
name_HG510PG = 'HG510PG.tar.gzip'
build_jcbyl_path_HG510PG = 'opt/trendchip/mips-linux-uclibc-4.9.3/usr/'

G2_100B = 'yinhe_G2-100B/'
jcbyl_G2_100B = '/data/nextcloud/rom/files/YHDZ\|银河电子/三合一\|G2-100B/交叉编译链/'
name_G2_100B = 'G2-100B.tar.gzip'
build_jcbyl_path_G2_100B = 'rsdk-1.5.5-4181-EB-2.6.30-0.9.30.3-110225/bin'

DTTV200 = 'datang_DTTV200/'
jcbyl_DTTV200 = '/data/nextcloud/rom/files/DTYD\|大唐移动/三合一\|DTTV200/交叉编译链/'
name_DTTV200 = 'DTTV200_buildroot-gcc463.tar.gzip'
build_jcbyl_path_DTTV200 = 'buildroot-gcc463/usr/lib'

E909 = 'chuangwei_E909/'
jcbyl_E909 = '/data/nextcloud/rom/files/Skyworth\|创维/三合一\|E909/交叉编译链/'
name_E909 = 'E909.tar.gzip'
build_jcbyl_path_E909 = 'rsdk-1.5.5-4181-EB-2.6.30-0.9.30.3-110225/bin'

E910V10C = 'chuangwei_E910V10C/'
jcbyl_E910V10C = '/data/nextcloud/rom/files/Skyworth\|创维/三合一\|E910V10C/交叉编译链/'
name_E910V10C = 'E910V10C.tar.gzip'
build_jcbyl_path_E910V10C = 'rsdk-1.5.5-5281-EB-2.6.30-0.9.30.3-110714/bin'

MR622_BJ = 'fenghuo_MR622-BJ/'
jcbyl_MR622_BJ = '/data/nextcloud/rom/files/FIBH\|烽火/重庆烽火/四合一\|MR622-BJ/交叉编译链/'
name_MR622_BJ = 'MR622-BJ.tar.gzip'
build_jcbyl_path_MR622_BJ = 'opt/toolchains/crosstools-mips-gcc-4.6-linux-3.4-uclibc-0.9.32-binutils-2.21/usr/lib'

dt741 = 'chuagnwei_DT741/'
jcbyl_dt741 = '/data/nextcloud/rom/files/Skyworth\|创维/四合一\|DT741/交叉编译链/'
name_dt741 = 'DT741.tar.gzip'
build_jcbyl_path_dt741 = 'mips-linux-uclibc/usr/bin'

dt541 = 'tjdx_chuangwei_DT541/'
jcbyl_dt541 = '/data/nextcloud/rom/files/Skyworth\|创维/四合一\|DT541/交叉编译链/'
name_dt541 = 'cross_compiler.tar'
build_jcbyl_path_dt541 = 'mips-linux-uclibc/usr/bin'

js212e = 'zhongyi_js212e/'
jcbyl_js212e = '/data/nextcloud/rom/files/DWnet\|中怡数宽/三合一\|JS212E/交叉编译链/'
name_js212e = 'JS212E.JS212F.tar.gzip'
build_jcbyl_path_js212e = 'mips-linux-glibc-4.9.3/usr/bin'

r2000 = 'datang_R2000AP-IN/'
jcbyl_r2000 = '/data/nextcloud/rom/files/DTDX\|西安大唐/二合一\|C2DT-M362/交叉编译链/'
name_r2000 = 'C2DT-M362.tar.gzip'
build_jcbyl_path_r2000 = 'buildroot-gcc342/bin'

S_BOX8Q74 = 'zhaoge_S-BOX8Q74/'
jcbyl_S_BOX8Q74 = '/data/nextcloud/rom/files/SUNNIWELL\|朝歌/三合一\|S-BOX8Q74/交叉编译链/'
name_S_BOX8Q74 = 'S-BOX8Q74.tar.gzip'
build_jcbyl_path_S_BOX8Q74 = 'rsdk-4.8.5-5281-EB-3.18-u0.9.33-m32ut-150818p01_151020/bin'

S_BOX8Q74C = 'zhaoge_S-BOX8Q74C/'
jcbyl_S_BOX8Q74C = '/data/nextcloud/rom/files/SUNNIWELL\|朝歌/三合一\|S-BOX8Q74C/交叉编译链/'
name_S_BOX8Q74C = 'S-BOX8Q74C.tar.gzip'
build_jcbyl_path_S_BOX8Q74C = 'buildroot-gcc342/bin'

S_BOX8Q94 = 'zhaoge_S-BOX8Q94/'
jcbyl_S_BOX8Q94 = '/data/nextcloud/rom/files/SUNNIWELL\|朝歌/四合一\|S-BOX8Q94/交叉编译链/'
name_S_BOX8Q94 = 'S-BOX8Q94.tar.gzip'
build_jcbyl_path_S_BOX8Q94 = 'rsdk-4.8.5-5281-EB-3.18-u0.9.33-m32ut-150818p01_151020/bin'

Z84 = 'zhaoneng_Z84/'
jcbyl_Z84 = '/data/nextcloud/rom/files/SUNNIWELL\|兆能/三合一\|Z84/交叉编译链/'
name_Z84 = 'Z84.KPR008.Sbox-8L74.tar.gzip'
build_jcbyl_path_Z84 = 'buildroot-gcc342/bin'

kpr008 = 'kangpu_kpr008/'
jcbyl_kpr008 = '/data/nextcloud/rom/files/SUNNIWELL\|康普/三合一\|KP-R008/交叉编译链/'
name_kpr008 = 'Z84.KPR008.Sbox-8L74.tar.gzip'
build_jcbyl_path_kpr008 = 'buildroot-gcc342/bin'

S_BOX8L74 = 'zhaoge_S-BOX8L74/'
jcbyl_S_BOX8L74 = '/data/nextcloud/rom/files/SUNNIWELL\|康普/三合一\|KP-R008/交叉编译链/'
name_S_BOX8L74 = 'Z84.KPR008.Sbox-8L74.tar.gzip'
build_jcbyl_path_S_BOX8L74 = 'buildroot-gcc342/bin'

S_BOX8L94 = 'zhaoge_S-BOX8L94/'
jcbyl_S_BOX8L94 = '/data/nextcloud/rom/files/SUNNIWELL\|朝歌/四合一\|S-BOX8L94/交叉编译链/'
name_S_BOX8L94 = 'S-BOX8L94_rsdk-4.8.5-5281-EB-3.18-u0.9.33-m32ut-150818p01_151020.tar.gzip'
build_jcbyl_path_S_BOX8L94 = 'rsdk-4.8.5-5281-EB-3.18-u0.9.33-m32ut-150818p01_151020/bin'

PT926G = 'youhua_PT926G/'
jcbyl_PT926G = '/data/nextcloud/rom/files/YHTX\|友华/四合一\|PT926G/交叉编译链/'
name_PT926G = 'PT926G_msdk-4.8.5-mips-EB-3.18-u0.9.33-m32ut-170828_lunapro-171213_yueme.tar.gzip'
build_jcbyl_path_PT926G = 'msdk-4.8.5-mips-EB-3.18-u0.9.33-m32ut-170828_lunapro-171213_yueme/bin'

# # MR622-KK/MR222-KK
MTK7526 = 'fenghuo_MTK7526/'
jcbyl_MTK7526 = '/data/nextcloud/rom/files/FIBH\|烽火/重庆烽火/四合一\|MR222-KK/交叉编译链/'
name_MTK7526 = 'MR622-KK_MR222-KK_7526-gcc-MTK7526.tar.gzip'
build_jcbyl_path_MTK7526 = '7526-gcc/usr/lib'

# MR820-LK
MR820_LK = 'fenghuo_MR820-LK/'
jcbyl_MR820_LK = '/data/nextcloud/rom/files/FIBH\|烽火/重庆烽火/三合一\|MR820-LK/交叉编译链/'
name_MR820_LK = 'MR820-LK_RELTKmsdk-4.4.7-mips-EL-3.10-u0.9.33-m32t-140827.tar.gz'
build_jcbyl_path_MR820_LK = 'msdk-4.4.7-mips-EL-3.10-u0.9.33-m32t-140827/bin'

FHS7100 = 'yunpu_FHS7100/'
jcbyl_FHS7100 = '/data/nextcloud/rom/files/WinPal\|云普/光猫二合一\|FHS7100/交叉编译链/'
name_FHS7100 = 'FHS7100_rsdk-1.5.6-5281-EB-2.6.30-0.9.30.3-131105.tar.gzip'
build_jcbyl_path_FHS7100 = 'rsdk-1.5.6-5281-EB-2.6.30-0.9.30.3-131105/bin'

BK_RC_M1 = 'weimeng_BK-RC-M1/'
jcbyl_BK_RC_M1 = '/data/nextcloud/rom/files/WAYOS\|维盟/AC网关\|BK-RC-M1/交叉编译链/'
name_BK_RC_M1 = 'BK-RC-M1.tar.gz'
build_jcbyl_path_BK_RC_M1 = 'buildroot-gcc463/usr/lib'

BK_RC_2 = 'wanwangbotong_BK-RC-2/'
jcbyl_BK_RC_2 = '/data/nextcloud/rom/files/TG-NET\|万网博通/AC网关\|BK-RC-2/交叉编译链/'
name_BK_RC_2 = 'BK-RC-2_X86_OpenWrt-SDK-ramips-for-redhat-i686-gcc-4.8-linaro_uClibc-0.9.33.2.tar.bz2'
build_jcbyl_path_BK_RC_2 = 'OpenWrt-SDK-ramips-for-redhat-i686-gcc-4.8-linaro_uClibc-0.9.33.2/staging_dir'

BK_AP300_MRW1 = 'weimeng_BK-AP300-MRW1/'
jcbyl_BK_AP300_MRW1 = '/data/nextcloud/rom/files/WAYOS\|维盟/二合一\|BK-AP300-MRW1/交叉编译链/'
name_BK_AP300_MRW1 = 'buildroot-gcc342-wayos.tar.gz'
build_jcbyl_path_BK_AP300_MRW1 = 'buildroot-gcc342-wayos/bin'

# HG1023/HG1024
HG1023 = 'shuangying_HG1023/'
jcbyl_HG1023 = '/data/nextcloud/rom/files/Allwins\|双赢伟业/HG1023、HG1024\|交叉编译链/'
name_HG1023 = 'toolchain_gcc4.6.3_glibc_1028.tar.gz'
build_jcbyl_path_HG1023 = 'mips-linux-glibc-4.6.3/usr/lib'

H10g_12 = 'glwd_H10g-12/'
jcbyl_H10g_12 = '/data/nextcloud/rom/files/GLWD\|格林伟迪/H10g-12/交叉编译链/'
name_H10g_12 = 'H10g-12.tar.bz2'
build_jcbyl_path_H10g_12 = 'msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331_cmcc/bin'

H10e_12 = 'glwd_H10e-12/'
jcbyl_H10e_12 = '/data/nextcloud/rom/files/GLWD\|格林伟迪/H10e-12/交叉编译链/'
name_H10e_12 = 'msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331_cmcc.tgz'
build_jcbyl_path_H10e_12 = 'msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331_cmcc/bin'

# TEWA-808WG TEWA-808AG  TEWA-808AE
TEWA_808 = 'tianyi_TEWA-808/'
jcbyl_TEWA_808 = '/data/nextcloud/rom/files/SCTY\|四川天邑/三合一\|TEWA-808WG/交叉编译链/'
name_TEWA_808 = 'TEWA-808.tar.gz'
build_jcbyl_path_TEWA_808 = 'crosstools-mips-gcc-5.3-linux-4.1-uclibc-1.0.12-binutils-2.25-NPTL/usr/lib'

B860GV21P = 'zhongxing_B860GV21P/'
jcbyl_B860GV21P = '/data/nextcloud/rom/files/ZTE\|中兴/B860GV2.1-P/交叉编译链/'
name_B860GV21P = 'arm-linux-uclibcgnueabi-strcmp.tar.gz'
build_jcbyl_path_B860GV21P = 'arm-linux-uclibcgnueabi-strcmp/bin'

B860GV21P_arm = 'zhongxing_B860GV2.1-P-arm/'
jcbyl_B860GV21P_arm = '/data/nextcloud/rom/files/ZTE\|中兴/B860GV2.1-P/交叉编译链/B860GV2.1-P-arm'
name_B860GV21P_arm = 'arm-linux-glibc.tar.gz'
build_jcbyl_path_B860GV21P_arm = 'arm-linux-glibc/lib'

B860GV21P_usr = 'zhongxing_B860GV2.1-P-usr/'
jcbyl_B860GV21P_usr = '/data/nextcloud/rom/files/ZTE\|中兴/B860GV2.1-P/交叉编译链/B860GV2.1-P-usr'
name_B860GV21P_usr = 'usr.tar.gz'
build_jcbyl_path_B860GV21P_usr = 'usr/lib'

B860GV21P_release = 'zhongxing_B860GV2.1-P_release/'
jcbyl_B860GV21P_release = '/data/nextcloud/rom/files/ZTE\|中兴/B860GV2.1-P/交叉编译链/'
name_B860GV21P_release = 'B860G2.1P_release_cross_mobile.tar.gz'
build_jcbyl_path_B860GV21P_release = 'arm-linux-uclibcgnueabi-strcmp/bin'

# QT1905 QT1906
QT190X = 'kukukeji_QT190X/'
jcbyl_QT190X = '/data/nextcloud/rom/files/QMER\|酷酷科技/三合一\|QT1906/交叉编译链/'
name_QT190X = 'arm-linux-glibc.tar.bz2'
build_jcbyl_path_QT190X = 'arm-linux-glibc/lib'

# TW-804 TW-805
TW_80X = 'teyizg_TW-80X/'
jcbyl_TW_80X = '/data/nextcloud/rom/files/TYZG\|特易中国/TW-804/交叉编译链/'
name_TW_80X = 'msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331_cmcc.tgz'
build_jcbyl_path_TW_80X = 'msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331_cmcc/bin'

# H10e-11 H10g-13
H10e_11 = 'cmcc_xwrj_H10e-11/'
jcbyl_H10e_11 = '/data/nextcloud/rom/files/STARNET\|星网锐捷/CMCC\|H10e-11/交叉编译链/'
name_H10e_11 = 'cross_compiler.tar'
build_jcbyl_path_H10e_11 = 'cross_compiler/arm-linux-glibc/lib'

# 交叉编译链有误
DT741v230 = 'chuagnwei_DT741v230/'
jcbyl_DT741v230 = '/data/nextcloud/rom/files/Skyworth\|创维/四合一\|DT741V230/交叉编译链/'
name_DT741v230 = 'DT741v230_x64.buildroot-gcc342.tar.bz2'
build_jcbyl_path_DT741v230 = 'cross_compiler/arm-linux-uclibcgnueabi_soft_x64_rpc_ipv6/bin'

R3Gv2 = 'dawo_xiaomi_R3Gv2/'
jcbyl_R3Gv2 = '/data/nextcloud/rom/files/Xiaomi\|小米通讯/R3Gv2/交叉编译链/'
name_R3Gv2 = 'R3Gv2.tar.gz'
build_jcbyl_path_R3Gv2 = 'sdk_package/toolchain/lib'

T15_04 = 'zywulian_T15-04_T15-05/'
jcbyl_T15_04 = '/data/nextcloud/rom/files/CMTOT\|中移物联/T15-04_T15-05/交叉编译链/'
name_T15_04 = 'T15-04_T15-05.tar.gz'
build_jcbyl_path_T15_04 = 'mips-linux-glibc-4.6.3/usr/lib'

H810G = 'cmcc_xwrj_H810G/'
jcbyl_H810G = '/data/nextcloud/rom/files/STARNET\|星网锐捷/CMCC\|H810G/中兴微方案/交叉编译链/'
name_H810G = 'H810G_cross_compiler.tar'
build_jcbyl_path_H810G = 'cross_compiler/arm-linux-glibc/bin'

H810G_MTK = 'cmcc_xwrj_H810G_MTK/'
jcbyl_H810G_MTK = '/data/nextcloud/rom/files/STARNET\|星网锐捷/CMCC\|H810G/MTK方案/交叉编译链/'
name_H810G_MTK = 'trendchip_xingwangruijie.tar.bz2'
build_jcbyl_path_H810G_MTK = 'mips-linux-uclibc/bin/'

SVG6000RW_M = 'cmcc_xwrj_SVG6000RW-M/'
jcbyl_SVG6000RW_M = '/data/nextcloud/rom/files/STARNET\|星网锐捷/CMCC\|SVG6000RW-M/中兴微方案/交叉编译链/'
name_SVG6000RW_M = 'SVG6000RW-M_cross_compiler.tar'
build_jcbyl_path_SVG6000RW_M = 'cross_compiler/arm-linux-glibc/bin'

SVG6000RW_M_MTK = 'cmcc_xwrj_SVG6000RW-M-MTK/'
jcbyl_SVG6000RW_M_MTK = '/data/nextcloud/rom/files/STARNET\|星网锐捷/CMCC\|SVG6000RW-M/MTK方案/交叉编译链/'
name_SVG6000RW_M_MTK = 'buildroot-gcc342.tar.gz'
build_jcbyl_path_SVG6000RW_M_MTK = 'buildroot-gcc342/bin'

BK_AP300_MRW2 = 'weimeng_BK-AP300-MRW2/'
jcbyl_BK_AP300_MRW2 = '/data/nextcloud/rom/files/WAYOS\|维盟/二合一\|BK-AP300-MRW2/交叉编译链/'
name_BK_AP300_MRW2 = 'buildroot-gcc463.tar.gz'
build_jcbyl_path_BK_AP300_MRW2 = 'buildroot-gcc463/usr/lib'

MR222_BJ = 'fenghuo_MR222-BJ/'
jcbyl_MR222_BJ = '/data/nextcloud/rom/files/FIBH\|烽火/天津烽火/四合一\|MR222-BJ/交叉编译链/'
name_MR222_BJ = 'brcm_crosstools-gcc-4.6-linux-3.4-uclibc-0.9.32-binutils-2.21.Rel0.6-full.tar.bz2'
build_jcbyl_path_MR222_BJ = 'opt/toolchains/crosstools-mips-gcc-4.6-linux-3.4-uclibc-0.9.32-binutils-2.21/usr/bin/'

IP206H_F = 'haixin_IP206H-F/'
jcbyl_IP206H_F = '/data/nextcloud/rom/files/HBMT\|海信/IP106H-F/交叉编译链（与IP206H-F交叉编译链一样）/'
name_IP206H_F = '2019-11-19\|海信-山东联通安审 插件econet-mips-linux-uclibc-4.9.3.tar.gz'
build_jcbyl_path_IP206H_F = 'opt/trendchip/mips-linux-uclibc-4.9.3'

HG521G_SDLT = 'youhua_HG521G_SDLT/'
jcbyl_HG521G_SDLT = '/data/nextcloud/rom/files/YHTX\|友华/四合一\|HG521G/交叉编译链/山东联通对接交叉编译链/'
name_HG521G_SDLT = 'msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331.bz2'
build_jcbyl_path_HG521G_SDLT = 'usr/bin/'

DT741_SDLT = 'chuangwei_DT741_SDLT/'
jcbyl_DT741_SDLT = '/data/nextcloud/rom/files/固件\|交叉编译链\|相关文档/Skyworth\|创维/山东联通版本交叉编译链\|DT541\|DT741\|E910V10C/'
name_DT741_SDLT = 'skyworth_cross_compiler.tar'
build_jcbyl_path_DT741_SDLT = 'arm-linux-glibc'


def file_is_have(file_path):
    """
    path.exist()  检查路径是否存在
    path.is_file() 检查文件是否存在
    :param file_path:
    :return:
    """
    print('开始检查目录：{}'.format(file_path))
    try:
        fp = str(file_path)
        path = pathlib.Path(fp)
        if path.exists():
            if path.is_file():
                print('已找到路径:{}'.format(fp))
                return 1
        return 0
    except Exception as e:
        print(e)


def is_have_file(path_name):
    '这个路径 是否存在，只能是路径'
    try:
        res = os.path.exists(path_name)
        # print('------2222222222-------判断目录{}---是否存在结果：{}'.format(path_name,res))
        return res
    except Exception as e:
        print(e)


def cpDir(path, search_path, target):
    # 如果返现目录不正确，则在当前目录下遍历目标目录，如果目标目录存在，则复制到指定目录下
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            print('{}---{}'.format(path + search_path, c_path))
            if path + search_path != c_path:
                if search_path in c_path:
                    cmd = [f'cp -r {c_path} {target}', f'rm -rf {c_path}']
                    for i in cmd:
                        executionShell(i, path)
                        print(i)
                else:
                    cpDir(c_path, search_path, target)
            else:
                print('解压路径与期望路径一致：{}={}'.format(path + search_path, c_path))


def executionShell(cmdstring, cwd=None, timeout=None, shell=True):
    """
    执行一个SHELL命令
    封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
    参数:
        cwd: 到指定路径下，执行shell命令
        timeout: 超时时间，秒，支持小数，精度0.1秒
        shell: 是否通过shell运行
    """
    try:
        if shell:
            cmdstring_list = cmdstring
        else:
            cmdstring_list = shlex.split(cmdstring)
        p = subprocess.Popen(cmdstring_list, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
                             shell=shell)
        p.wait(timeout)
        data = []
        for line in iter(p.stdout.readline, b''):
            try:
                if len(line) > 1:
                    try:
                        line = line.replace('\n', '')
                    except:
                        pass
                    try:
                        line = line.decode('utf-8')
                    except:
                        pass
                    if line: print('{}'.format(line))
            except:
                print('异常输出信息：{}'.format(line))
                pass
            finally:
                data.append(line)
        p.stdout.close()
        if data: print(data)
        return data
    except Exception as e:
        print(e)


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    try:
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            print(f'新增目录 {path}')
        return True
    except:
        return False


def mkdirP(path):
    cmd = f'mkdir -p {path}'
    executionShell(cmd)


def cpUnpack(target, src, name, ucmd, bpath):
    # if not file_is_have(f'{target}{name}'):
    mkdir(target)
    if not is_have_file(target + bpath):
        cmd = [f'cp -r {src}{name} {target}', f'{ucmd} {name}']
        print(f'{target}{bpath} OOOOOOOOOOOO【执行复制解压操作】')
        for c in cmd:
            executionShell(c, target)
        if not is_have_file(target + bpath):
            search_path = bpath.split('/')[0]
            cpDir(target, search_path, target)
            if not is_have_file(target + bpath):
                print(f'{target}{bpath} 失败 step 2')
            else:
                print(f'{target}{bpath} 成功 step 2')
                executionShell(f'rm -rf {name}', target)
        else:
            print(f'{target}{bpath} 成功 step 1')
    else:
        print(f'{target}{bpath} 111111111111【构建环境正常】')


def initJCBYL():
    for j in jl:
        target = j['target']
        src = j['src']
        name = j['name']
        bpath = j['bpath']
        cmd = j['cmd']
        cpUnpack(work_path + target, src, name, cmd, bpath)
    print('初始化交叉编译环境全部完成')


if __name__ == '__main__':
    jl = [
        # {'target': mr820, 'src': jcbyl_mr820, 'name': name_mr820, 'bpath':build_jcbyl_path_mr820,'cmd': unpack_cmd_tar},
        # {'target': RG020ET_CA, 'src': jcbyl_RG020ET_CA, 'name': name_RG020ET_CA,'bpath':build_jcbyl_path_RG020ET_CA, 'cmd': unpack_cmd_tar},
        # {'target': HG510E, 'src': jcbyl_HG510E, 'name': name_HG510E, 'bpath':build_jcbyl_path_HG510E,'cmd': unpack_cmd_tar},
        # {'target': HG510PG, 'src': jcbyl_HG510PG, 'name': name_HG510PG, 'bpath':build_jcbyl_path_HG510PG,'cmd': unpack_cmd_tar},
        # {'target': G2_100B, 'src': jcbyl_G2_100B, 'name': name_G2_100B, 'bpath':build_jcbyl_path_G2_100B, 'cmd': unpack_cmd_tar},
        # {'target': DTTV200, 'src': jcbyl_DTTV200, 'name': name_DTTV200, 'bpath': build_jcbyl_path_DTTV200,'cmd': unpack_cmd_tar},
        # {'target': E909, 'src': jcbyl_E909, 'name': name_E909, 'bpath':build_jcbyl_path_E909,'cmd': unpack_cmd_tar},
        # {'target': E910V10C, 'src': jcbyl_E910V10C, 'name': name_E910V10C, 'bpath':build_jcbyl_path_E910V10C,'cmd': unpack_cmd_tar},
        # {'target': MR622_BJ, 'src': jcbyl_MR622_BJ, 'name': name_MR622_BJ, 'bpath':build_jcbyl_path_MR622_BJ,'cmd': unpack_cmd_tar},
        # {'target': dt741, 'src': jcbyl_dt741, 'name': name_dt741, 'bpath':build_jcbyl_path_dt741,'cmd': unpack_cmd_tar},
        # {'target': js212e, 'src': jcbyl_js212e, 'name': name_js212e, 'bpath': build_jcbyl_path_js212e,'cmd': unpack_cmd_tar},
        # {'target': r2000, 'src': jcbyl_r2000, 'name': name_r2000, 'bpath': build_jcbyl_path_r2000,'cmd': unpack_cmd_tar},
        # {'target': S_BOX8Q74, 'src': jcbyl_S_BOX8Q74, 'name': name_S_BOX8Q74, 'bpath': build_jcbyl_path_S_BOX8Q74,'cmd': unpack_cmd_tar},
        # {'target': S_BOX8Q74C, 'src': jcbyl_S_BOX8Q74C, 'name': name_S_BOX8Q74C, 'bpath': build_jcbyl_path_S_BOX8Q74C,'cmd': unpack_cmd_tar},
        # {'target': S_BOX8Q94, 'src': jcbyl_S_BOX8Q94, 'name': name_S_BOX8Q94, 'bpath': build_jcbyl_path_S_BOX8Q94,'cmd': unpack_cmd_tar},
        # {'target': Z84, 'src': jcbyl_Z84, 'name': name_Z84, 'bpath': build_jcbyl_path_Z84,'cmd': unpack_cmd_tar},
        # {'target': kpr008, 'src': jcbyl_kpr008, 'name': name_kpr008, 'bpath': build_jcbyl_path_kpr008,'cmd': unpack_cmd_tar},
        # {'target': S_BOX8L74, 'src': jcbyl_S_BOX8L74, 'name': name_S_BOX8L74, 'bpath': build_jcbyl_path_S_BOX8L74,'cmd': unpack_cmd_tar},
        # {'target': S_BOX8L94, 'src': jcbyl_S_BOX8L94, 'name': name_S_BOX8L94, 'bpath': build_jcbyl_path_S_BOX8L94,'cmd': unpack_cmd_tar},
        # {'target': PT926G, 'src': jcbyl_PT926G, 'name': name_PT926G, 'bpath': build_jcbyl_path_PT926G,'cmd': unpack_cmd_tar},
        # {'target': MTK7526, 'src': jcbyl_MTK7526, 'name': name_MTK7526, 'bpath':build_jcbyl_path_MTK7526,'cmd': unpack_cmd_tar},
        # {'target': MR820_LK, 'src': jcbyl_MR820_LK, 'name': name_MR820_LK, 'bpath':build_jcbyl_path_MR820_LK,'cmd': unpack_cmd_tar},
        # {'target': FHS7100, 'src': jcbyl_FHS7100, 'name': name_FHS7100, 'bpath':build_jcbyl_path_FHS7100,'cmd': unpack_cmd_tar},
        # {'target': BK_RC_M1, 'src': jcbyl_BK_RC_M1, 'name': name_BK_RC_M1, 'bpath':build_jcbyl_path_BK_RC_M1,'cmd': unpack_cmd_tar},
        # {'target': BK_RC_2, 'src': jcbyl_BK_RC_2, 'name': name_BK_RC_2, 'bpath':build_jcbyl_path_BK_RC_2,'cmd': unpack_cmd_tar},
        # {'target': BK_AP300_MRW1, 'src': jcbyl_BK_AP300_MRW1, 'name': name_BK_AP300_MRW1, 'bpath':build_jcbyl_path_BK_AP300_MRW1,'cmd': unpack_cmd_tar},
        # {'target': HG1023, 'src': jcbyl_HG1023, 'name': name_HG1023, 'bpath':build_jcbyl_path_HG1023,'cmd': unpack_cmd_tar},
        # {'target': H10g_12, 'src': jcbyl_H10g_12, 'name': name_H10g_12, 'bpath':build_jcbyl_path_H10g_12,'cmd': unpack_cmd_tar_bz2},
        # {'target': H10e_12, 'src': jcbyl_H10e_12, 'name': name_H10e_12, 'bpath':build_jcbyl_path_H10e_12,'cmd': unpack_cmd_tar_tgz},
        # {'target': TEWA_808, 'src': jcbyl_TEWA_808, 'name': name_TEWA_808, 'bpath':build_jcbyl_path_TEWA_808,'cmd': unpack_cmd_tar},
        # {'target': B860GV21P, 'src': jcbyl_B860GV21P, 'name': name_B860GV21P, 'bpath':build_jcbyl_path_B860GV21P,'cmd': unpack_cmd_tar},
        # {'target': B860GV21P_release, 'src': jcbyl_B860GV21P_release, 'name': name_B860GV21P_release, 'bpath':build_jcbyl_path_B860GV21P_release,'cmd': unpack_cmd_tar},
        # {'target': B860GV21P_arm, 'src': jcbyl_B860GV21P_arm, 'name': name_B860GV21P_arm, 'bpath':build_jcbyl_path_B860GV21P_arm,'cmd': unpack_cmd_tar},
        # {'target': B860GV21P_usr, 'src': jcbyl_B860GV21P_usr, 'name': name_B860GV21P_usr, 'bpath':build_jcbyl_path_B860GV21P_usr,'cmd': unpack_cmd_tar},
        # {'target': QT190X, 'src': jcbyl_QT190X, 'name': name_QT190X, 'bpath':build_jcbyl_path_QT190X,'cmd': unpack_cmd_tar},
        # {'target': TW_80X, 'src': jcbyl_TW_80X, 'name': name_TW_80X, 'bpath':build_jcbyl_path_TW_80X,'cmd': unpack_cmd_tar},
        # {'target': H10e_11, 'src': jcbyl_H10e_11, 'name': name_H10e_11, 'bpath':build_jcbyl_path_H10e_11,'cmd': unpack_cmd_tar},
        # # {'target': DT741v230, 'src': jcbyl_DT741v230, 'name': name_DT741v230, 'bpath':build_jcbyl_path_DT741v230,'cmd': unpack_cmd_tar},
        # {'target': R3Gv2, 'src': jcbyl_R3Gv2, 'name': name_R3Gv2, 'bpath': build_jcbyl_path_R3Gv2,'cmd': unpack_cmd_tar},
        # {'target': T15_04, 'src': jcbyl_T15_04, 'name': name_T15_04, 'bpath': build_jcbyl_path_T15_04,'cmd': unpack_cmd_tar},
        # {'target': H810G, 'src': jcbyl_H810G, 'name': name_H810G, 'bpath': build_jcbyl_path_H810G,'cmd': unpack_cmd_tar},
        # {'target': SVG6000RW_M, 'src': jcbyl_SVG6000RW_M, 'name': name_SVG6000RW_M, 'bpath': build_jcbyl_path_SVG6000RW_M,'cmd': unpack_cmd_tar},
        # {'target': BK_AP300_MRW2, 'src': jcbyl_BK_AP300_MRW2, 'name': name_BK_AP300_MRW2, 'bpath': build_jcbyl_path_BK_AP300_MRW2,'cmd': unpack_cmd_tar},
        # {'target': MR222_BJ, 'src': jcbyl_MR222_BJ, 'name': name_MR222_BJ, 'bpath': build_jcbyl_path_MR222_BJ,'cmd': unpack_cmd_tar_bz2},
        # {'target': H810G_MTK, 'src': jcbyl_H810G_MTK, 'name': name_H810G_MTK, 'bpath': build_jcbyl_path_H810G_MTK,'cmd': unpack_cmd_tar_bz2},
        # {'target': SVG6000RW_M_MTK, 'src': jcbyl_SVG6000RW_M_MTK, 'name': name_SVG6000RW_M_MTK, 'bpath': build_jcbyl_path_SVG6000RW_M_MTK,'cmd': unpack_cmd_tar_tgz},
        # {'target': dt541, 'src': jcbyl_dt541, 'name': name_dt541, 'bpath': build_jcbyl_path_dt541,'cmd': unpack_cmd_tar},
        # {'target': IP206H_F, 'src': jcbyl_IP206H_F, 'name': name_IP206H_F, 'bpath': build_jcbyl_path_IP206H_F,'cmd': unpack_cmd_tar},
        # {'target': HG521G_SDLT, 'src': jcbyl_HG521G_SDLT, 'name': name_HG521G_SDLT, 'bpath': build_jcbyl_path_HG521G_SDLT,'cmd': unpack_cmd_tar_bz2},
        {'target': DT741_SDLT, 'src': jcbyl_DT741_SDLT, 'name': name_DT741_SDLT, 'bpath': build_jcbyl_path_DT741_SDLT,'cmd': unpack_cmd_tar},

    ]
    print('配置编译环境数量：{}'.format(len(jl)))
    # initDir()
    initJCBYL()
    # cpDir('/Users/xuechao.ma/Downloads','/简书/user-1870882-1555474029/Tools','/Users/xuechao.ma/Downloads/test')
