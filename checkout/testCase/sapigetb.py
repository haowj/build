#!/sur/bin/env python3
# -*- coding:utf-8 -*-
import re


class SuperApiGetB:
    def __init__(self, values, device, active):
        self.device = device
        self.sda = None
        self.ida = None
        self.aci = active
        if values.get('sapigetb'):
            self._s_rule(values.get('sapigetb'))
        if values.get('ifconfig'):
            self._i_rule(values.get('ifconfig'))

    def _s_rule(self, args):
        data = dict()
        for i in args.split('\r\n')[:-1]:
            if 'sapigetb' in i:
                continue
            tem = i.split('=')
            data[tem[0]] = tem[1]
        self.sda = data

    def _i_rule(self, args):
        data = dict()
        for i in args.split('\r\n\r\n')[:-1]:
            if 'ifconfig' in i:
                continue
            data[i[:i.index(' ')]] = i
        self.ida = data

    @property
    def sn(self):
        return '设备输出数据：sn = {} || 指定匹配参数数据：{}'.format(self.sda.get('sn'), self.device.dev_sn), \
               self.sda.get('sn') == self.device.dev_sn

    @property
    def oemcode(self):
        return '设备输出数据：oemcode = {} || 指定匹配参数数据：{}'.format(self.sda.get('oemcode'), self.device.oem_code), \
               self.sda.get('oemcode') == self.device.oem_code

    @property
    def dev_model(self):
        return '设备输出数据：dev_model = {} || 指定匹配参数数据：{}'.format(self.sda.get('dev_model'), self.device.dev_model), \
               self.sda.get('dev_model') == self.device.dev_model

    @property
    def lan_mac(self):
        pattern = re.compile(r'([A-Z0-9]{2}:){5}[A-Z0-9]{2}')
        loc_ = self.sda.get('local_ifname').split(',') if self.sda.get('local_ifname') else []
        lob_ = self.sda.get('lan_mac').split(',') if self.sda.get('lan_mac') else []
        lob_d = str()
        ast = False
        if len(loc_) == len(lob_):
            for i in range(len(loc_)):
                loc_d = self.ida[loc_[i]]
                mm = pattern.search(loc_d)
                if mm:
                    ast = lob_[i] == mm.group().replace(':', '')
                    lob_d += mm.group() + ','
                else:
                    ast = False
                    break
            return '设备输出数据：lan_mac = {} || ifconfig获取数据：{}'.format(self.sda.get('lan_mac'), lob_d[:-1]), ast

        return '设备输出数据：lan_mac = {} || local_ifname：{}'.format(self.sda.get('lan_mac'),
                                                               self.sda.get('local_ifname')), ast

    @property
    def wan_mac(self):
        pattern = re.compile(r'([A-Z0-9]{2}:){5}[A-Z0-9]{2}')
        loc_ = self.sda.get('wan_ifname').split(',') if self.sda.get('wan_ifname') else []
        lob_ = self.sda.get('wan_mac').split(',') if self.sda.get('wan_mac') else []
        lob_d = str()
        ast = False
        if len(loc_) == len(lob_):
            for i in range(len(loc_)):
                loc_d = self.ida[loc_[i]]
                mm = pattern.search(loc_d)
                if mm:
                    ast = lob_[i] == mm.group().replace(':', '')
                    lob_d += mm.group() + ','
                else:
                    ast = False
                    break
            return '设备输出数据：wan_mac = {} || ifconfig获取数据：{}'.format(self.sda.get('wan_mac'), lob_d[:-1]), ast

        return '设备输出数据：wan_mac = {} || local_ifname：{}'.format(self.sda.get('wan_mac'),
                                                               self.sda.get('local_ifname')), ast

    @property
    def wifi_mac(self):
        w_m = self.sda.get('wifi_mac').split(',') if self.sda.get('wifi_mac') else []
        s_d = self.sda.get('ssid').split(',') if self.sda.get('ssid') else []
        w_d = self.sda.get('widx').split(',') if self.sda.get('widx') else []
        ast = len(w_m) == len(s_d) == len(w_d)
        return '设备输出数据：wifi_mac = {} || ssid = {} || widx = {}'.format(self.sda.get('wifi_mac'), self.sda.get('ssid'),
                                                                       self.sda.get('widx')), ast

    @property
    def rom_build(self):
        r_b = self.sda.get('rom_build')
        pattern = re.compile(r'\d{4}(\-|\/|.)\d{1,2}\1\d{1,2}T\d{2}(:)\d{2}\2\d{2}\+\d{4}')
        mm = pattern.search(r_b)
        if mm:
            ast = True
        else:
            ast = False

        return '设备输出数据：rom_build = {} || '.format(self.sda.get('rom_build')), ast

    @property
    def dialup(self):
        ast = '1' == self.sda.get('dialup')
        return '设备输出数据：rom_build = {} || 0-未知，1-DHCP，2-PPPoE，3-静态IP '.format(self.sda.get('dialup')), ast

    @property
    def gwip(self):

        pattern = re.compile(r'inet addr:([0-9]{0,3}.){3}.[0-9]{0,3}')
        loc_ = self.sda.get('local_ifname').split(',') if self.sda.get('local_ifname') else []
        lob_ = self.sda.get('gwip').split(',') if self.sda.get('gwip') else []
        lob_d = str()
        ast = False
        if len(loc_) == len(lob_):
            for i in range(len(loc_)):
                loc_d = self.ida[loc_[i]]
                mm = pattern.search(loc_d)
                if mm:
                    ast = lob_[i] == mm.group().replace('inet addr:', '')
                    lob_d += mm.group() + ','
                else:
                    ast = False
                    break
            return '设备输出数据：gwip ={} || ifconfig获取数据：{}'.format(self.sda.get('gwip'), lob_d[:-1]), ast

        return '设备输出数据：gwip ={} || local_ifname：{}'.format(self.sda.get('gwip'), self.sda.get('local_ifname')), ast

    @property
    def gwmask(self):
        pattern = re.compile(r'Mask:([0-9]{0,3}.){3}.[0-9]{0,3}')
        loc_ = self.sda.get('local_ifname').split(',') if self.sda.get('local_ifname') else []
        lob_ = self.sda.get('gwmask').split(',') if self.sda.get('gwmask') else []
        lob_d = str()
        ast = False
        if len(loc_) == len(lob_):
            for i in range(len(loc_)):
                loc_d = self.ida[loc_[i]]
                mm = pattern.search(loc_d)
                if mm:
                    ast = lob_[i] == mm.group().replace('Mask:', '')
                    lob_d += mm.group() + ','
                else:
                    ast = False
                    break
            return '设备输出数据：gwmask ={} || ifconfig获取数据：{}'.format(self.sda.get('gwmask'), lob_d[:-1]), ast

        return '设备输出数据：gwmask ={} || local_ifname：{}'.format(self.sda.get('gwmask'), self.sda.get('local_ifname')), ast

    @property
    def local_ips(self):
        loc_ = self.sda.get('local_ips')
        lob_ = self.sda.get('gwip')

        i_ = self.device.dev_ip
        ast = lob_ and i_ in loc_
        return '设备输出数据：gwip = {} || local_ips = {} || 设备IP地址'.format(lob_, loc_, str(i_)), ast

    @property
    def hw_ver(self):
        loc_ = self.sda.get('hw_ver')
        if self.aci:
            ast = loc_ == self.aci
        else:
            ast = ''

        return '设备输出数据：hw_ver = {} ||'.format(loc_), ast

    @property
    def rom_ver(self):
        loc_ = self.sda.get('rom_ver')
        if self.aci:
            ast = loc_ == self.aci
        else:
            ast = ''

        return '设备输出数据：rom_ver = {} ||'.format(loc_), ast

    @property
    def widx(self):
        loc_ = self.sda.get('widx')
        if self.aci:
            ast = loc_ == self.aci
        else:
            ast = ''

        return '设备输出数据：widx = {} ||'.format(loc_), ast

    @property
    def ssid(self):
        loc_ = self.sda.get('ssid')
        if self.aci:
            ast = loc_ == self.aci
        else:
            ast = ''
        return '设备输出数据：ssid = {} ||'.format(loc_), ast

    @property
    def local_ifname(self):
        loc_ = self.sda.get('local_ifname')
        if self.aci:
            ast = loc_ == self.aci
        else:
            ast = ''

        return '设备输出数据：local_ifname = {} ||'.format(loc_), ast

    @property
    def wan_ifname(self):
        loc_ = self.sda.get('wan_ifname')
        if self.aci:
            ast = loc_ == self.aci
        else:
            ast = ''
        return '设备输出数据：wan_ifname = {} ||'.format(loc_), ast
