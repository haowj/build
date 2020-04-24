#!/bin/bash

build_env=/opt/build_tools
echo $1
echo $2

if [ "$1" = "pc" ]; then
    CROSS_TOOLS_PATH=
    CROSS_TOOLS_TARGET=
fi

if [ "$1" = "mr820" ]; then
    CROSS_TOOLS_PATH=$build_env/fenghuo_MR820/rsdk-1.5.8-4281-EB-2.6.30-0.9.30.3-m32ub-120907/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "rg020et" ]; then
    CROSS_TOOLS_PATH=$build_env/beier_RG020ET-CA/rsdk-1.5.8-4281-EB-2.6.30-0.9.30.3-m32ub-120907/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "hg510e" ]; then
    export LD_LIBRARY_PATH=$build_env/youhua_HG510E/buildroot-gcc463/usr/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/youhua_HG510E/buildroot-gcc463/usr/bin
    CROSS_TOOLS_TARGET=mipsel-linux
fi

if [ "$1" = "hg510pg" ]; then
    export LD_LIBRARY_PATH=$build_env/youhua_HG510PG/opt/trendchip/mips-linux-uclibc-4.9.3/usr/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/youhua_HG510PG/opt/trendchip/mips-linux-uclibc-4.9.3/usr/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "g2100b" ]; then
    CROSS_TOOLS_PATH=$build_env/yinhe_G2-100B/rsdk-1.5.5-4181-EB-2.6.30-0.9.30.3-110225/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "js212e" ]; then
    export LD_LIBRARY_PATH=/opt/build_tools/zhongyi_js212e/mips-linux-glibc-4.9.3/usr/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/zhongyi_js212e/mips-linux-glibc-4.9.3/usr/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "dttv200" ]; then
    export LD_LIBRARY_PATH=$build_env/datang_DTTV200/buildroot-gcc463/usr/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/datang_DTTV200/buildroot-gcc463/usr/bin
    CROSS_TOOLS_TARGET=mipsel-linux
fi

if [ "$1" = "e909" ]; then
    CROSS_TOOLS_PATH=$build_env/chuangwei_E909/rsdk-1.5.5-4181-EB-2.6.30-0.9.30.3-110225/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "e910" ]; then
    export LD_LIBRARY_PATH=$build_env/datang_DTTV200/buildroot-gcc463/usr/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/chuangwei_E910V10C/rsdk-1.5.5-5281-EB-2.6.30-0.9.30.3-110714/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "mr622" ]; then
    export LD_LIBRARY_PATH=$build_env/fenghuo_MR622-BJ/opt/toolchains/crosstools-mips-gcc-4.6-linux-3.4-uclibc-0.9.32-binutils-2.21/usr/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/fenghuo_MR622-BJ/opt/toolchains/crosstools-mips-gcc-4.6-linux-3.4-uclibc-0.9.32-binutils-2.21/usr/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "dt741" ]; then
    CROSS_TOOLS_PATH=$build_env/chuagnwei_DT741/mips-linux-uclibc/usr/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "8q74" ]; then
    CROSS_TOOLS_PATH=$build_env/zhaoge_S-BOX8Q74/rsdk-4.8.5-5281-EB-3.18-u0.9.33-m32ut-150818p01_151020/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "8q74c" ]; then
    CROSS_TOOLS_PATH=$build_env/zhaoge_S-BOX8Q74C/buildroot-gcc342/bin
    CROSS_TOOLS_TARGET=mipsel-linux
fi

if [ "$1" = "8q94" ]; then
    CROSS_TOOLS_PATH=$build_env/zhaoge_S-BOX8Q94/rsdk-4.8.5-5281-EB-3.18-u0.9.33-m32ut-150818p01_151020/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "z84" ]; then
    CROSS_TOOLS_PATH=$build_env/zhaoneng_Z84/buildroot-gcc342/bin
    CROSS_TOOLS_TARGET=mipsel-linux
fi

if [ "$1" = "r2000" ]; then
    CROSS_TOOLS_PATH=$build_env/datang_R2000AP-IN/buildroot-gcc342/bin
    CROSS_TOOLS_TARGET=mipsel-linux
fi

