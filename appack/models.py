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
map_dev_model_type = (('原始名称','原始名称'),('大小写不同','大小写不同'),('交叉编译链简称','交叉编译链简称'),('型号不一样','型号不一样'),('交叉编译链一样','交叉编译链一样'),)


ver = (
        ('1.0', "1.0"),
        ('1.5', "1.5"),
        ('2.0', "2.0"),
        ('2.5', "2.5"),
        ('3.0', "3.0"),
    )

packtype = (
    ('gzip', 'gzip'),
    ('lzma', 'lzma'),
)


class oem_db(models.Model):

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

class dev_model_db(models.Model):
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

class map_dev_model_db(models.Model):
    type = models.CharField('类型', blank=True, max_length=50, choices=map_dev_model_type, help_text='类型')
    dev_model = models.CharField('设备型号', blank=True, max_length=50,  help_text='类型')
    map_dev_model = models.CharField('Cbuild中设备型号', blank=True, max_length=50)
    comment = models.CharField('备注', blank=True, max_length=50)
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        设备型号
        """
        verbose_name = '构建-设备型号构建映射表'
        verbose_name_plural = verbose_name

# Create your models here.
class build_log(models.Model):
    dev_model = models.CharField('设备型号', max_length=50, default='',help_text='设备型号')
    user = models.CharField('操作人',default='', max_length=50)
    build_reason = models.TextField('构建原因',default='', max_length=200)
    build_tag = models.TextField('构建版本',default='', max_length=200)
    build_result = models.TextField('构建结果',default='', max_length=1000)
    build_status = models.TextField('构建状态码',default='', max_length=200)
    type = models.CharField('构建类型',default='', max_length=30)
    comment = models.CharField('备注',default='', max_length=200)
    time_stamp = models.CharField('时间戳', max_length=50, null=True, blank=True,default='0', help_text='时间戳')
    create_time = models.DateTimeField('创建日期',auto_now_add=True)
    update_time = models.DateTimeField('更新日期',auto_now=True)
    class Meta:
        """
        构建-日志
        """
        verbose_name = '插件-构建日志'
        verbose_name_plural = verbose_name



class sapiloaderVersion(models.Model):
    """
    加载器版本
    """
    sapiloader_file = models.FileField('加载器文件', upload_to='upload/sapiloader/%Y/%m/%d', help_text='加载器文件')
    sapiloader_version = models.CharField('superloader版本', max_length=50, help_text='superloader版本')
    user = models.CharField('操作人', max_length=30, help_text='操作人')
    comment = models.TextField('备注', max_length=500, null=True, blank=True, help_text='备注')
    md5 = models.CharField('MD5', max_length=50, null=True, blank=True, help_text='md5')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        重命名表名称
        """
        verbose_name = '版本-加载器版本'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.sapiloader_version

class sapiloaderCVersion(models.Model):
    """
    加载器版本
    """
    dev_model = models.CharField('设备型号', max_length=50, default='', help_text='设备型号')
    sapiloaderC_version = models.CharField('sapiloaderC版本', max_length=50, help_text='sapiloaderC版本')
    sapiloaderC_file = models.FileField('sapiloaderC文件', upload_to='upload/supertack/%Y/%m/%d', help_text='sapiloaderC文件')
    download_url = models.CharField('下载url', default='',max_length=200, help_text='下载url')
    user = models.CharField('操作人', max_length=30, help_text='操作人')
    build_reason = models.TextField('构建说明', max_length=500, null=True, blank=True, help_text='构建说明')
    md5 = models.CharField('MD5', max_length=50, null=True, blank=True, help_text='md5')
    build_result = models.CharField('构建结果', max_length=50, null=True, blank=True, help_text='构建结果')
    build_status = models.CharField('构建状态码', max_length=50, null=True, blank=True, help_text='构建状态码')
    build_type = models.CharField('构建类型', max_length=50, null=True, blank=True,default='', help_text='构建类型')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        """
        重命名表名称
        """
        verbose_name = '版本-加载器版本(C)'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.sapiloaderC_version

class superdcfVersion(models.Model):
    """
    superd配置文件版本
    """
    dev_model = models.CharField('设备型号', max_length=50, default='', help_text='设备型号')
    superdcf_version = models.CharField('superdcf版本',max_length=50,help_text='superdcf版本')
    superdcf_file = models.FileField('superdcf文件',upload_to='upload/superdcf/%Y/%m/%d',help_text='superdcf文件')
    user = models.CharField('操作人', max_length=30, help_text='操作人')
    md5 = models.CharField('MD5', max_length=50, null=True, blank=True, help_text='md5')
    type = models.CharField('类型', max_length=50, null=True, blank=True, help_text='类型')
    comment = models.TextField('备注', max_length=500, null=True, blank=True, help_text='备注')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)

    class Meta:
        """
        重命名表名称
        """
        verbose_name = '版本-superd配置文件版本'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.superdcf_version

