from django.db import models

model = (
            ('中国移动','中国移动'),
            ('中国电信','中国电信'),
            ('中国联通','中国联通'),
    )


class PhoneNumber(models.Model):
    phoneNumber = models.CharField('手机号码', max_length=11, blank=True, null=True, help_text='手机号码')
    phoneType = models.CharField('号码运营商', max_length=10, blank=True, null=True, choices=model, help_text='号码运营商')
    utilizeUser = models.CharField('使用人', max_length=10, blank=True, null=True, help_text='使用人')
    status = models.CharField('状态', max_length=1, blank=True, null=True, default=1, help_text='状态 0-删除, 1-存在')
    update_time = models.DateTimeField('更新日期', auto_now=True)
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    user = models.CharField('操作人', max_length=20, blank=True, null=True, help_text='操作人')

    def __str__(self):
        return self.phoneNumber

    class Mate:
        """手机号码管理"""
        verbose_name = 'App-手机号码'
        verbose_name_plural = verbose_name

class PhoneApplicationsUser(models.Model):
    phoneNumber = models.CharField('手机号码', max_length=11, blank=True, null=True, help_text='手机号码')
    applicationsType = models.CharField('账户类型', max_length=10, blank=True, null=True, help_text='账户类型')
    applicationsName = models.CharField('应用名称', max_length=10, blank=True, null=True, help_text='应用名称')
    applicationsUser = models.CharField('应用账号', max_length=50, blank=True, null=True, help_text='应用账号')
    applicationsPass = models.CharField('账号密码', max_length=50, blank=True, null=True, help_text='账户密码')
    status = models.CharField('状态', max_length=1, blank=True, null=True, default=1, help_text='状态 0-删除, 1-存在')
    update_time = models.DateTimeField('更新日期', auto_now=True)
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    user = models.CharField('操作人', max_length=20, blank=True, null=True, help_text='操作人')

    def __str__(self):
        return self.phoneNumber

    class Mate:
        """
        app应用账户管理
        """
        verbose_name = 'App-应用账户'
        verbose_name_plural = verbose_name