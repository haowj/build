from django.db import models

# 审计3.0服务 生成vi_type_id 使用
class IdentityTypeCoding(models.Model):
    identityType = models.CharField('身份类型编码', max_length=30)
    en = models.CharField('EN', max_length=15)
    code = models.CharField('CODE', max_length=1)
    explaines = models.CharField('说明', max_length=60)
    comment = models.CharField('备注',blank=True,default=None,max_length=200,null=True,help_text='备注')
    user = models.CharField('操作人', max_length=30, help_text='操作人',blank=True,default='auto create')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        verbose_name = 'audit3.0-身份类型编码'
        verbose_name_plural = 'audit3.0-身份类型编码'

class BusinessType(models.Model):
    businessType = models.CharField('业务类型', max_length=30)
    en = models.CharField('EN', max_length=15)
    code = models.CharField('CODE', max_length=2)
    comment  = models.CharField('备注',blank=True,default=None,max_length=200,null=True,help_text='备注')
    user = models.CharField('操作人', max_length=30, help_text='操作人',blank=True,default='auto create')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        verbose_name = 'audit3.0-业务类型'
        verbose_name_plural = 'audit3.0-业务类型'

    def __str__(self):
        return self.businessType

class EnterpriseCoding(models.Model):
    name = models.CharField('企业名称', max_length=100)
    en = models.CharField('EN', max_length=15, blank=True)
    code = models.CharField('CODE', max_length=4)
    typeCode = models.ForeignKey(BusinessType, verbose_name='业务类型', on_delete=models.CASCADE)
    comment = models.CharField('备注',blank=True,default=None,max_length=200,null=True,help_text='备注')
    user = models.CharField('操作人', max_length=30, help_text='操作人',blank=True,default='auto create')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        verbose_name = 'audit3.0-企业名称'
        verbose_name_plural = 'audit3.0-企业名称'

    def __str__(self):
        return self.name
# 审计3.0服务 生成vi_type_id 结束

# 各网安平台虚拟身份入库
class NetSafetyPlatform(models.Model):
    wname = models.CharField('网安平台名称', max_length=100)
    code = models.CharField('网安平台编码', unique=True, max_length=100)
    status = models.CharField('状态-0可用-1不可用', default=0, max_length=1)

    class Meta:
        verbose_name = '网安-平台基础信息'
        verbose_name_plural = '网安-平台基础信息'

    def __str__(self):
        return self.wname

class ProtocolType(models.Model):
    typeName = models.CharField('类型名称', max_length=100)
    code = models.CharField('类型编码', max_length=100)
    platformCode = models.ForeignKey(NetSafetyPlatform, verbose_name='平台编码', on_delete=models.CASCADE)
    status = models.CharField('状态-0可用-1不可用', default=0, max_length=1)

    class Meta:
        verbose_name = '网安-平台类型信息'
        verbose_name_plural = '网安-平台类型信息'

    def __str__(self):
        return self.typeName

class ProtocolApplication(models.Model):
    appName = models.CharField('应用名称', max_length=100)
    code = models.CharField('应用编码', unique=True, max_length=100)
    typeCode = models.ForeignKey(ProtocolType, verbose_name='类型编码', on_delete=models.CASCADE)
    platformCode = models.ForeignKey(NetSafetyPlatform, verbose_name='平台编码', on_delete=models.CASCADE)
    status = models.CharField('状态-0可用-1不可用', default=0, max_length=1)
    class Meta:
        verbose_name = '网安-平台应用信息'
        verbose_name_plural = '网安-平台应用信息'
    def __str__(self):
        return self.appName

class AppProCode(models.Model):
    ns_appname = models.CharField('网安平台企业名称', max_length=100)
    ns_code = models.CharField('网安平台企业code', max_length=10)
    vi_ec_id = models.CharField('智云企业id', max_length=20, blank=True,)
    platformCode = models.ForeignKey(NetSafetyPlatform, verbose_name='网安平台编码', on_delete=models.CASCADE,help_text='网安平台编码')
    comment = models.CharField('备注', blank=True, default=None, max_length=200, null=True, help_text='备注')
    user = models.CharField('操作人', max_length=30, help_text='操作人', blank=True, default='auto create')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        verbose_name = '网安-平台企业名称'
        verbose_name_plural = '网安-平台企业名称'
