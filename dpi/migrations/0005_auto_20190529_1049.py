# Generated by Django 2.0.2 on 2019-05-29 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0004_auto_20190525_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='DpiConfLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_id', models.CharField(blank=True, max_length=100, verbose_name='规则id')),
                ('op_info', models.CharField(max_length=500, verbose_name='规则名称')),
                ('user', models.CharField(max_length=50, verbose_name='操作人')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
            ],
            options={
                'verbose_name': 'dpiConf-更新日志',
                'verbose_name_plural': 'dpiConf-更新日志',
            },
        ),
        migrations.CreateModel(
            name='MobileInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oem', models.CharField(max_length=50, verbose_name='手机厂商')),
                ('os_name', models.CharField(max_length=50, verbose_name='操作系统名称')),
                ('os_version', models.CharField(max_length=50, verbose_name='操作系统版本')),
                ('oem_os_name', models.CharField(blank=True, max_length=50, verbose_name='手机厂商型号名称')),
                ('oem_os_version', models.CharField(blank=True, max_length=50, verbose_name='手机厂商操作系统版本')),
                ('status', models.CharField(default=1, max_length=1, verbose_name='状态:1可用0不可用')),
                ('user', models.CharField(blank=True, default='auto create', help_text='操作人', max_length=30, verbose_name='操作人')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
            ],
            options={
                'verbose_name': 'dpiConf-终端详情',
                'verbose_name_plural': 'dpiConf-终端详情',
            },
        ),
        migrations.RemoveField(
            model_name='dpipcap',
            name='os_version',
        ),
        migrations.RemoveField(
            model_name='dpipcap',
            name='phone_model',
        ),
        migrations.AddField(
            model_name='dpiconf',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='规则权重'),
        ),
        migrations.AddField(
            model_name='dpipcap',
            name='mobileinfo_id',
            field=models.IntegerField(default=0, verbose_name='手机详情ID'),
        ),
    ]