if [ "$1" = "kpr008" ]; then
    CROSS_TOOLS_PATH=$build_env/kangpu_kpr008/buildroot-gcc342/bin
    CROSS_TOOLS_TARGET=mipsel-linux
fi

if [ "$1" = "Sbox-8L74" ]; then
    CROSS_TOOLS_PATH=$build_env/zhaoge_S-BOX8L74/buildroot-gcc342/bin
    CROSS_TOOLS_TARGET=mipsel-linux
fi

if [ "$1" = "sbox8l94" ]; then
    CROSS_TOOLS_PATH=$build_env/zhaoge_S-BOX8L94/rsdk-4.8.5-5281-EB-3.18-u0.9.33-m32ut-150818p01_151020/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "PT926G" ]; then
    CROSS_TOOLS_PATH=$build_env/youhua_PT926G/msdk-4.8.5-mips-EB-3.18-u0.9.33-m32ut-170828_lunapro-171213_yueme/bin
    CROSS_TOOLS_TARGET=mips-linux-uclibc
fi

if [ "$1" = "MTK7526" ]; then # MR622-KK/MR222-KK
    export LD_LIBRARY_PATH=$build_env/fenghuo_MTK7526/7526-gcc/usr/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/fenghuo-MTK7526/7526-gcc/usr/bin
    CROSS_TOOLS_TARGET=mips-buildroot-linux-uclibc
fi

if [ "$1" = "RELTK447" ]; then # MR820-LK
    CROSS_TOOLS_PATH=$build_env/fenghuo_MR820-LK/msdk-4.4.7-mips-EL-3.10-u0.9.33-m32t-140827/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "FHS7100" ]; then
    CROSS_TOOLS_PATH=$build_env/yunpu_FHS7100/rsdk-1.5.6-5281-EB-2.6.30-0.9.30.3-131105/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "BK-RC-M1" ]; then
    export LD_LIBRARY_PATH=$build_env/zjzy_wm_BK-RC-M1/buildroot-gcc463/usr/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/zjzy_BK-RC-M1/buildroot-gcc463/usr/bin
    CROSS_TOOLS_TARGET=mipsel-buildroot-linux-uclibc
fi

#   未找到对应型号
if [ "$1" = "OWRT-MT7621" ]; then
    export STAGING_DIR=/opt/OpenWrt-SDK-ramips-for-redhat-i686-gcc-4.8-linaro_uClibc-0.9.33.2/staging_dir
    CROSS_TOOLS_PATH=/opt/OpenWrt-SDK-ramips-for-redhat-i686-gcc-4.8-linaro_uClibc-0.9.33.2/staging_dir/toolchain-mipsel_24kec+dsp_gcc-4.8-linaro_uClibc-0.9.33.2/bin
    CROSS_TOOLS_TARGET=mipsel-openwrt-linux-uclibc
fi

if [ "$1" = "BK-RC-2" ]; then
    export STAGING_DIR=$build_env/wanwangbotong_BK-RC-2/OpenWrt-SDK-ramips-for-redhat-i686-gcc-4.8-linaro_uClibc-0.9.33.2/staging_dir
    CROSS_TOOLS_PATH=$build_env/wanwangbotong_BK-RC-2/OpenWrt-SDK-ramips-for-redhat-i686-gcc-4.8-linaro_uClibc-0.9.33.2/staging_dir/toolchain-i386_i486_gcc-4.8-linaro_uClibc-0.9.33.2/bin
    CROSS_TOOLS_TARGET=i486-openwrt-linux-uclibc
fi

if [ "$1" = "BK-AP300-MRW1" ]; then
    CROSS_TOOLS_PATH=$build_env/weimeng_BK-AP300-MRW1/buildroot-gcc342-wayos/bin
    CROSS_TOOLS_TARGET=mipsel-linux-uclibc
fi

# 未找到对应型号
#if [ "$1" = "H10E" ]; then
#    CROSS_TOOLS_PATH=/opt/H10E/msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331_cmcc/bin
#    CROSS_TOOLS_TARGET=mips-linux-gnu
#fi


if [ "$1" = "HG1023" ]; then
    export LD_LIBRARY_PATH=$build_env/shuangying_HG1023/mips-linux-glibc-4.6.3/usr/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/shuangying_HG1023/mips-linux-glibc-4.6.3/usr/bin
    CROSS_TOOLS_TARGET=mips-buildroot-linux-gnu
