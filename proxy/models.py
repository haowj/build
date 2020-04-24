from django.db import models

# Create your models here.
class proxyVersion(models.Model):
    """
    superd版本
    """
    dev_model = models.CharField('设备型号', max_length=50,default='', help_text='设备型号')
    proxy_version = models.CharField('版本', max_length=50,)
    proxy_file = models.FileField('文件路径', upload_to='upload/supertack/%Y/%m/%d')
    download_url = models.CharField('下载url', default='',max_length=200, help_text='下载url')
    user = models.CharField('操作人', max_length=30, help_text='操作人')
    build_reason = models.TextField('构建说明', max_length=500, null=True, blank=True, help_text='构建说明')
    md5 = models.CharField('MD5', max_length=50, null=True, blank=True, help_text='md5')
    build_result = models.CharField('构建结果', max_length=50, null=True, blank=True, help_text='构建结果')
    build_status = models.CharField('构建状态码', max_length=50, null=True, blank=True, help_text='构建状态码')
    build_type = models.CharField('构建类型', max_length=50, null=True, blank=True,default='', help_text='构建类型')
    time_stamp = models.CharField('时间戳', max_length=50, null=True, blank=True,default='0', help_text='时间戳')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        重命名表名称
        """
        verbose_name = '版本-反向代理版本'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.proxy_version