# 各网安平台虚拟身份入库 结束

# dpi信息维护 开始
class Multimode(models.Model):
    type_id = models.IntegerField('多模类型id')
    type_value = models.CharField('多模类型值', max_length=50)
    status = models.CharField('状态:1可用0不可用', default=1, max_length=1)
    comment = models.CharField('备注', blank=True, default=None, max_length=200, null=True, help_text='备注')
    user = models.CharField('操作人', max_length=30, help_text='操作人', blank=True, default='auto create')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        verbose_name = 'dpiConf-多模'
        verbose_name_plural = 'dpiConf-多模'
    def __str__(self):
        return self.type_value

class MobileInfo(models.Model):
    oem = models.CharField('手机厂商', max_length=50)
    os_name = models.CharField('操作系统名称', max_length=50)
    os_version = models.CharField('操作系统版本', max_length=50)
    oem_os_name = models.CharField('手机厂商型号名称', max_length=50,blank=True)
    oem_os_version = models.CharField('手机厂商操作系统版本', max_length=50,blank=True)
    status = models.CharField('状态:1可用0不可用', default=1, max_length=1)
    user = models.CharField('操作人', max_length=30, help_text='操作人', blank=True, default='auto create')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        verbose_name = 'dpiConf-终端详情'
        verbose_name_plural = 'dpiConf-终端详情'
    def __str__(self):
        return self.oem

class DpiPcap(models.Model):
    vi_type_id = models.IntegerField('虚拟身份类型id')
    taget_account = models.CharField('检索账号', max_length=100)
    mobileinfo_id = models.IntegerField('手机详情ID',default=0)
    app_type = models.CharField('应用类型:app/web', max_length=20)
    app_version = models.CharField('应用版本', max_length=50)
    md5 = models.CharField('pacp文件的md5', max_length=50)
    file_save_path_name = models.CharField('文件存储的绝对路径', max_length=200)
    status = models.CharField('状态:1可用0不可用', default=1, max_length=1)
    comment = models.CharField('备注', blank=True, default=None, max_length=200, null=True, help_text='备注')
    user = models.CharField('操作人', max_length=30, help_text='操作人', blank=True, default='auto create')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        verbose_name = 'dpiConf-Pcap文件维护'
        verbose_name_plural = 'dpiConf-Pcap文件维护'

class DpiConfLog(models.Model):
    rule_id =  models.CharField('规则id',max_length=100,blank=True)
    op_info = models.CharField('规则名称', max_length=500)
    user = models.CharField('操作人', max_length=50)
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        verbose_name = 'dpiConf-更新日志'
        verbose_name_plural = 'dpiConf-更新日志'

class DpiConf(models.Model):
    rule_name = models.CharField('规则名称', max_length=50)
    vi_type_id = models.IntegerField('虚拟身份类型id')
    weight = models.IntegerField('规则权重', default=0)
    multimode = models.ForeignKey(Multimode, verbose_name='多模id', on_delete=models.CASCADE,help_text='多模id')
    dpipcap_id = models.IntegerField('dpipcapID')
    rule_data = models.CharField('规则内容', max_length=200)
    rule_begin_match = models.CharField('规则匹配开始内容', max_length=50)
    rule_end_match = models.CharField('规则匹配结束内容', max_length=50)
    status = models.CharField('状态:1可用0不可用', default=1, max_length=1)
    comment = models.CharField('备注', blank=True, default=None, max_length=200, null=True, help_text='备注')
    user = models.CharField('操作人', max_length=30, help_text='操作人', blank=True, default='auto create')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        verbose_name = 'dpiConf-配置详情'
        verbose_name_plural = 'dpiConf-配置详情'
    def __str__(self):
        return self.rule_name

# dpi信息维护 结束