fi

if [ "$1" = "H10g-12" ]; then
    CROSS_TOOLS_PATH=$build_env/glwd_H10g-12/msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331_cmcc/bin
    CROSS_TOOLS_TARGET=mips-linux-gnu
fi

if [ "$1" = "H10e-12" ]; then
    CROSS_TOOLS_PATH=$build_env/glwd_H10e-12/msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331_cmcc/bin
    CROSS_TOOLS_TARGET=mips-linux-gnu
fi


if [ "$1" = "TEWA-808" ]; then
    export LD_LIBRARY_PATH=$build_env/tianyi_TEWA-808/crosstools-mips-gcc-5.3-linux-4.1-uclibc-1.0.12-binutils-2.25-NPTL/usr/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/tianyi_TEWA-808/crosstools-mips-gcc-5.3-linux-4.1-uclibc-1.0.12-binutils-2.25-NPTL/usr/bin
    CROSS_TOOLS_TARGET=mips-linux
fi

if [ "$1" = "QT1905" ]; then
    export LD_LIBRARY_PATH=$build_env/kukukeji_QT190X/arm-linux-glibc/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/kukukeji_QT190X/arm-linux-glibc/bin
    CROSS_TOOLS_TARGET=arm-buildroot-linux-gnueabi
fi

if [ "$1" = "QT1906" ]; then
    export LD_LIBRARY_PATH=$build_env/kukukeji_QT190X/arm-linux-glibc/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/kukukeji_QT190X/arm-linux-glibc/bin
    CROSS_TOOLS_TARGET=arm-buildroot-linux-gnueabi
fi

# 废弃
#if [ "$1" = "CMCC-HG521G" ]; then
#    CROSS_TOOLS_PATH=/opt/msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331_cmcc/bin
#    CROSS_TOOLS_TARGET=mips-linux-gnu
#fi
# 废弃
#if [ "$1" = "CMCC-HG510E" ]; then
#    CROSS_TOOLS_PATH=/opt/msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331_cmcc/bin
#    CROSS_TOOLS_TARGET=mips-linux-gnu
#fi


if [ "$1" = "B860GV21P" ]; then
    CROSS_TOOLS_PATH=$build_env/zhongxing_B860GV21P/arm-linux-uclibcgnueabi-strcmp/bin
    CROSS_TOOLS_TARGET=arm-buildroot-linux-uclibcgnueabi
fi

if [ "$1" = "B860GV2.1-P-arm" ]; then
    export LD_LIBRARY_PATH=$build_env/zhongxing_B860GV21P-arm/arm-linux-glibc/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/zhongxing_B860GV21P-arm/arm-linux-glibc/bin
    CROSS_TOOLS_TARGET=arm-linux
fi

if [ "$1" = "B860GV2.1-P-usr" ]; then
    export LD_LIBRARY_PATH=$build_env/zhongxing_B860GV21P-usr/usr/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/zhongxing_B860GV21P-usr/usr/bin
    CROSS_TOOLS_TARGET=arm-linux
fi

if [ "$1" = "TW-80X" ]; then
    CROSS_TOOLS_PATH=$build_env/teyizg_TW-80X/msdk-4.8.5-mips-EB-3.18-g2.23-m32ut-170331_cmcc/bin
    CROSS_TOOLS_TARGET=mips-linux-gnu
fi

if [ "$1" = "H10e-11" ]; then
    export LD_LIBRARY_PATH=$build_env/cmcc_xwrj_H10e-11/cross_compiler/arm-linux-glibc/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/cmcc_xwrj_H10e-11/cross_compiler/arm-linux-glibc/bin
    CROSS_TOOLS_TARGET=arm-linux
fi
# 跟H10e-11 一样
if [ "$1" = "H10g-13" ]; then
    export LD_LIBRARY_PATH=$build_env/cmcc_xwrj_H10g-11/cross_compiler/arm-linux-glibc/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/cmcc_xwrj_H10g-13/cross_compiler/arm-linux-glibc/bin
    CROSS_TOOLS_TARGET=arm-linux
fi