class superctlVersion(models.Model):
    """
    superctl版本
    """
    dev_model = models.CharField('设备型号', max_length=50, default='', help_text='设备型号')
    superctl_version = models.CharField('superctl版本', max_length=50, help_text='superctl版本')
    superctl_file = models.FileField('superctl文件', upload_to='upload/superctl/%Y/%m/%d', help_text='superctl文件')
    user = models.CharField('操作人', max_length=30, help_text='操作人')
    comment = models.TextField('备注', max_length=500, null=True, blank=True, help_text='备注')
    md5 = models.CharField('MD5', max_length=50, null=True, blank=True, help_text='md5')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        重命名表名称
        """
        verbose_name = '版本-superctl版本'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.superctl_version

class supertackVersion(models.Model):
    """
    supertack版本
    """
    dev_model = models.CharField('设备型号', max_length=50, default='', help_text='设备型号')
    supertack_version = models.CharField('supertack版本', max_length=50, help_text='supertack版本')
    supertack_file = models.FileField('supertack文件', upload_to='upload/supertack/%Y/%m/%d', help_text='supertack文件')
    user = models.CharField('操作人', max_length=30, help_text='操作人')
    comment = models.TextField('备注', max_length=500, null=True, blank=True, help_text='备注')
    md5 = models.CharField('MD5', max_length=50, null=True, blank=True, help_text='md5')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        重命名表名称
        """
        verbose_name = '版本-supertack版本'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.supertack_version

class dpiConfigVersion(models.Model):
    """
    dpi配置文件版本
    """
    dev_model = models.CharField('设备型号', max_length=50, default='')
    dev_model_id = models.CharField('设备型号id', max_length=50, default='')
    zdpi_sig_version = models.CharField('dpi配置文件版本', max_length=50)
    zdpi_sig_file = models.FileField('dpi配置文件', upload_to='upload/dpiConfig/%Y/%m/%d')
    user = models.CharField('操作人', max_length=30)
    comment = models.TextField('备注', max_length=500, null=True, blank=True)
    md5 = models.CharField('MD5', max_length=50, null=True, blank=True)
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        重命名表名称
        """
        verbose_name = '版本-dpi配置文件版本'
        verbose_name_plural = verbose_name

class superdVersion(models.Model):
    """
    superd版本
    """
    dev_model = models.CharField('设备型号', max_length=50,default='', help_text='设备型号')
    superd_version = models.CharField('superd版本', max_length=50, help_text='superd版本')
    superd_file = models.FileField('superd文件', upload_to='upload/supertack/%Y/%m/%d', help_text='superd文件')
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
        verbose_name = '版本-superd版本'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.superd_version

class version_contorl(models.Model):
    """
    版本控制表
    """
    dev_model_id = models.CharField('设备型号id', max_length=50,default='', help_text='设备型号')
    rom_version = models.CharField('固件版本',max_length=100,help_text='固件版本')
    docking_solution = models.CharField('对接方案',max_length=32, choices=ver, default="1.0",help_text='对接方案')
    pack_type = models.CharField('压缩方式',max_length=30,choices=packtype,help_text='压缩方式')
    package_contains_path = models.CharField('压缩包内路径',max_length=100,default='sapi/run',help_text='压缩包内路径')
    package_contains_path_type = models.CharField('压缩包内路径类型',max_length=100,default='supertack',help_text='压缩包内路径类型')
    sapiloader_version_id = models.CharField('加载器id',max_length=30,null=True, blank=True,help_text='加载器id')
    sapiloaderC_version_id = models.CharField('加载器(C)id',max_length=30,null=True, blank=True,help_text='加载器(C)id')
    superctl_version_id = models.CharField('连接器id',max_length=30,null=True, blank=True,help_text='连接器id')
    supertack_version_id = models.CharField('连接器(C)id',max_length=30,null=True, blank=True,help_text='连接器(C)id')
    superd_version_id = models.CharField('插件id',max_length=30,null=True, blank=True,help_text='插件id')
    superdcf_version_id = models.CharField('配置文件id',max_length=30,null=True, blank=True,help_text='配置文件id')
    zdpi_sig_version_id = models.CharField('dpi配置文件id',max_length=30,null=True, blank=True)
    user = models.CharField('操作人',max_length=50,help_text='操作人')
    comment = models.TextField('备注', max_length=500, null=True, blank=True, help_text='备注')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        重命名表名称
        """
        verbose_name = '版本-维护信息控制表'
        verbose_name_plural = verbose_name

