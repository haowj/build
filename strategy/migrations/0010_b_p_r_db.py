# Generated by Django 2.0.2 on 2019-07-05 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0009_auto_20190705_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='B_P_R_DB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dev_model', models.CharField(default='', help_text='设备型号', max_length=50, verbose_name='设备型号')),
                ('superd_version', models.CharField(default='1.0', help_text='插件版本', max_length=32, verbose_name='插件版本')),
                ('connector_version', models.CharField(default='1.0', help_text='连接器版本', max_length=32, verbose_name='连接器版本')),
                ('superdcf_version', models.CharField(default='1.0', help_text='配置文件版本', max_length=32, verbose_name='配置文件版本')),
                ('zdpi_sig_version', models.CharField(default='1.0', max_length=32, verbose_name='DPI配置文件版本')),
                ('release_version', models.CharField(default='1.0', help_text='线上版本', max_length=32, verbose_name='线上版本')),
                ('docking_solution', models.CharField(choices=[('1.0', '1.0'), ('1.5', '1.5'), ('2.0', '2.0'), ('2.5', '2.5'), ('3.0', '3.0')], default='1.0', help_text='对接方案', max_length=32, verbose_name='对接方案')),
                ('package_contains_path', models.CharField(default='', help_text='包内路径', max_length=32, verbose_name='包内路径')),
                ('package_contains_path_type', models.CharField(default='supertack', help_text='压缩包内路径类型', max_length=100, verbose_name='压缩包内路径类型')),
                ('pack_type', models.CharField(choices=[('gzip', 'gzip'), ('lzma', 'lzma')], help_text='压缩方式', max_length=30, verbose_name='压缩方式')),
                ('pack_name', models.CharField(default='', help_text='压缩包名称', max_length=100, verbose_name='压缩包名称')),
                ('md5', models.CharField(default='', help_text='压缩包md5', max_length=100, verbose_name='压缩包md5')),
                ('pack_content', models.CharField(blank=True, help_text='压缩包内容描述', max_length=500, null=True, verbose_name='压缩包内容描述')),
                ('package', models.FileField(help_text='插件包', max_length=200, upload_to='upload/package/%Y/%m/%d', verbose_name='插件包')),
                ('download_url', models.CharField(blank=True, help_text='下载地址', max_length=200, null=True, verbose_name='下载地址')),
                ('user', models.CharField(help_text='操作人', max_length=50, verbose_name='操作人')),
                ('build_time', models.CharField(blank=True, help_text='构建时间', max_length=50, null=True, verbose_name='构建时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
            ],
            options={
                'verbose_name': '打包结果-PG包',
                'verbose_name_plural': '打包结果-PG包',
            },
        ),
    ]
