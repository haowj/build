from django.db import models


model = (
            ('面板AP','面板AP'),
            ('二合一','二合一'),
            ('三合一','三合一'),
            ('四合一','四合一'),
            ('吸顶AP','吸顶AP'),
            ('AC网关','AC网关'),
            ('光猫AP','光猫AP'),
            ('嗅探光猫','嗅探光猫'),
            ('嗅探2合1','嗅探2合1'),
            ('室外AP','室外AP'),
            ('机顶盒','机顶盒'),
            ('交换机','交换机'),
    )


class Oem(models.Model):
    """
    Original Equipment Manufacturer Data Base
    生产厂商数据
    """
    oem_name = models.CharField('生产厂商', blank=True, max_length=100)
    oem_code = models.CharField('厂商编码', blank=True, max_length=50, help_text='厂商名称缩写')
    comment  = models.CharField('备注',blank=True,default=None,max_length=200,null=True,help_text='备注')
    user = models.CharField('操作人', max_length=30, help_text='操作人')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        设备型号
        """
        verbose_name = '厂商-厂商信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.oem_name


class DeviceModel(models.Model):
    """
    device model data base
    设备型号数据
    """
    type = models.CharField('类型', blank=True, max_length=50, choices=model, help_text='类型')
    oem_id =models.CharField('设备厂商id',blank=True,max_length=50,help_text='设备厂商id')
    zy_model = models.CharField('中建智云型号',blank=True,max_length=100,unique=True,help_text='中建智云型号')
    oem_model = models.CharField('厂商型号',blank=True,max_length=100,help_text='厂商型号')
    old_model  = models.CharField('老型号',blank=True,max_length=100,help_text='老型号')
    oem_name = models.CharField('厂商名称', blank=True,null=True,default='', max_length=100, help_text='厂商名称')
    oem_code = models.CharField('厂商编码', blank=True,null=True,default='', max_length=50, help_text='厂商名称缩写')
    comment  = models.CharField('备注',blank=True,default=None,max_length=200,null=True,help_text='备注')
    user = models.CharField('操作人', max_length=30, help_text='操作人')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        设备型号
        """
        verbose_name = '型号-设备型号对照表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.zy_model