class pack_list_contorl(models.Model):
    """
    构建结果表
    """
    dev_model = models.CharField('设备型号', max_length=50, default='',help_text='设备型号')
    superd_version = models.CharField('插件版本',max_length=32, default="1.0",help_text='插件版本')
    connector_version = models.CharField('连接器版本',max_length=32, default="1.0",help_text='连接器版本')
    superdcf_version = models.CharField('配置文件版本',max_length=32, default="1.0",help_text='配置文件版本')
    zdpi_sig_version = models.CharField('DPI配置文件版本',max_length=32, default="1.0")
    release_version = models.CharField('线上版本',max_length=32, default="1.0",help_text='线上版本')
    docking_solution = models.CharField('对接方案',max_length=32, choices=ver, default="1.0",help_text='对接方案')
    package_contains_path = models.CharField('包内路径',max_length=32, default="",help_text='包内路径')
    package_contains_path_type = models.CharField('压缩包内路径类型',max_length=100,default='supertack',help_text='压缩包内路径类型')
    pack_type = models.CharField('压缩方式',max_length=30,choices=packtype,help_text='压缩方式')
    pack_name = models.CharField('压缩包名称',max_length=100,default='',help_text='压缩包名称')
    md5 = models.CharField('压缩包md5',max_length=100,default='',help_text='压缩包md5')
    pack_content = models.CharField('压缩包内容描述',max_length=500,null=True,blank=True,help_text='压缩包内容描述')
    package = models.FileField('插件包', upload_to='upload/package/%Y/%m/%d',max_length=200, help_text='插件包')
    download_url = models.CharField('下载地址',max_length=200,null=True,blank=True,help_text='下载地址')
    user = models.CharField('操作人',max_length=50,help_text='操作人')
    build_time = models.CharField('构建时间', max_length=50,null=True,blank=True,help_text='构建时间')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        重命名表名称
        """
        verbose_name = '打包结果-PG包'
        verbose_name_plural = verbose_name

class sapiloader_pack(models.Model):
    dev_model = models.CharField('设备型号', max_length=50,default='',blank=True,null=True)
    version = models.CharField('加载器版本', max_length=50,default='',blank=True,null=True)
    reason = models.CharField('构建原因', max_length=30,default='',blank=True,null=True)
    pack_name = models.CharField('包名称', max_length=100,default='',blank=True,null=True)
    pack_save_path = models.CharField('包存放路径', max_length=300,default='',blank=True,null=True)
    url = models.CharField('下载链接', max_length=300,default='',blank=True,null=True)
    md5 = models.CharField('压缩包md5',max_length=100,default='',help_text='压缩包md5')

    user = models.CharField('构建人', max_length=50,default='',blank=True,null=True)
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        重命名表名称
        """
        verbose_name = '打包结果-加载器包'
        verbose_name_plural = verbose_name

class release_plug_log(models.Model):
    dev_model = models.CharField('设备型号', max_length=50)
    rtype = models.CharField('上线类型', default='pg',blank=True,max_length=50)
    user = models.CharField('操作人', max_length=50)
    plug_title_name = models.CharField('配置项名称', default='',max_length=100)
    plug_name = models.CharField('插件文件名称', max_length=100)
    plug_md5 = models.CharField('插件的md5值', max_length=100)
    version = models.CharField('上线版本号', max_length=50,blank=True)
    cmd_content = models.CharField('加载器执行命令',max_length=500,blank=True,default='')
    comment = models.CharField('上线说明', max_length=500,blank=True)
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        上线插件日志
        """
        verbose_name = '插件-发布上线操作日志'
        verbose_name_plural = verbose_name
class Operatingtag(models.Model):
    project_name = models.CharField('项目名称', default='',max_length=50)
    project_path = models.CharField('项目路径', default='',max_length=100)
    tag = models.CharField('tag号', max_length=50,blank=True)
    comment = models.CharField('comment', max_length=50,blank=True)
    status = models.CharField('状态',default=1, max_length=50,blank=True)
    user = models.CharField('操作人', max_length=50)
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        上线插件日志
        """
        verbose_name = '版本-版本号信息记录'
        verbose_name_plural = verbose_name

class advertising(models.Model):
    title = models.CharField('标题', default='',blank=True,null=True,max_length=100)
    user = models.CharField('操作人',default='', max_length=50)
    content = models.CharField('内容', default='',max_length=1000)
    type = models.CharField('类型', max_length=30,blank=True,default='')
    location = models.CharField('位置', max_length=50,blank=True,null=True,default='')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """
        上线插件日志
        """
        verbose_name = '公告-全局广播内容'
        verbose_name_plural = verbose_name

class unpack_cmd(models.Model):
    dev_model = models.CharField('设备型号', default='',blank=True,null=True,max_length=100)
    unpack_cmd = models.CharField('解压命令', default='',blank=True,null=True,max_length=100)
    run_cmd = models.CharField('启动命令', default='',blank=True,null=True,max_length=100)
    user = models.CharField('操作人',default='', max_length=50)
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        """

        """
        verbose_name = '记录-PG包解压命令'
        verbose_name_plural = verbose_name