# x64
if [ "$1" = "DT741v230" ]; then
    CROSS_TOOLS_PATH=$build_env/chuagnwei_DT741v230/cross_compiler/arm-linux-uclibcgnueabi_soft_x64_rpc_ipv6/bin
    CROSS_TOOLS_TARGET=arm-linux-uclibcgnueabi
fi

if [ "$1" = "R3Gv2" ]; then
    export LD_LIBRARY_PATH=$build_env/dawo_xiaomi_R3Gv2/sdk_package/toolchain/lib:$LD_LIBRARY_PATH
    CROSS_TOOLS_PATH=$build_env/dawo_xiaomi_R3Gv2/sdk_package/toolchain/bin
    CROSS_TOOLS_TARGET=mipsel-xiaomi-linux-uclibc
fi

cd ../libzdpi

if [ "$1" = "H10G-12" ]; then
    sed -i '/\/\* DEV-CFG \*\//a\#define H10G12_PCAP_BPF 1' ./config.h
fi

if [[ "$1" = "BK-RC-M1" || "$1" = "dttv200" ]]; then
    sed -i '/\/\* DEV-CFG \*\//a\#define PCAP_BPF_BK_RC_M1 1' ./config.h
fi

make -f Makefile DEV=$1 clean
make -f Makefile DEV=$1 CTPATH=$CROSS_TOOLS_PATH CTTARGET=$CROSS_TOOLS_TARGET

cd ../libzfirewall

if [ "$1" = "H10G-12" ]; then
    sed -i '/\/\* DEV-CFG \*\//a\#define IPTABLES_MARK_OTHER 1' ./config.h
fi
make -f Makefile DEV=$1 clean
make -f Makefile DEV=$1 CTPATH=$CROSS_TOOLS_PATH CTTARGET=$CROSS_TOOLS_TARGET

cd ../super2d
if [[ "$1" = "hg510e" || "$1" = "hg510pg" ]]; then
    sed -i 's/^#define SAPI_SINGLE_PROC_CHECK/\/\/#define SAPI_SINGLE_PROC_CHECK/g' config.h
fi
if [[ "$1" = "js212e" || "$1" = "r2000" || "$1" = "HG1023" || "$1" = "H10G-12" ]]; then
    sed -i '/\/\* DEV-CFG \*\//a\#define FW_ZHONGYI_SCHEME 1' ./config.h
fi
if [ "$1" = "mr622" ]; then
    sed -i 's/^\#define ACL_ICMP_SUPPORT/\/\/\#define ACL_ICMP_SUPPORT/g' ./wayos/wayos_def.h
fi

if [[ "$1" = "8q74c" || "$1" = "z84" || "$1" = "kpr008" || "$1" = "Sbox-8L74" || "$1" = "BK-AP300-MRW1" ]]; then
    sed -i 's/^\#pragma pack/\/\/\#pragma pack/g' ./wayos/wayos_def.h
fi

if [ "$1" = "r2000" ]; then
    sed -i 's/^\#pragma pack/\/\/\#pragma pack/g' ./wayos/wayos_def.h
    sed -i 's/^#define FW_FOLLOW_UP_INSPECTION/\/\/#define FW_FOLLOW_UP_INSPECTION/g' config.h
    sed -i 's/^#define SAPI_SINGLE_PROC_CHECK/\/\/#define SAPI_SINGLE_PROC_CHECK/g' config.h
fi

if [ "$1" = "RELTK447" ]; then
    sed -i '/\/\* DEV-CFG \*\//a\#define RELTK447 1' ./config.h
fi

if [[ "$1" = "mr820" || "$1" = "mr622" || "$1" = "RELTK447"|| "$1" = "MTK7526" ]]; then
    sed -i '/\/\* DEV-CFG \*\//a\#define FENGHUO_SSID_AUDIT 1' ./config.h
fi

if [ -z $2 ]; then
    sed -i "s/router_model/$1/g" config.h
else
    sed -i "s/router_model/$2/g" config.h
fi

make -f Makefile DEV=$1 RELEASE=$2 clean
make -f Makefile DEV=$1 CTPATH=$CROSS_TOOLS_PATH CTTARGET=$CROSS_TOOLS_TARGET RELEASE=$2
git checkout config.h
git checkout ../libzdpi/config.h
git checkout ../libzfirewall/config.h
git checkout wayos/wayos_def.h
