# Generated by Django 2.0.2 on 2019-08-26 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneApplicationsUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', models.CharField(blank=True, help_text='手机号码', max_length=11, null=True, verbose_name='手机号码')),
                ('applicationsType', models.CharField(blank=True, help_text='账户类型', max_length=10, null=True, verbose_name='账户类型')),
                ('applicationsName', models.CharField(blank=True, help_text='应用名称', max_length=50, null=True, verbose_name='应用名称')),
                ('applicationsUser', models.CharField(blank=True, help_text='应用账号', max_length=50, null=True, verbose_name='应用账号')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('user', models.CharField(blank=True, help_text='操作人', max_length=20, null=True, verbose_name='操作人')),
            ],
        ),
    ]
