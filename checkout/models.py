from django.db import models
from checkout.base.redisConn import rs_conn
from checkout.base.const import get_value_list
from django.db.models.signals import post_delete
from django.dispatch import receiver


class TestCase(models.Model):
    """
    测试用例
    """
    args_command = models.CharField(u'操作指令', blank=False, null=False, max_length=50)
    args_name = models.CharField(u'匹配参数', blank=False, null=False, max_length=30)
    args_vales = models.CharField(u'指定匹配内容', blank=True, max_length=100)
    args_remark = models.TextField(u'备注', max_length=300)
    args_operator = models.CharField(u'操作人', max_length=30, help_text='操作人')
    status = models.CharField('有效性:1有效', max_length=2, default=1)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.args_name

    class Meta:
        verbose_name = '测试用例配置'
        verbose_name_plural = '测试用例配置'


class DeviceDB(models.Model):
    """
    设备状态表
    """
    stat = (
        ('0', '空闲',),
        ('1', '预执行',),
        ('2', '执行中',),
        ('3', '失败',),
    )
    oem_name = models.CharField(u'设备厂商名称', null=True, blank=True,max_length=50)
    dev_sn = models.CharField(u'设备SN', max_length=32, null=False, blank=False)
    dev_model = models.CharField(u'智云型号', blank=False, null=False, max_length=20)
    dev_ip = models.CharField(u'设备IP', blank=False, null=False, max_length=15)
    dev_port = models.CharField(u'访问端口', blank=False, null=False, max_length=10, default='')
    dev_user = models.CharField(u'设备账户', blank=False, null=False, max_length=18)
    dev_password = models.CharField(u'设备密码', blank=False, null=False, max_length=20)
    status = models.CharField(u'状态', blank=False, null=False, max_length=2, default='0', choices=stat)
    operator = models.CharField(u'操作人', max_length=30, help_text='操作人')
    remark = models.TextField(u'备注', max_length=200)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.dev_model

    class Meta:
        verbose_name = '设备状态表'
        verbose_name_plural = '设备状态表'


class CaseSet(models.Model):
    """

    测试集
    """
    case_name = models.CharField(u'集合名称', blank=False, null=False, max_length=30)
    case_action = models.CharField(u'用例项', blank=False, null=False, max_length=300)
    operator = models.CharField(u'操作人', max_length=30, help_text='操作人',default='')
    status = models.CharField('有效性:1有效',max_length=2,default=1)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.case_name

    class Meta:
        verbose_name = '测试集'
        verbose_name_plural = '测试集'


class ExecuteStrategy(models.Model):
    """
    执行策略
    """
    stat = (
        ('0', '空闲', ),
        ('1', '执行',),
        ('2', '执行中',),
        ('3', '失败',),
    )

    deviceID = models.ForeignKey(DeviceDB, verbose_name=u'设备ID', on_delete=models.CASCADE)
    caseID = models.CharField(u'测试集ID', blank=False, null=False, max_length=30)
    task_status = models.CharField(u'任务状态', blank=False, null=False, max_length=6, default='0', choices=stat)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    operator = models.CharField(u'操作人', max_length=30, help_text='操作人')
    status = models.CharField('有效性:1有效',max_length=2,default=1)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        super(ExecuteStrategy, self).save(force_insert, force_update, using, update_fields)
        rs_conn.set('ExecuteStrategy', self.task_status)

    class Meta:
        verbose_name = '执行策略'
        verbose_name_plural = '执行策略'


class StrategyRecord(models.Model):
    """
    执行策略记录表
    """
    stat = (
        ('0', '创建',),
        ('1', '上传',),
        ('2', '成功',),
        ('3', '失败',),
    )
    strategyID = models.ForeignKey(ExecuteStrategy, verbose_name=u'策略ID', on_delete=models.CASCADE, default='')
    caseID = models.CharField(u'测试集ID', blank=False, null=False, max_length=30)
    task_status = models.CharField(u'任务状态', blank=False, null=False, max_length=6, default='0', choices=stat)
    operator = models.CharField(u'操作人', max_length=30, help_text='操作人')
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '执行策略记录表'
        verbose_name_plural = '执行策略记录表'


class StrategyData(models.Model):
    """
    策略执行返回数据表
    """
    strategyRID = models.ForeignKey(StrategyRecord, verbose_name=u'记录表ID', on_delete=models.CASCADE)
    deviceID = models.ForeignKey(DeviceDB, verbose_name=u'设备ID', on_delete=models.CASCADE)
    command = models.CharField(u'操作指令', blank=False, null=False, max_length=30)
    check_rule = models.CharField(u'校验参数', blank=True, max_length=100)
    check_data = models.CharField(u'校验数据', blank=True, max_length=100)
    data = models.TextField(u'数据', max_length=300)
    result = models.CharField(u'结论', max_length=20)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '执行策略返回数据表'
        verbose_name_plural = '执行策略返回数据表'


class InitData(models.Model):
    """
    原始数据保存
    """
    strategyRID = models.ForeignKey(StrategyRecord, verbose_name=u'记录表ID', on_delete=models.CASCADE, default='')
    command = models.CharField(u'操作指令', max_length=100, default='')
    initData = models.TextField(u'原始数据', max_length=300)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '原始数据'
        verbose_name_plural = '原始数据'


class Basics(models.Model):
    """
    基础信息
    """
    Name = models.CharField(u'信息名称', max_length=60, unique=True)
    content = models.CharField(u'信息内容', max_length=100)
    remark = models.TextField(u'备注', max_length=200)
    operator = models.CharField(u'操作人', max_length=80, help_text='操作人')
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.Name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        sql = 'select Name from checkout_basics where id=%s' % self.id
        datas = get_value_list(sql)
        if datas is not None:
            rs_conn.delete(datas[0][0])
        super(Basics, self).save(force_insert, force_update, using, update_fields)
        rs_conn.set(self.Name, self.content)

    class Meta:
        verbose_name = '基础配置表'
        verbose_name_plural = '基础配置表'


@receiver(post_delete, sender=Basics)
def delete_upload_files(sender, instance, **kwargs):
    rs_conn.delete(instance.Name)

